# main.py — AI Virtual Interview Trainer (camera_input, safe + working)
import streamlit as st
import cv2
from PIL import Image
import numpy as np
from emotion_analysis import analyze_emotion, EmotionSmoother
from speech_analysis import record_and_analyze
import time

# Page setup
st.set_page_config(page_title="AI Virtual Interview Trainer", layout="wide")
st.title("🎯 AI Virtual Interview Trainer — Safe Mode (camera_input)")
st.write("*Phase 2+ — Emotion (Single + Pseudo-Live) and Speech Sentiment*")

col1, col2 = st.columns(2)

# ---------------- Single-frame capture (works reliably)
with col1:
    st.header("👀 Facial Emotion Detection (Single Frame)")
    if st.button("Capture Frame & Analyze Emotion"):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        if not ret or frame is None:
            st.error("❌ Could not access webcam. Make sure camera is free and allowed.")
        else:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            try:
                result = analyze_emotion(frame_rgb)
                if isinstance(result, tuple):
                    emo, conf = result
                else:
                    emo, conf = result, 0.0
            except Exception as e:
                emo, conf = "Error", 0.0
                print("Single-frame analyze error:", e)

            img = Image.fromarray(frame_rgb)
            st.image(img, caption=f"Detected Emotion: {emo} ({conf})", use_container_width=True)

# ---------------- Speech sentiment (unchanged)
with col2:
    st.header("🎙 Speech Sentiment Analysis")
    if st.button("Record & Analyze Speech"):
        with st.spinner("Listening for 5 seconds..."):
            text, sentiment = record_and_analyze()
        if text:
            st.success(f"🗣 You said: {text}")
            st.info(f"💬 Sentiment: *{sentiment}*")
        else:
            st.error(sentiment)

st.write("---")
st.caption("Below is a safe *pseudo-live* mode using the browser camera input (no WebRTC).")

# ---------------- Pseudo-live using st.camera_input + smoothing ----------------
st.write("### 📹 Pseudo-Live Camera (press Capture repeatedly or Auto mode)")

if "pseudo_running" not in st.session_state:
    st.session_state.pseudo_running = False
if "smoother" not in st.session_state:
    st.session_state.smoother = EmotionSmoother(window_size=5)

cols = st.columns([1, 1, 1])
with cols[0]:
    start = st.button("Start Auto Capture")
with cols[1]:
    stop = st.button("Stop Auto Capture")
with cols[2]:
    one_shot = st.button("Capture Now")

# camera_input widget (returns an uploaded file-like object)
camera_file = st.camera_input("Point your camera at your face and capture a frame here")

# Start / Stop logic
if start:
    st.session_state.pseudo_running = True
    st.experimental_rerun()

if stop:
    st.session_state.pseudo_running = False
    st.experimental_rerun()

# If user clicked Capture Now, analyze camera_file immediately
if one_shot and camera_file is not None:
    img = Image.open(camera_file).convert("RGB")
    arr = np.array(img)
    result = analyze_emotion(arr)
    if isinstance(result, tuple):
        emo, conf = result
    else:
        emo, conf = result, 0.0
    st.success(f"Captured Emotion: {emo} ({conf})")
    # update smoother
    st.session_state.smoother.update(emo, float(conf))

# Auto-capture loop: capture every ~1.5s while pseudo_running True
# (We simulate a live view: the user must allow camera_input and stay on page.)
if st.session_state.pseudo_running:
    st.write("Auto capture running — capturing every 1.5s. Click Stop to end.")
    # If no camera_file yet, show camera_input prompt and wait
    if camera_file is None:
        st.info("Please click the camera capture button (the camera_input widget) to allow the browser camera.")
    else:
        # analyze this captured camera_file
        img = Image.open(camera_file).convert("RGB")
        arr = np.array(img)
        result = analyze_emotion(arr)
        if isinstance(result, tuple):
            emo, conf = result
        else:
            emo, conf = result, 0.0
        st.session_state.smoother.update(emo, float(conf))
        stable = st.session_state.smoother.get_stable_emotion()
        if isinstance(stable, tuple):
            label, conf_avg = stable
            st.success(f"Stable Emotion: {label} ({conf_avg})")
        else:
            st.info(f"Stable Emotion: {stable}")

        # Show current frame
        st.image(img, caption=f"Captured (auto): {emo} ({conf})", use_container_width=True)

        # Small pause so UI doesn't freeze; then rerun to re-capture via camera_input
        time.sleep(1.5)
        st.experimental_rerun()

# If not running auto-mode, show last stable result if present
if not st.session_state.pseudo_running:
    stable = st.session_state.smoother.get_stable_emotion()
    if isinstance(stable, tuple):
        st.info(f"Last stable emotion: {stable[0]} ({stable[1]})")
    else:
        st.info(f"Last stable emotion: {stable}")

st.write("---")
st.caption("This mode is intentionally simple and reliable for demos — no WebRTC required.")