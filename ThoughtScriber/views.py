from django.shortcuts import render

# Create your views here.
import subprocess
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os 
from django.conf import settings
from google.cloud import speech
import io
import logging
import time

logger = logging.getLogger(__name__)



def convert_mp3_to_wav_subprocess(mp3_file_path, wav_file_path):
    command = [
        'ffmpeg',
        '-i', mp3_file_path,
        '-acodec', 'pcm_s16le',
        '-ac', '1',
        '-ar', '16000',
        wav_file_path
    ]
    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info("Conversion successful")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error converting MP3 to WAV: {e.stderr.decode('utf-8')}")
        raise e


def transcribe_audio(speech_file_path):
    # Instantiates a client using the credentials in the environment variable
    client = speech.SpeechClient()

    # Loads the audio into memory
    with io.open(speech_file_path, 'rb') as audio_file:
        content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)

    # Gather all the transcriptions into a list
    return [result.alternatives[0].transcript for result in response.results]


class AudioTranscribeView(APIView):

    def post(self, request, *args, **kwargs):
        start_time = time.time()

        # Ensure the media directory exists
        media_dir = os.path.join(settings.BASE_DIR, 'media')
        if not os.path.exists(media_dir):
            os.makedirs(media_dir)

        logger.info("Received transcription request")

        audio_file = request.FILES.get('audio_file', None)
        if not audio_file:
            logger.error("No audio file provided")
            return Response({'error': 'No audio file provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Define temporary file paths
        temp_mp3_path = os.path.join(media_dir, 'temp_audio.mp3')
        temp_wav_path = os.path.join(media_dir, 'temp_converted_audio.wav')

        # Save the uploaded MP3 file temporarily
        with open(temp_mp3_path, 'wb+') as f:
            for chunk in audio_file.chunks():
                f.write(chunk)
        logger.info(f"Audio file saved temporarily at {temp_mp3_path}")

        # Convert the file from MP3 to WAV using subprocess
        try:
            convert_mp3_to_wav_subprocess(temp_mp3_path, temp_wav_path)
            transcriptions = transcribe_audio(temp_wav_path)
            logger.info("Transcription successful")
           
        except Exception as e:
            logger.error(f'Error in processing audio file: {str(e)}')
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            if os.path.exists(temp_mp3_path): os.remove(temp_mp3_path)
            if os.path.exists(temp_wav_path): os.remove(temp_wav_path)
            logger.info("Temporary audio file deleted")

            end_time = time.time()  # Record the end time of the request
            logger.info(f"Transcription process completed in {end_time - start_time} seconds")

        return Response({'transcription': transcriptions}, status=status.HTTP_200_OK)


def record_audio(request):
    return render(request, 'audio/record_audio.html')


