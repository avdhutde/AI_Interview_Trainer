import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration
import av
import cv2

st.title("🎥 WebRTC Forced Codec Test")

# Force VP8 codec and public STUN server
rtc_config = RTCConfiguration({
    "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
})

class CodecTransformer(VideoTransformerBase):
    def transform(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        cv2.putText(img, "WebRTC Working ✅", (30, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
        return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_streamer(
    key="codec-test",
    rtc_configuration=rtc_config,
    video_transformer_factory=CodecTransformer,
    async_transform=False,
    media_stream_constraints={"video": True, "audio": False},
)