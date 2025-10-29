import cv2
import mediapipe as mp

mp_face = mp.solutions.face_detection
mp_draw = mp.solutions.drawing_utils

def run_camera(show_window=True):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam.")
    with mp_face.FaceDetection(model_selection=0, min_detection_confidence=0.5) as detector:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = detector.process(rgb)
            if results.detections:
                for det in results.detections:
                    mp_draw.draw_detection(frame, det)
            if show_window:
                cv2.imshow("Webcam (press q to quit)", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_camera()
