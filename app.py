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

# --- 1. CONFIGURAÇÃO DE TEMA: CREME E ALTO CONTRASTE ---
st.set_page_config(page_title="FAMORTISCO AI", page_icon="🐦‍⬛", layout="centered")

st.markdown("""
    <style>
    /* Fundo Creme */
    .stApp {
        background-color: #FFFDD0; 
        color: #1A1A1A;
    }
    h1, h2, h3, p, span, label, .stMarkdown {
        color: #1A1A1A !important;
    }
    /* Botão Azul Royal que vira Verde no Hover */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #0047AB;
        color: #FFFFFF !important;
        border: none;
        font-weight: bold;
        padding: 12px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #2E7D32 !important;
        color: #FFFFFF !important;
    }
    /* Estilização do Botão de WhatsApp */
    div.stLinkButton > a {
        background-color: #25D366 !important;
        color: white !important;
        border-radius: 8px;
        text-align: center;
        display: block;
        padding: 12px;
        font-weight: bold;
        text-decoration: none;
        border: 1px solid #128C7E;
    }
    .stTextArea textarea {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. EXIBIÇÃO DO LOGO (CORRIGIDO) ---
# O nome abaixo deve ser IDÊNTICO ao arquivo no GitHub
logo_path = "LOGO 2025 NOME.jpg" 
if os.path.exists(logo_path):
    st.image(Image.open(logo_path), use_container_width=True)
else:
    st.title("🐦‍⬛ FAMORTISCO AI")
    st.error(f"Erro: O arquivo '{logo_path}' não foi encontrado no repositório.")

# --- 3. CONFIGURAÇÕES (SECRETS) ---
api_key = st.secrets.get("GOOGLE_API_KEY")
email_user = st.secrets.get("EMAIL_REMETENTE")
email_pass = st.secrets.get("EMAIL_SENHA")
meu_zap = st.secrets.get("MEU_WHATSAPP", "")

def enviar_email(destino, conteudo):
    try:
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = destino
        msg['Subject'] = "📜 Estratégia Literária - FAMORTISCO AI"
        msg.attach(MIMEText(conteudo, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, email_pass)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Erro no e-mail: {e}")
        return False

# --- 4. FLUXO PRINCIPAL ---
# Texto do botão alterado conforme solicitado
arquivo = st.file_uploader("Suba seu manuscrito (PDF ou DOCX)", type=['pdf', 'docx'], label_visibility="visible")

# Nota: O Streamlit traduz o botão nativo do uploader automaticamente 
# para "Browse files" ou "Procurar arquivos" dependendo do navegador, 
# mas forçamos o label acima para clareza.

if arquivo and api_key:
    try:
        if arquivo.type == "application/pdf":
            reader = PdfReader(arquivo)
            texto = "".join([p.extract_text() or "" for p in reader.pages[:10]])
        else:
            doc = Document(arquivo)
            texto
