import streamlit as st
import requests
from PyPDF2 import PdfReader
from docx import Document
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.set_page_config(page_title="BoostEbook AI - Pro", layout="centered")
st.title("🧠 BoostEbook AI")

# Configurações via Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")
email_user = st.secrets.get("EMAIL_REMETENTE")
email_pass = st.secrets.get("EMAIL_SENHA")

file = st.file_uploader("Suba seu ebook (PDF ou DOCX)", type=['pdf', 'docx'])

def enviar_email(destino, conteudo):
    try:
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = destino
        msg['Subject'] = "🚀 Sua Estratégia de Marketing - BoostEbook AI"
        
        msg.attach(MIMEText(conteudo, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, email_pass)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Erro ao enviar e-mail: {e}")
        return False

if file and api_key:
    # Lógica de extração de texto (PDF/DOCX)
    if file.type == "application/pdf":
        reader = PdfReader(file)
        texto = "".join([p.extract_text() or "" for p in reader.pages[:5]])
    else:
        doc = Document(file)
        texto = "\n".join([p.text for p in doc.paragraphs[:50]])

    if st.button("🚀 GERAR ESTRATÉGIA COMPLETA"):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={api_key}"
        prompt = f"Crie roteiros de ASMR, Reels e um e-mail de vendas para: {texto[:3000]}"
        
        response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
        
        if response.status_code == 200:
            resultado = response.json()['candidates'][0]['content']['parts'][0]['text']
            st.session_state['resultado'] = resultado
            st.write(resultado)
            st.balloons()

    # Opção de envio de e-mail após a geração
    if 'resultado' in st.session_state:
        email_destino = st.text_input("Enviar para qual e-mail?")
        if st.button("📧 DISPARAR ESTRATÉGIA"):
            if enviar_email(email_destino, st.session_state['resultado']):
                st.success(f"E-mail enviado com sucesso para {email_destino}!")
