import streamlit as st
import requests
from PyPDF2 import PdfReader
from docx import Document
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import urllib.parse

st.set_page_config(page_title="BoostEbook AI - Central de Vendas", layout="centered")
st.title("🧠 BoostEbook AI")

# Configurações via Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")
email_user = st.secrets.get("EMAIL_REMETENTE")
email_pass = st.secrets.get("EMAIL_SENHA")

def enviar_email(destino, conteudo):
    try:
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = destino
        msg['Subject'] = "🚀 Estratégia de Marketing - BoostEbook AI"
        msg.attach(MIMEText(conteudo, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, email_pass)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Erro no envio de e-mail: {e}")
        return False

file = st.file_uploader("Suba seu ebook (PDF ou DOCX)", type=['pdf', 'docx'])

if file and api_key:
    try:
        # Extração inteligente de texto
        if file.type == "application/pdf":
            reader = PdfReader(file)
            texto = "".join([p.extract_text() or "" for p in reader.pages[:5]])
        else:
            doc = Document(file)
            texto = "\n".join([p.text for p in doc.paragraphs[:50]])

        if st.button("🚀 GERAR ESTRATÉGIA COMPLETA"):
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={api_key}"
            prompt = f"Crie roteiros de ASMR, Reels e um e-mail de vendas para este conteúdo: {texto[:3000]}"
            
            response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
            
            if response.status_code == 200:
                resultado = response.json()['candidates'][0]['content']['parts'][0]['text']
                st.session_state['resultado'] = resultado
                st.subheader("Estratégia Gerada:")
                st.write(resultado)
                st.balloons()
            else:
                st.error("Erro na IA. Verifique sua chave.")

        # SEÇÃO DE DISPAROS
        if 'resultado' in st.session_state:
            st.divider()
            st.subheader("📲 Disparar Conteúdo")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### via E-mail")
                email_dest = st.text_input("E-mail do cliente:")
                if st.button("📧 Enviar Agora"):
                    if enviar_email(email_dest, st.session_state['resultado']):
                        st.success("E-mail enviado!")

            with col2:
                st.markdown("### via WhatsApp")
                num_whats = st.text_input("Número (Ex: 5511999999999):")
                if num_whats:
                    # Codifica o texto para o formato de URL do WhatsApp
                    texto_zap = urllib.parse.quote(st.session_state['resultado'])
                    link_zap = f"https://api.whatsapp.com/send?phone={num_whats}&text={texto_zap}"
                    st.link_button("🟢 Abrir no WhatsApp", link_zap)

    except Exception as e:
        st.error(f"Erro técnico: {e}")
