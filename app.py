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
# 1. CONFIGURAÇÃO DE TEMA
# ==============================
st.set_page_config(
    page_title="FAMORTISCO AI",
    page_icon="🐦‍⬛",
    layout="centered"
)

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
div.stLinkButton > a {
    background-color: #25D366 !important;
    color: white !important;
    border-radius: 8px;
    text-align: center;
    display: block;
    padding: 12px;
    font-weight: bold;
    text-decoration: none;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# 2. LOGO
# ==============================
logo_nome = "LOGO2025NOME.jpg"
if os.path.exists(logo_nome):
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        st.image(Image.open(logo_nome), width=250)
else:
    st.title("🐦‍⬛ FAMORTISCO AI")

# ==============================
# 3. SECRETS
# ==============================
api_key = st.secrets.get("GOOGLE_API_KEY")
email_user = st.secrets.get("EMAIL_REMETENTE")
email_pass = st.secrets.get("EMAIL_SENHA")
meu_zap = st.secrets.get("MEU_WHATSAPP", "")

# ==============================
# 4. FUNÇÕES AUXILIARES
# ==============================
def enviar_email(destino, conteudo):
    try:
        msg = MIMEMultipart()
        msg["From"] = email_user
        msg["To"] = destino
        msg["Subject"] = "📜 Estratégia Gerada - FAMORTISCO AI"
        msg.attach(MIMEText(conteudo, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email_user, email_pass)
        server.send_message(msg)
        server.quit()
        return True
    except:
        return False


def extrair_frames(video_path, intervalo=3, limite=5):
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 24
    frames = []
    contador = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if contador % (fps * intervalo)*
