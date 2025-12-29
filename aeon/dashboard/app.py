import streamlit as st
import requests

st.title("ÆON Control Panel")

API = "http://localhost:8000"

st.header("Context")
emotion = st.text_input("Emotion")
intent = st.text_input("Intent")

if st.button("Update Context"):
    requests.post(f"{API}/context/update", json={
        "emotion": emotion,
        "intent": intent
    })

if st.button("Run Agent"):
    r = requests.post(f"{API}/agent/run")
    st.json(r.json())

st.header("System Health")
if st.button("Refresh"):
    r = requests.get(f"{API}/system/health")
    st.json(r.json())
