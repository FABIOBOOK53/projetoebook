Python
import streamlit as st
import requests
from PyPDF2 import PdfReader
from docx import Document
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import urllib.parse
from PIL import Image

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="FAMORTISCO AI", page_icon="📜", layout="wide")

# CSS para manter a identidade visual Dark/Gótica
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        background-color: #721c24;
        color: white;
        border: 1px solid #f8d7da;
    }
    div.stLinkButton > a {
        background-color: #25D366 !important;
        color: white !important;
        border-radius: 5px;
        text-align: center;
        display: block;
        padding: 0.5em;
        text-decoration: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- EXIBIÇÃO DO LOGO ---
# Certifique-se de que o arquivo 'logo.jpg' esteja no seu GitHub junto com o app.py
try:
    logotipo = Image.open("LOGO 2025 NOME.jpg")
    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        st.image(logotipo, use_container_width=True)
except:
    st.title("📜 FAMORTISCO AI")

st.markdown("<h3 style='text-align: center;'>Estratégias de Marketing para Dark Fiction</h3>", unsafe_allow_html=True)

# --- CONFIGURAÇÕES ---
api_key = st.secrets.get("GOOGLE_API_KEY")
email_user = st.secrets.get("EMAIL_REMETENTE")
email_pass = st.secrets.get("EMAIL_SENHA")
meu_zap = st.secrets.get("MEU_WHATSAPP", "")

# --- FUNÇÃO DE E-MAIL ---
def enviar_email(destino, conteudo):
    try:
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = destino
        msg['Subject'] = "🔥 Estratégia de Redenção - FAMORTISCO AI"
        msg.attach(MIMEText(conteudo, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, email_pass)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Erro no envio: {e}")
        return False

# --- PROCESSO PRINCIPAL ---
file = st.file_uploader("Suba seu manuscrito (PDF ou DOCX)", type=['pdf', 'docx'])

if file and api_key:
    try:
        if file.type == "application/pdf":
            reader = PdfReader(file)
            texto = "".join([p.extract_text() or "" for p in reader.pages[:10]])
        else:
            doc = Document(file)
            texto = "\n".join([p.text for p in doc.paragraphs[:100]])

        if st.button("🚀 GERAR ESTRATÉGIA LITERÁRIA"):
            # Usando o modelo validado no seu chat: Gemini 3 Flash Preview
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={api_key}"
            prompt = f"Você é um estrategista gótico de marketing. Crie roteiros de ASMR, Reels e um e-mail de vendas para este conteúdo: {texto[:3500]}"
            
            with st.spinner('Consumindo a escuridão para criar sua estratégia...'):
                response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
                if response.status_code == 200:
                    st.session_state['resultado'] = response.json()['candidates'][0]['content']['parts'][0]['text']
                    st.balloons()
                else:
                    st.error("Ocorreu um erro na conexão com a IA.")

        if 'resultado' in st.session_state:
            st.markdown("### 🖋️ Resultado da Análise")
            st.info(st.session_state['resultado'])
            
            st.divider()
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**E-mail Profissional**")
                dest = st.text_input("Enviar para:", placeholder="email@exemplo.com")
                if st.button("📧 Enviar Estratégia"):
                    if enviar_email(dest, st.session_state['resultado']):
                        st.success("Enviado com sucesso!")
            
            with c2:
                st.markdown("**WhatsApp Direto**")
                num = st.text_input("Número (DDD):", value=meu_zap)
                if num:
                    resumo = st.session_state['resultado'][:1500]
                    link = f"https://api.whatsapp.com/send?phone={num}&text={urllib.parse.quote('*🚀 FAMORTISCO AI:* ' + resumo)}"
                    st.link_button("🟢 Abrir no WhatsApp", link)

    except Exception as e:
        st.error(f"Erro técnico: {e}")
