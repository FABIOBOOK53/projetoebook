import streamlit as st
import requests
from PyPDF2 import PdfReader
from docx import Document
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import urllib.parse
from PIL import Image
import os
import mimetypes
import tempfile
import cv2
import whisper
from moviepy.editor import VideoFileClip

# ==============================
# CONFIGURAÇÃO
# ==============================
st.set_page_config(page_title="FAMORTISCO AI", page_icon="🐦‍⬛", layout="centered")

st.markdown("""
<style>
.stApp { background-color: #FFFDD0; color: #1A1A1A; }
h1, h2, h3, p, span, label { color: #1A1A1A !important; }
.stButton>button {
    width: 100%;
    border-radius: 8px;
    background-color: #0047AB;
    color: white !important;
    font-weight: bold;
    padding: 12px;
    border: none;
}
.stButton>button:hover { background-color: #2E7D32 !important; }
</style>
""", unsafe_allow_html=True)

# ==============================
# LOGO
# ==============================
logo_nome = "LOGO2025NOME.jpg"
if os.path.exists(logo_nome):
    st.image(Image.open(logo_nome), width=250)
else:
    st.title("🐦‍⬛ FAMORTISCO AI")

# ==============================
# SECRETS
# ==============================
api_key = st.secrets.get("GOOGLE_API_KEY")

# ==============================
# FUNÇÕES
# ==============================
def extrair_frames(video_path, intervalo=3, limite=5):
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 24
    frames = []
    contador = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if contador % (fps * intervalo) == 0:
            frames.append(frame)

        contador += 1

    cap.release()
    return frames[:limite]


def transcrever_audio(video_path):
    model = whisper.load_model("base")
    with tempfile.Named
