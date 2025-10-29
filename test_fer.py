# test_fer.py
import cv2
from emotion_analysis import analyze_emotion

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("CAMERA FAIL")
    exit(1)

print("Camera opened. Press q to quit.")
while True:
    ret, frame = cap.read()
    if not ret:
        print("FRAME FAIL")
        break
    # convert to RGB because analyze_emotion expects RGB-like frame resizing
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    emo = analyze_emotion(rgb)
    print("Detected Emotion:", emo)
    cv2.imshow("test_fer - press q to quit", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
