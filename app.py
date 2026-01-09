import streamlit as st
from PyPDF2 import PdfReader
from docx import Document
import requests

st.set_page_config(page_title="FAMORTISCO AI", layout="centered")
st.title("FAMORTISCO AI")
st.write("Upload PDF/DOCX + geração de estratégia com Gemini 2.5")

# ---------------- API KEY ----------------
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# Função para extrair texto de PDF/DOCX
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
                # --------- Verifica se a conta tem chave ---------
                if API_KEY:
                    # --------- Chamada para IA real ---------
                    modelo_funcional = "models/gemini-2.5-flash"  # modelo real
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
                            # Se 404 (Free account), usa simulação
                            st.warning("Não foi possível chamar a IA real (conta Free). Mostrando resultado simulado.")
                            resultado_simulado = (
                                "=== SIMULAÇÃO DE RESULTADO ===\n\n"
                                "Resumo do seu arquivo:\n"
                                + texto[:500]
                                + "\n\nSugestão de estratégia:\n"
                                "- Use títulos chamativos\n"
                                "- Poste snippets do conteúdo nas redes sociais\n"
                                "- Incentive engajamento com perguntas aos seguidores\n"
                                "- Crie e-mails curtos e diretos promovendo o conteúdo"
                            )
                            st.text_area("Resultado da IA (simulado)", resultado_simulado, height=400)
                    except Exception as e:
                        st.error(f"Erro de conexão: {e}")
                else:
                    # --------- Conta sem chave ---------
                    st.warning("GOOGLE_API_KEY não configurada. Usando resultado simulado.")
                    resultado_simulado = (
                        "=== SIMULAÇÃO DE RESULTADO ===\n\n"
                        "Resumo do seu arquivo:\n"
                        + texto[:500]
                        + "\n\nSugestão de estratégia:\n"
                        "- Use títulos chamativos\n"
                        "- Poste snippets do conteúdo nas redes sociais\n"
                        "- Incentive engajamento com perguntas aos seguidores\n"
                        "- Crie e-mails curtos e diretos promovendo o conteúdo"
                    )
                    st.text_area("Resultado da IA (simulado)", resultado_simulado, height=400)
