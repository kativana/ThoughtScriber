# ThoughtScriber

## Description
A Django-based application that transcribes audio to text.

## Features
- **Audio Recording:** Users can initiate audio recording by clicking the "Start" button. Clicking the "Stop" button halts the recording process.
- **Automatic Transcription:** After stopping the recording, the audio file is automatically sent to the application's backend for processing and transcription through integration with Google's Speech-to-Text API.
- **Transcription Display:** The transcribed text is then displayed to the user on the webpage.

## Tech Stack
- **Frontend:** Utilizes JavaScript for handling audio recording, initiating AJAX requests to the backend, and displaying the transcribed text to the user.
- **Backend:** Developed with Django, serving both as the web application framework and the RESTful API endpoint for processing audio transcription requests.
- **Audio Processing:** Leverages FFmpeg for audio file conversion and processing, ensuring compatibility with the Google Speech-to-Text API.
- **Speech-to-Text Conversion:** Employs Google Cloud's Speech-to-Text API for accurate and efficient transcription of audio content.
- **Deployment:** Hosted on Heroku, a platform for deploying and running the web application.

## Prerequisites
- Python 
- Django
- Google Cloud account for Speech-to-Text API access
- FFmpeg for audio processing

## Challenges & Solutions
**Limited Google API Quota**
- **Challenge:** The app operates within the constraints of the Google API's free tier as a temporary measure, serving as a demonstration of the project's capabilities.
- **Solution (Planned):** Future development efforts will focus on implementing open-source speech recognition technologies like PocketSphinx, including training the model with domain-specific data to improve accuracy and usability.
