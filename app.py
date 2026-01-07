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

# --- 1. CONFIGURAÇÃO DE TEMA: FUNDO CREME E ALTO CONTRASTE ---
st.set_page_config(page_title="FAMORTISCO AI", page_icon="🐦‍⬛", layout="centered")

st.markdown("""
    <style>
    /* Fundo da Tela em Creme */
    .stApp {
        background-color: #FFFDD0; 
        color: #1A1A1A; /* Texto em preto para leitura clara */
    }
    
    /* Títulos e Subtítulos */
    h1, h2, h3, p {
        color: #1A1A1A !important;
    }

    /* Estilização dos Botões (Azul Royal -> Verde Sucesso) */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #0047AB; /* Azul Royal para destaque no creme */
        color: #FFFFFF !important;
        border: none;
        font-weight: bold;
        padding: 12px;
        transition: 0.3s ease-in-out;
    }
    
    /* Mudança para Verde ao clicar ou passar o mouse */
    .stButton>button:hover, .stButton>button:active, .stButton>button:focus {
        background-color: #2E7D32 !important; 
        color: #FFFFFF !important;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
    }

    /* Botão do WhatsApp (Verde WhatsApp padrão) */
    div.stLinkButton > a {
        background-color: #25D366 !important;
        color: white !important;
        border-radius: 8px;
        text-align: center;
        text-decoration: none;
        display: block;
        padding: 12px;
        font-weight: bold;
        border: 1px solid #128C7E;
    }

    /* Inputs e Caixas de Texto com bordas visíveis */
    .stTextArea textarea, .stTextInput input {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
        border: 1px solid #CCCCCC !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. EXIBIÇÃO DO LOGO ---
logo_path = "LOGO2025NOME.JPG"
if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    st.image(logo, use_container_width=True)
else:
    st.title("🐦‍⬛ FAMORTISCO AI")

st.markdown("<h2 style='text-align: center;'>Estratégias de Marketing Literário</h2>", unsafe_allow_html=True)
st.markdown("---")

# --- 3. CONFIGURAÇÕES (SECRETS) ---
api_key = st.secrets.get("GOOGLE_API_KEY")
email_user = st.secrets.get("EMAIL_REMETENTE")
email_pass = st.secrets.get("EMAIL_SENHA")
meu_zap = st.secrets.get("MEU_WHATSAPP", "")

# Função de Envio de E-mail
def enviar_email(destino, conteudo):
    try:
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = destino
        msg['Subject'] = "📜 Sua Estratégia - FAMORTISCO AI"
        msg.attach(MIMEText(conteudo, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, email_pass)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Erro no portal de e-mail: {e}")
        return False

# --- 4. ÁREA DE TRABALHO ---
arquivo = st.file_uploader("Suba seu manuscrito (PDF ou DOCX)", type=['pdf', 'docx'])

if arquivo and api_key:
    try:
        # Extração de texto para PDF e DOCX
        if arquivo.type == "application/pdf":
            reader = PdfReader(arquivo)
            texto = "".join([p.extract_text() or "" for p in reader.pages[:10]])
        else:
            doc = Document(arquivo)
            texto = "\n".join([p.text for p in doc.paragraphs[:100]])

        if st.button("🚀 GERAR MINHA ESTRATÉGIA"):
            # Usando o modelo validado Gemini 3 Flash Preview
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={api_key}"
            prompt = f"Você é um estrategista literário sênior. Crie roteiros de Reels, ASMR e um e-mail de vendas para: {texto[:3500]}"
            
            with st.spinner('A IA está lendo sua alma... digo, seu livro...'):
                response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
                if response.status_code == 200:
                    st.session_state['resultado'] = response.json()['candidates'][0]['content']['parts'][0]['text']
                    st.success("Estratégia Invocada!")
                else:
                    st.error("Falha na conexão com a IA. Tente novamente.")

        # Resultados e Canais de Disparo
        if 'resultado' in st
