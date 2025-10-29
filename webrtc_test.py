import streamlit as st
from streamlit_webrtc import webrtc_streamer

st.title("webrtc minimal test")
st.write("This shows only the raw browser camera via WebRTC - no Python processing.")
webrtc_streamer(key="test", media_stream_constraints={"video": True, "audio": False})
