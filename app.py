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

# --- 1. CONFIGURAÇÃO DE TEMA E CORES PERSONALIZADAS ---
st.set_page_config(page_title="FAMORTISCO AI", page_icon="🐦‍⬛", layout="centered")

# CSS para Fundo Cinza #262626 e Botões Azul -> Verde
st.markdown("""
    <style>
    /* Fundo da Tela */
    .stApp {
        background-color: #262626;
        color: #FFFFFF;
    }
    
    /* Estilização dos Botões Gerais (Azul que vira Verde) */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #007BFF; /* Azul */
        color: white;
        border: none;
        font-weight: bold;
        padding: 10px;
        transition: 0.4s;
    }
    
    .stButton>button:active, .stButton>button:focus, .stButton>button:hover {
        background-color: #28A745 !important; /* Verde ao clicar/focar */
        color: white !important;
    }

    /* Botão do WhatsApp (Verde por padrão) */
    div.stLinkButton > a {
        background-color: #25D366 !important;
        color: white !important;
        border-radius: 8px;
        text-align: center;
        text-decoration: none;
        display: block;
        padding: 10px;
        font-weight: bold;
    }

    /* Estilo para áreas de texto e inputs */
    .stTextArea textarea {
        background-color: #1A1A1A !important;
        color: #FFFFFF !important;
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

# Função de E-mail
def enviar_email(destino, conteudo):
    try:
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = destino
        msg['Subject'] = "📜 Estratégia de Marketing - FAMORTISCO AI"
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

# --- 4. INTERFACE ---
arquivo = st.file_uploader("Suba o arquivo do Ebook (PDF ou DOCX)", type=['pdf', 'docx'])

if arquivo and api_key:
    try:
        # Extração de texto
        if arquivo.type == "application/pdf":
            reader = PdfReader(arquivo)
            texto = "".join([p.extract_text() or "" for p in reader.pages[:10]])
        else:
            doc = Document(arquivo)
            texto = "\n".join([p.text for p in doc.paragraphs[:100]])

        if st.button("🚀 GERAR ESTRATÉGIA"):
            # Modelo validado Gemini 3 Flash Preview
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={api_key}"
            prompt = f"Crie roteiros de Reels, ASMR e e-mail de vendas para: {texto[:3500]}"
            
            with st.spinner('A IA está trabalhando...'):
                response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
                if response.status_code == 200:
                    st.session_state['resultado'] = response.json()['candidates'][0]['content']['parts'][0]['text']
                    st.success("Estratégia Gerada!")
                else:
                    st.error("Erro na API do Google.")

        if 'resultado' in st.session_state:
            st.markdown("### 🖋️ Resultado:")
            st.text_area("", st.session_state['resultado'], height=300)
            
            st.divider()
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📧 Enviar E-mail")
                email_dest = st.text_input("E-mail do cliente:")
                if st.button("Disparar E-mail"):
                    if enviar_email(email_dest, st.session_state['resultado']):
                        st.success("Enviado!")

            with col2:
                st.markdown("#### 🟢 Enviar WhatsApp")
                num_whats = st.text_input("Número (DDD):", value=meu_zap)
                if num_whats:
                    texto_url = urllib.parse.quote(st.session_state['resultado'][:1500])
                    link_zap = f"https://api.whatsapp.com/send?phone={num_whats}&text={texto_url}"
                    st.link_button("Abrir WhatsApp", link_zap)

    except Exception as e:
        st.error(f"Erro: {e}")
