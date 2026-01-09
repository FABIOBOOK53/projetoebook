import streamlit as st
from PyPDF2 import PdfReader
from docx import Document
import requests
import urllib.parse

st.set_page_config(page_title="FAMORTISCO AI", layout="centered")
st.title("FAMORTISCO AI")
st.write("Upload PDF/DOCX + geração de estratégia")

# ---------------- SECRETS ----------------
API_KEY = st.secrets.get("GOOGLE_API_KEY")
MEU_WHATSAPP = st.secrets.get("MEU_WHATSAPP", "")
EMAIL_REMETENTE = st.secrets.get("EMAIL_REMETENTE")
EMAIL_SENHA = st.secrets.get("EMAIL_SENHA")

# ---------------- FUNÇÃO PARA EXTRAIR TEXTO ----------------
def extrair_texto(arquivo):
    texto = ""
    if arquivo.type == "application/pdf":
        reader = PdfReader(arquivo)
        for p in reader.pages[:5]:
            t = p.extract_text()
            if t:
                texto += t + "\n"
    elif arquivo.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(arquivo)
        for p in doc.paragraphs[:50]:
            texto += p.text + "\n"
    return texto.strip()

# ---------------- UPLOAD ----------------
arquivo = st.file_uploader("Envie PDF ou DOCX", type=["pdf","docx"])

if arquivo:
    texto = extrair_texto(arquivo)
    if not texto:
        st.warning("Não foi possível extrair texto do arquivo")
    else:
        st.success("Texto extraído com sucesso")

        if st.button("Gerar Estratégia"):
            with st.spinner("Processando..."):
                if API_KEY:
                    # --------- Tenta chamar IA real ---------
                    modelo_funcional = "models/gemini-2.5-flash"
                    url = f"https://generativelanguage.googleapis.com/v1/models/{modelo_funcional}:generateContent"
                    prompt = (
                        "Você é um especialista em marketing digital.\n"
                        "Crie roteiros de Reels, ASMR e e-mail de vendas com base no texto abaixo:\n\n"
                        + texto[:3500]
                    )
                    payload = {"contents":[{"parts":[{"text":prompt}]}]}
                    headers = {"Content-Type":"application/json", "x-goog-api-key":API_KEY}

                    try:
                        r = requests.post(url, headers=headers, json=payload, timeout=60)
                        if r.status_code == 200:
                            resultado = r.json()["candidates"][0]["content"]["parts"][0]["text"]
                            st.text_area("Resultado da IA (real)", resultado, height=400)
                        else:
                            # --------- Se 404, usa simulação ---------
                            st.warning("Não foi possível chamar a IA real (conta Free). Mostrando resultado simulado.")
                            resultado = (
                                "=== SIMULAÇÃO DE RESULTADO ===\n\n"
                                "Resumo do seu arquivo:\n"
                                + texto[:500]
                                + "\n\nSugestão de estratégia:\n"
                                "- Use títulos chamativos\n"
                                "- Poste snippets do conteúdo nas redes sociais\n"
                                "- Incentive engajamento com perguntas aos seguidores\n"
                                "- Crie e-mails curtos e diretos promovendo o conteúdo"
                            )
                            st.text_area("Resultado da IA (simulado)", resultado, height=400)
                    except Exception as e:
                        st.error(f"Erro de conexão: {e}")
                else:
                    # --------- Sem chave ---------
                    st.warning("GOOGLE_API_KEY não configurada. Mostrando resultado simulado.")
                    resultado = (
                        "=== SIMULAÇÃO DE RESULTADO ===\n\n"
                        "Resumo do seu arquivo:\n"
                        + texto[:500]
                        + "\n\nSugestão de estratégia:\n"
                        "- Use títulos chamativos\n"
                        "- Poste snippets do conteúdo nas redes sociais\n"
                        "- Incentive engajamento com perguntas aos seguidores\n"
                        "- Crie e-mails curtos e diretos promovendo o conteúdo"
                    )
                    st.text_area("Resultado da IA (simulado)", resultado, height=400)

        # ---------------- OPÇÃO DE ENVIO ----------------
        st.divider()
        st.write("📤 Enviar resultado")

        if 'resultado' in locals():
            c1, c2 = st.columns(2)
            with c1:
                num = st.text_input("WhatsApp (DDD+Número):", value=MEU_WHATSAPP)
                if st.button("Enviar pelo WhatsApp"):
                    if num:
                        link = f"https://api.whatsapp.com/send?phone={num}&text={urllib.parse.quote(resultado[:1000])}"
                        st.markdown(f"[Abrir WhatsApp]({link})", unsafe_allow_html=True)
            with c2:
                dest = st.text_input("E-mail para envio:")
                if st.button("Enviar por E-mail"):
                    import smtplib
                    from email.mime.text import MIMEText
                    from email.mime.multipart import MIMEMultipart

                    try:
                        msg = MIMEMultipart()
                        msg['From'] = EMAIL_REMETENTE
                        msg['To'] = dest
                        msg['Subject'] = "📜 Sua Estratégia - FAMORTISCO AI"
                        msg.attach(MIMEText(resultado, 'plain'))

                        server = smtplib.SMTP('smtp.gmail.com', 587)
                        server.starttls()
                        server.login(EMAIL_REMETENTE, EMAIL_SENHA)
                        server.send_message(msg)
                        server.quit()
                        st.success("E-mail enviado com sucesso!")
                    except Exception as e:
                        st.error(f"Erro ao enviar e-mail: {e}")
