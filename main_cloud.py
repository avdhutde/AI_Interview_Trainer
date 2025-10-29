import streamlit as st
import cv2
from PIL import Image
import numpy as np

st.set_page_config(page_title="AI Interview Trainer (Lite)", layout="wide")
st.title("🎯 AI Interview Trainer — Cloud Demo (Lite Version)")

col1, col2 = st.columns(2)

with col1:
    st.header("📸 Facial Emotion Detection (Demo)")
    if st.button("Capture Frame"):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        if not ret:
            st.error("❌ Could not access webcam.")
        else:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            st.image(img, caption="Frame Captured!", use_container_width=True)
            st.info("Emotion analysis disabled in cloud demo (for performance).")

with col2:
    st.header("💬 Speech Sentiment (Placeholder)")
    st.write("Speech recording is disabled in Streamlit Cloud demo environment.")

st.caption("⚙️ Local version supports full emotion + audio features.")