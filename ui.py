import streamlit as st
from speech_to_text import listen_and_transcribe
from emotion_detection import run_camera
from feedback_generator import generate_feedback
import threading

st.title("AI Interview Trainer — Demo")

if st.button("Open Webcam (new window)"):
    st.warning("A separate OpenCV window will open. Press 'q' there to close it.")
    threading.Thread(target=run_camera, daemon=True).start()

st.write("---")
st.write("Click below to record a short answer (Google Speech API, needs internet).")

if st.button("Record & Transcribe (8s max)"):
    with st.spinner("Listening..."):
        text = listen_and_transcribe(timeout=5, phrase_time_limit=8)
    st.subheader("Transcript")
    st.write(text)
    st.subheader("Feedback")
    st.write(generate_feedback(text))
