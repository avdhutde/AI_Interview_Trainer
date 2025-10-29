# emotion_analysis.py — returns (emotion, confidence)
import cv2
import traceback
from collections import deque
import statistics

# ✅ Import DeepFace safely
try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
except Exception as e:
    DEEPFACE_AVAILABLE = False
    print("DeepFace import failed:", e)

def analyze_emotion(frame):
    """
    Input: RGB numpy array (H,W,3)
    Returns: (emotion_string, confidence_float)
    Uses DeepFace with a safe, compatible call (no model_name param).
    """
    try:
        if not DEEPFACE_AVAILABLE:
            return "DeepFace Not Available", 0.0

        # ↓ Downscale for faster analysis
        small = cv2.resize(frame, (320, 240))

        # Safe DeepFace call (avoid model_name if not supported)
        # Use detector_backend to speed up and be compatible across versions
        result = DeepFace.analyze(
            small,
            actions=["emotion"],
            enforce_detection=False,
            detector_backend="opencv"
        )

        if isinstance(result, list):
            result = result[0]

        # result may contain 'dominant_emotion' and 'emotion' dict
        dominant = None
        if isinstance(result, dict):
            dominant = result.get("dominant_emotion") or (result.get("emotion") and max(result.get("emotion"), key=result.get("emotion").get))
            probs = result.get("emotion") or {}
        else:
            # fallback: try common keys
            dominant = None
            probs = {}

        conf = 0.0
        if dominant and isinstance(probs, dict):
            conf = float(probs.get(dominant, 0.0)) if probs.get(dominant) is not None else 0.0

        if dominant:
            return str(dominant).capitalize(), round(conf, 3)
        else:
            return "Unknown", 0.0

    except Exception as e:
        print("DeepFace analyze error:", e)
        traceback.print_exc()
        return "Error", 0.0

# ✅ Emotion smoother
class EmotionSmoother:
    def __init__(self, window_size=5):
        self.history = deque(maxlen=window_size)

    def update(self, emotion, confidence):
        """Add new (emotion, confidence) pair"""
        if emotion not in ["Error", "Unknown", "DeepFace Not Available"]:
            # store a tuple
            self.history.append((emotion, confidence))

    def get_stable_emotion(self):
        """Return the most common emotion in recent frames as (emotion, avg_conf)"""
        if not self.history:
            return "No Data", 0.0
        emotions = [e for e, _ in self.history]
        most_common = max(set(emotions), key=emotions.count)
        avg_conf = statistics.mean([c for e, c in self.history if e == most_common])
        return most_common, round(avg_conf, 3)