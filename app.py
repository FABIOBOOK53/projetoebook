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

# --- 1. CONFIGURAÇÃO DE TEMA E IDIOMA ---
# Adicionamos 'lang="pt-br"' no HTML para evitar traduções automáticas do navegador
st.set_page_config(page_title="FAMORTISCO AI", page_icon="🐦‍⬛", layout="centered")

st.markdown("""
    <html lang="pt-br">
    <style>
    .stApp { background-color: #FFFDD0; color: #1A1A1A; }
    h1, h2, h3, p, span, label { color: #1A1A1A !important; }
    
    /* Botões: Azul Royal que vira Verde */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #0047AB;
        color: white !important;
        font-weight: bold;
        padding: 12px;
        transition: 0.3s;
        border: none;
    }
    .stButton>button:hover { background-color: #2E7D32 !important; }
    
    /* Botão WhatsApp */
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
    </html>
    """, unsafe_allow_html=True)

# --- 2. EXIBIÇÃO DO LOGO ---
logo_nome = "LOGO2025NOME.jpg"
if os.path.exists(logo_nome):
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.image(Image.open(logo_nome), width=300)
else:
    st.title("🐦‍⬛ FAMORTISCO AI")

# --- 3. CONFIGURAÇÕES E FUNÇÕES ---
api_key = st.secrets.get("GOOGLE_API_KEY")
email_user = st.secrets.get("EMAIL_REMETENTE")
email_pass = st.secrets.get("EMAIL_SENHA")
meu_zap = st.secrets.get("MEU_WHATSAPP", "")

def enviar_email(destino, conteudo):
    try:
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = destino
        msg['Subject'] = "📜 Sua Estratégia Literária - FAMORTISCO AI"
        msg.attach(MIMEText(conteudo, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, email_pass)
        server.send_message(msg)
        server.quit()
        return True
    except:
        return False

# --- 4. INTERFACE TOTALMENTE EM PORTUGUÊS ---
st.markdown("### Procurar Arquivos")
# O label do uploader é o que aparece para o usuário
arquivo = st.file_uploader("Arraste ou selecione seu manuscrito (PDF ou DOCX)", type=['pdf', 'docx'], label_visibility="collapsed")

if arquivo and api_key:
    try:
        texto_ext = ""
        if arquivo.type == "application/pdf":
            reader = PdfReader(arquivo)
            for page in reader.pages[:10]:
                texto_ext += page.extract_text() or ""
        else:
            doc = Document(arquivo)
            texto_ext = "\n".join([p.text for p in doc.paragraphs[:100]])

        if st.button("🚀 GERAR MINHA ESTRATÉGIA"):
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={api_key}"
            prompt = f"Crie roteiros de Reels, ASMR e e-mail de vendas para: {texto_ext[:3500]}"
            
            with st.spinner('A IA está analisando seu livro...'):
                resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
                if resp.status_code == 200:
                    st.session_state['resultado'] = resp.json()['candidates'][0]['content']['parts'][0]['text']
                    st.success("Estratégia Gerada!")
                else:
                    st.error("Erro na IA. Verifique sua chave.")

        if 'resultado' in st.session_state:
            st.markdown("### 🖋️ O Plano Mestre:")
            st.info(st.session_state['resultado'])
            
            st.divider()
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### 📧 Enviar por E-mail")
                dest = st.text_input("E-mail do autor:")
                if st.button("Disparar E-mail"):
                    if enviar_email(dest, st.session_state['resultado']):
                        st.success("Enviado com sucesso!")
            
            with c2:
                st.markdown("#### 🟢 Enviar por WhatsApp")
                num = st.text_input("Número (com DDD):", value=meu_zap)
                if num:
                    resumo = f"*🚀 FAMORTISCO AI*\n\n{st.session_state['resultado'][:1500]}..."
                    link = f"https://api.whatsapp.com/send?phone={num}&text={urllib.parse.quote(resumo)}"
                    st.link_button("Abrir WhatsApp", link)
    except Exception as e:
        st.error(f"Erro: {e}")
