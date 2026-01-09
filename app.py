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

# ==============================
# 1. CONFIGURAÇÃO BÁSICA
# ==============================
st.set_page_config(
    page_title="FAMORTISCO AI",
    page_icon="🐦‍⬛",
    layout="centered"
)

# ==============================
# 2. CONTROLE DE USO (ANTI-ABUSO)
# ==============================
if "usos" not in st.session_state:
    st.session_state["usos"] = 0

LIMITE_DIARIO = 5

if st.session_state["usos"] >= LIMITE_DIARIO:
    st.error("Limite diário de uso atingido. Tente novamente amanhã.")
    st.stop()

# ==============================
# 3. CSS
# ==============================
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
# 4. LOGO
# ==============================
logo_nome = "LOGO2025NOME.jpg"
if os.path.exists(logo_nome):
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        st.image(Image.open(logo_nome), width=250)
else:
    st.title("🐦‍⬛ FAMORTISCO AI")

# ==============================
# 5. SECRETS
# ==============================
api_key = st.secrets.get("GOOGLE_API_KEY")
email_user = st.secrets.get("EMAIL_REMETENTE")
email_pass = st.secrets.get("EMAIL_SENHA")
meu_zap = st.secrets.get("MEU_WHATSAPP", "")

if not api_key:
    st.error("GOOGLE_API_KEY não encontrada nos Secrets.")
