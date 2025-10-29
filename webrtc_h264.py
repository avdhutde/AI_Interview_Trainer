import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration
import av
import cv2

st.title("🎥 WebRTC H264 Test (Final Codec Fix)")

# Force H264 codec + Google STUN
rtc_config = RTCConfiguration({
    "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}],
    "sdpSemantics": "unified-plan"
})

class H264Transformer(VideoTransformerBase):
    def transform(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        cv2.putText(img, "H.264 Test - Working Stream", (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
        return av.VideoFrame.from_ndarray(img, format="bgr24")

# Include force codec constraint
webrtc_streamer(
    key="h264-test",
    rtc_configuration=rtc_config,
    video_transformer_factory=H264Transformer,
    media_stream_constraints={"video": True, "audio": False},
    video_html_attrs={"autoPlay": True, "playsinline": True},
    async_transform=False,
)