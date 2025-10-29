from textblob import TextBlob

def generate_feedback(transcript):
    if not transcript.strip():
        return "No speech detected - please try again."
    blob = TextBlob(transcript)
    polarity = blob.sentiment.polarity
    if polarity > 0.3:
        tone, advice = "Positive", "Keep the confident tone. Add more examples."
    elif polarity < -0.2:
        tone, advice = "Negative", "Try to sound more optimistic."
    else:
        tone, advice = "Neutral", "Good neutral tone; add enthusiasm for impact."
    length = len(transcript.split())
    if length < 5:
        extra = "Answer is short — expand a bit."
    elif length > 80:
        extra = "Answer is long — make it concise."
    else:
        extra = "Answer length looks fine."
    return f"Tone: {tone}\nAdvice: {advice}\n{extra}\n\nTranscript: {transcript}"
