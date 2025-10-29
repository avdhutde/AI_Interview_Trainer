import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration
import av
import cv2

st.title("🧩 WebRTC Safe Mode Test")

rtc_config = RTCConfiguration({
    "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
})

class SafeTransformer(VideoTransformerBase):
    def transform(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        cv2.rectangle(img, (100, 100), (300, 300), (0, 255, 0), 3)
        cv2.putText(img, "SAFE MODE", (120, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
        return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_streamer(
    key="safe",
    rtc_configuration=rtc_config,
    video_transformer_factory=SafeTransformer,
    async_transform=False,
    media_stream_constraints={"video": True, "audio": False},
    video_html_attrs={"controls": True, "autoPlay": True},
)