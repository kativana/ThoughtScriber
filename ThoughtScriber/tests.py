from django.test import TestCase

# Create your tests here.
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
import os



class AudioTranscriptionTests(APITestCase):
    def test_audio_transcription(self):
        # Path to a test audio file (e.g., test_audio.mp3)
        test_audio_path = os.path.join(settings.BASE_DIR, 'ThoughtScriberProject\\test_files', 'test_audio.mp3')

        with open(test_audio_path, 'rb') as audio_file:
            uploaded_file = SimpleUploadedFile('test_audio.mp3', audio_file.read(), content_type='audio/mp3')
            response = self.client.post(reverse('audio-transcribe'), {'audio_file': uploaded_file}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('transcription', response.data)
        # Additional assertions as needed
