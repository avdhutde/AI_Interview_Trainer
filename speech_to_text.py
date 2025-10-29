import speech_recognition as sr

def listen_and_transcribe(timeout=5, phrase_time_limit=8):
    r = sr.Recognizer()
    mic = sr.Microphone()
    print("Calibrating microphone for 1 second...")
    with mic as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Please speak now...")
        audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
    try:
        text = r.recognize_google(audio)
        print("Transcription:", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print("Could not request results; check internet:", e)
        return ""
