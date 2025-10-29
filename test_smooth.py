# test_smooth.py
import cv2
from emotion_analysis import analyze_emotion, EmotionSmoother

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("CAMERA FAIL")
    exit(1)

smoother = EmotionSmoother(window_size=5)
print("Camera open. Press q to quit.")
while True:
    ret, frame = cap.read()
    if not ret:
        break
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    emo, conf = analyze_emotion(rgb)
    smoother.update(emo, conf)
    stable_emo, avg_conf = smoother.get_stable_emotion()
    print(f"Frame: {emo} ({conf}) | Stable: {stable_emo} ({avg_conf})")
    cv2.imshow("Stable Emotion Test", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()