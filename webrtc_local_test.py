import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import av
import cv2

st.set_page_config(page_title="WebRTC Local Camera Test", layout="centered")
st.title("🧪 Local WebRTC Camera Test")

class Identity(VideoTransformerBase):
    def transform(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        h, w = img.shape[:2]
        cv2.putText(img, "✅ Camera Working", (30, h//2),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)
        return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_streamer(
    key="local-test",
    video_transformer_factory=Identity,
    rtc_configuration={},  # LOCAL only
    media_stream_constraints={"video": True, "audio": False},
    async_transform=False
)