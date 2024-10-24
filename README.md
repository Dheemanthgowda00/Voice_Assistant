# Voice_Assistant

## Overview
This is a simple voice assistant project that listens for the hotword "Alexa" and responds to various commands. It can:
- Play a song on YouTube.
- Provide the current time.
- Give a short summary of a person from Wikipedia.
- Tell a joke.
- Perform web searches.

The assistant uses:
- **SpeechRecognition** for converting speech to text.
- **Pyttsx3** for text-to-speech functionality.
- **PyWhatKit** to interact with YouTube and Google search.
- **Wikipedia API** to fetch summaries of people.
- **PyJokes** for generating jokes.

## Features
- **Hotword Detection**: The assistant waits for the user to say "Alexa" before listening to commands.
- **Natural Speech Recognition**: Recognizes and processes natural language commands.
- **Multifunctionality**: Can play music, tell the time, give information about famous people, search the web, and tell jokes.
- **Voice Output**: Responds audibly to user commands using text-to-speech.

## Requirements

- Python 3.x
- SpeechRecognition (`speech_recognition`)
- Pyttsx3 (`pyttsx3`)
- PyWhatKit (`pywhatkit`)
- Wikipedia (`wikipedia-api`)
- PyJokes (`pyjokes`)
