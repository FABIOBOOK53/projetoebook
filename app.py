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
    .stApp { background-color: #FFFDD0; color: #1A1A1A; }
    h1, h2, h3, p, span, label, .stMarkdown { color: #1A1A1A !important; }
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
    .stButton>button:hover { background-color: #2E7D32 !important; color: #FFFFFF !important; }
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
    .stTextArea textarea { background-color: #FFFFFF !important; color: #1A1A1A !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. EXIBIÇÃO DO LOGO (NOME CORRIGIDO CONFORME GITHUB) ---
logo_nome = "LOGO2025NOME.jpg" # Nome exato que aparece no seu print do GitHub
try:
    if os.path.exists(logo_nome):
        st.image(Image.open(logo_nome), use_container_width=True)
    else:
        st.title("🐦‍⬛ FAMORTISCO AI")
        st.warning(f"Aviso: O arquivo '{logo_nome}' não foi detectado na raiz do repositório.")
except Exception as e:
    st.title("🐦‍⬛ FAMORTISCO AI")

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
    except:
        return False

# --- 4. FLUXO PRINCIPAL ---
st.markdown("### Procurar Arquivos")
arquivo = st.file_uploader("Suba seu manuscrito (PDF ou DOCX)", type=['pdf', 'docx'], label_visibility="collapsed")

if arquivo and api_key:
    try:
        texto_extraido = ""
        if arquivo.type == "application/pdf":
            reader = PdfReader(arquivo)
            for page in reader.pages[:10]:
                texto_extraido += page.extract_text() or ""
        else:
            doc = Document(arquivo)
            texto_extraido = "\n".join([p.text for p in doc.paragraphs[:100]])

        if st.button("🚀 GERAR MINHA ESTRATÉGIA"):
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={api_key}"
            prompt = f"Crie roteiros de Reels, ASMR e e-mail de vendas para: {texto_extraido[:3500]}"
            
            with st.spinner('Gerando...'):
                response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
                if response.status_code == 200:
                    st.session_state['resultado'] = response.json()['candidates'][0]['content']['parts'][0]['text']
                    st.success("Sucesso!")
                else:
                    st.error("Erro na IA.")

        if 'resultado' in st.session_state:
            st.info(st.session_state['resultado'])
            st.divider()
            c1, c2 = st.columns(2)
            with c1:
                email_dest = st.text_input("E-mail de destino:")
                if st.button("Disparar E-mail"):
                    if enviar_email(email_dest, st.session_state['resultado']):
                        st.success("Enviado!")
            with c2:
                num = st.text_input("WhatsApp:", value=meu_zap)
                if num:
                    link = f"https://api.whatsapp.com/send?phone={num}&text={urllib.parse.quote(st.session_state['resultado'][:1500])}"
                    st.link_button("Abrir WhatsApp", link)
    except Exception as e:
        st.error(f"Erro: {e}")
