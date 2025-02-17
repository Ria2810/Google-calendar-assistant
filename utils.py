from gtts import gTTS
import os
import base64
import streamlit as st
import openai
import re
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def speech_to_text(audio_data):
    with open(audio_data, "rb") as audio_file:
        try:
            # Attempt to transcribe the audio
            transcript = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file,
                response_format="json"  # Change from "text" to "json" for debugging
            )

            print("Full API Response:", transcript)  # Print full response
            if isinstance(transcript, dict) and "text" in transcript:
                return transcript["text"]
            else:
                print("Unexpected response format:", transcript)
                return None
        
        except Exception as e:
            print(f"An error occurred during transcription: {e}")
            return None

