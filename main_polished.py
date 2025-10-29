# main_polished.py — AI Virtual Interview Trainer (Safe Mode, polished)
import streamlit as st
import cv2
from PIL import Image
import numpy as np
import time
from collections import deque

# import your modules (must exist in project)
from emotion_analysis import analyze_emotion, EmotionSmoother
from speech_analysis import record_and_analyze

# -----------------------
# Helpers
# -----------------------
def short_feedback(emotion: str):
    """Return a short training tip for common emotions."""
    tips = {
        "Happy": "Good: keep smiling naturally. Maintain eye contact.",
        "Neutral": "Neutral is safe—add slight enthusiasm with voice variation.",
        "Sad": "Try to raise your chin slightly and smile gently.",
        "Angry": "Relax shoulders, breathe slowly before answering.",
        "Surprise": "Control sudden gasps — pause and speak steadily.",
        "Fear": "Take a slow breath, speak clearly, and slow down.",
        "Disgust": "Neutralize facial tension; focus on calm breathing.",
        "Contempt": "Keep expressions neutral and professional.",
        "Unknown": "No clear emotion detected — reposition camera or light.",
        "Error": "Analysis error — try single capture again."
    }
    return tips.get(emotion, "Be calm, steady, and confident.")

# -----------------------
# Page setup
# -----------------------
st.set_page_config(page_title="AI Virtual Interview Trainer (Polished)", layout="wide")
st.title("🎯 AI Virtual Interview Trainer — Polished Safe Mode")
st.write("Stable demo using browser camera input / OpenCV pseudo-live — history, confidence, and feedback")

# initialize session state
if "history" not in st.session_state:
    # store tuples (timestamp, emotion, confidence)
    st.session_state.history = deque(maxlen=60)
if "smoother" not in st.session_state:
    st.session_state.smoother = EmotionSmoother(window_size=5)
if "auto_running" not in st.session_state:
    st.session_state.auto_running = False
if "cap" not in st.session_state:
    st.session_state.cap = None

# layout
col_left, col_right = st.columns([2, 1])

