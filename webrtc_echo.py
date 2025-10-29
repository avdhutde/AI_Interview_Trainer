import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import av
import cv2

st.title("🔁 WebRTC Echo Test (Async Mode)")
st.write("If this works, you should see your live video feed with a green line drawn across it.")

class EchoTransformer(VideoTransformerBase):
    async def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        # draw a line so we can tell the frame is processed
        cv2.line(img, (0, 200), (640, 200), (0, 255, 0), 3)
        return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_streamer(
    key="echo",
    video_transformer_factory=EchoTransformer,
    async_transform=True,
    media_stream_constraints={"video": True, "audio": False},
)