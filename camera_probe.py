import cv2
import time

backends = [
    cv2.CAP_DSHOW,  # DirectShow (Windows)
    cv2.CAP_MSMF,   # Media Foundation (Windows)
    cv2.CAP_V4L2,   # Linux (harmless on Windows)
    cv2.CAP_ANY
]

def try_open(index, backend):
    cap = cv2.VideoCapture(index, backend)
    ok = cap.isOpened()
    info = None
    if ok:
        ret, frame = cap.read()
        if ret and frame is not None:
            info = f"read OK shape={frame.shape}"
        else:
            info = "opened but read failed"
        cap.release()
    return ok, info

for backend in backends:
    print('=== backend:', backend, '===')
    for i in range(0, 6):  # check indices 0..5
        ok, info = try_open(i, backend)
        print(f'index {i}: opened={ok} ; {info}')
    print()
print('Done.')