# -----------------------
# Left column: camera + capture
# -----------------------
with col_left:
    st.header("📸 Camera & Emotion Detection")

    # Single capture via browser (optional)
    camera_file = st.camera_input("Capture Image (click button below camera)")

    if camera_file is not None:
        img = Image.open(camera_file).convert("RGB")
        img_array = np.array(img)
        try:
            result = analyze_emotion(img_array)
            if isinstance(result, tuple):
                emo, conf = result
            else:
                emo, conf = result, 0.0
        except Exception as e:
            emo, conf = "Error", 0.0
            st.error(f"Emotion analysis failed: {e}")

        st.image(img, caption=f"Detected Emotion: {emo} ({conf})", use_column_width=True)
        # add to history
        st.session_state.history.append((time.time(), emo, float(conf)))
        st.session_state.smoother.update(emo, float(conf))

    st.write("---")
    st.subheader("🔁 Auto Capture (OpenCV single preview)")
    st.caption("This opens the webcam once and updates a single live preview. Use Stop to end.")

    interval = st.number_input("Capture interval (seconds):", min_value=0.5, max_value=5.0, value=1.5, step=0.5, format="%.1f")
    start_col, stop_col = st.columns(2)
    with start_col:
        if st.button("▶️ Start Auto Capture"):
            # start camera
            st.session_state.auto_running = True
            # ensure old capture is released before starting
            try:
                if st.session_state.cap is not None:
                    st.session_state.cap.release()
            except Exception:
                pass
    with stop_col:
        if st.button("⏹ Stop Auto Capture"):
            st.session_state.auto_running = False

    # placeholders for single live preview + status
    live_placeholder = st.empty()
    status_placeholder = st.empty()

    # Auto-capture: open camera and update single placeholder
    if st.session_state.auto_running:
        status_placeholder.info("Opening camera... If nothing appears, close other apps using the camera.")
        # open capture if not already
        if st.session_state.cap is None:
            # Try DirectShow (Windows) first
            try:
                cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                if not cap.isOpened():
                    cap = cv2.VideoCapture(0)  # fallback
            except Exception:
                cap = cv2.VideoCapture(0)
            st.session_state.cap = cap

        cap = st.session_state.cap
        if not cap.isOpened():
            status_placeholder.error("Cannot open camera. Close other apps using camera and click Start again.")
            st.session_state.auto_running = False
            # ensure release
            try:
                cap.release()
            except Exception:
                pass
            st.session_state.cap = None
        else:
            smoother = st.session_state.smoother
            try:
                # capture loop (will stop when auto_running set False)
                while st.session_state.auto_running:
                    ret, frame = cap.read()
                    if not ret or frame is None:
                        status_placeholder.error("Frame read failed (camera returned no frame).")
                        break

                    # convert to RGB for display + analysis
                    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    # analyze (safe)
                    try:
                        result = analyze_emotion(rgb)
                        if isinstance(result, tuple):
                            emo, conf = result
                        else:
                            emo, conf = result, 0.0
                    except Exception as e:
                        emo, conf = "Error", 0.0

                    # update smoother and history
                    try:
                        smoother.update(emo, float(conf))
                        stable = smoother.get_stable_emotion()
                        if isinstance(stable, tuple):
                            stable_label, stable_conf = stable
                        else:
                            stable_label, stable_conf = stable, 0.0
                    except Exception:
                        stable_label, stable_conf = emo, conf

                    st.session_state.history.append((time.time(), emo, float(conf)))

                    # update single preview and status
                    live_placeholder.image(rgb, caption=f"Detected: {emo} ({conf}) — Stable: {stable_label} ({stable_conf})", use_column_width=True)
                    status_placeholder.info(f"Auto capture running — stable: {stable_label} ({stable_conf})")

                    # control rate
                    time.sleep(float(interval))

            finally:
                # release resources on stop/exception
                try:
                    cap.release()
                except Exception:
                    pass
                st.session_state.cap = None
                st.session_state.auto_running = False
                status_placeholder.info("Auto capture stopped. Click Start to run again.")

# -----------------------
# Right column: history, chart, feedback, speech
# -----------------------
with col_right:
    st.header("📊 Emotion History & Feedback")

    # Show last N history
    hist = list(st.session_state.history)
    if hist:
        # show last 6 entries
        recent = hist[-6:]
        rows = []
        for ts, emo, conf in reversed(recent):
            rows.append(f"{time.strftime('%H:%M:%S', time.localtime(ts))} — {emo} ({conf})")
        st.write("Recent detections:")
        for r in rows:
            st.write("- " + r)

        # Show tiny chart of confidences for last entries
        times = [i for i in range(len(hist))]
        confidences = [h[2] for h in hist]
        # convert confidences to numeric (safe)
        try:
            confidences_num = [float(c) for c in confidences]
        except Exception:
            confidences_num = [0.0 for _ in confidences]

        st.line_chart({"confidence": confidences_num})
    else:
        st.info("No detections yet — capture a frame or start auto-capture.")

    st.write("---")
    st.subheader("💡 Feedback")
    # Use last stable emotion for feedback
    stable = st.session_state.smoother.get_stable_emotion()
    if isinstance(stable, tuple):
        label, conf_avg = stable
        st.write(f"**Stable emotion:** {label} — avg confidence {conf_avg}")
        st.info(short_feedback(label))
    else:
        st.write(f"**Stable emotion:** {stable}")
        st.info("Perform a few captures to get feedback.")

    st.write("---")
    st.subheader("🎙 Speech Sentiment")
    if st.button("Record & Analyze Speech"):
        with st.spinner("Listening for 5 seconds..."):
            text, sentiment = record_and_analyze()
        if text:
            st.success(f"🗣 You said: {text}")
            st.info(f"💬 Sentiment: *{sentiment}*")
        else:
            st.error(sentiment)

# -----------------------
# Footer
# -----------------------
st.write("---")
st.caption("Polished Safe Mode — reliable for demos. To add true live overlay via WebRTC we'd test further after demo.")