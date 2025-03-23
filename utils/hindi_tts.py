from gtts import gTTS
import os

def generate_hindi_tts(text, filename="hindi_speech.mp3"):
    """
    Converts the given text into Hindi speech dynamically.
    """

    tts = gTTS(text=text, lang="hi")
    tts.save(filename)
    
    return filename  # Return file path to be played


