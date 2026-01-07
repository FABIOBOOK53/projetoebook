import streamlit as st
import requests
from PyPDF2 import PdfReader
from docx import Document
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import urllib.parse

# Configuração da Página
st.set_page_config(page_title="BoostEbook AI - Pro", layout="wide")
st.title("🧠 BoostEbook AI")
st.markdown("---")

# 1. Configurações via Secrets (Streamlit Cloud)
api_key = st.secrets.get("GOOGLE_API_KEY")
email_user = st.secrets.get("EMAIL_REMETENTE")
email_pass = st.secrets.get("EMAIL_SENHA")
meu_zap = st.secrets.get("MEU_WHATSAPP", "") # Pega dos Secrets se existir

# Função para Enviar E-mail
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

# 2. Upload de Arquivo
file = st.file_uploader("Suba seu ebook (PDF ou DOCX)", type=['pdf', 'docx'])

if file and api_key:
    try:
        # Extração de Texto para PDF ou DOCX
        texto_extraido = ""
        if file.type == "application/pdf":
            reader = PdfReader(file)
            texto_extraido = "".join([p.extract_text() or "" for p in reader.pages[:10]])
        else:
            doc = Document(file)
            texto_extraido = "\n".join([p.text for p in doc.paragraphs[:100]])

        if st.button("🚀 GERAR ESTRATÉGIA COMPLETA"):
            # Rota do Gemini 3 Flash que validamos no chat do AI Studio
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={api_key}"
            
            prompt = f"""
            Você é um especialista em marketing literário. Com base no texto: {texto_extraido[:3500]}
            1. Crie 3 roteiros de 15s para Reels/TikTok.
            2. Crie 1 roteiro sensorial ASMR.
            3. Escreva um e-mail de vendas irresistível.
            4. Defina o público-alvo ideal.
            """
            
            with st.spinner('A IA está analisando seu livro...'):
                response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
                
                if response.status_code == 200:
                    resultado = response.json()['candidates'][0]['content']['parts'][0]['text']
                    st.session_state['resultado'] = resultado
                    st.balloons()
                else:
                    st.error(f"Erro na IA: {response.status_code}")
                    st.write(response.text)

        # 3. Exibição e Disparos
        if 'resultado' in st.session_state:
            st.markdown("### 📊 Resultado da Estratégia")
            st.info(st.session_state['resultado'])
            
            st.divider()
            st.subheader("📲 Canais de Disparo")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📧 Enviar por E-mail")
                email_dest = st.text_input("E-mail do Destinatário:", placeholder="cliente@email.com")
                if st.button("📧 Disparar E-mail"):
                    if not email_user or not email_pass:
                        st.warning("Configure EMAIL_REMETENTE e EMAIL_SENHA nos Secrets.")
                    elif enviar_email(email_dest, st.session_state['resultado']):
                        st.success(f"Enviado para {email_dest}!")

            with col2:
                st.markdown("#### 🟢 Enviar por WhatsApp")
                num_whats = st.text_input("Número (com DDD):", value=meu_zap, placeholder="5511999999999")
                
                if num_whats:
                    # Limita o texto para não quebrar o link do WhatsApp
                    texto_curto = st.session_state['resultado'][:1500]
                    texto_url = urllib.parse.quote(f"*🚀 ESTRATÉGIA BOOST EBOOK AI*\n\n{texto_curto}...")
                    link_zap = f"https://api.whatsapp.com/send?phone={num_whats}&text={texto_url}"
                    st.link_button("🟢 Abrir no WhatsApp", link_zap)

    except Exception as e:
        st.error(f"Erro no processamento: {e}")

else:
    if not api_key:
        st.warning("⚠️ Adicione sua GOOGLE_API_KEY nos Secrets do Streamlit.")
