# speech_analysis.py
import speech_recognition as sr
from textblob import TextBlob

def record_and_analyze(duration=5):
    """
    Record from microphone for ~duration seconds and return (text, mood).
    mood: 'Positive' / 'Neutral' / 'Negative' or 'Error: ...'
    """
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.8)
            print(f"Listening for {duration} seconds...")
            audio = recognizer.listen(source, phrase_time_limit=duration)
    except Exception as e:
        return None, f"Error: {e}"

    try:
        text = recognizer.recognize_google(audio)
        polarity = TextBlob(text).sentiment.polarity
        mood = "Positive" if polarity > 0 else "Negative" if polarity < 0 else "Neutral"
        return text, mood
    except Exception as e:
        return None, f"Error: {e}"
