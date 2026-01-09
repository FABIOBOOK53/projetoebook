import streamlit as st
import requests
from PyPDF2 import PdfReader
from docx import Document

st.set_page_config(page_title="FAMORTISCO AI")

st.title("FAMORTISCO AI")
st.write("Versao de teste - Gemini 1.0 PRO")

api_key = st.secrets.get("GOOGLE_API_KEY", "")

def extrair_texto(arquivo):
    if arquivo is None:
        return ""

    if arquivo.type == "application/pdf":
        reader = PdfReader(arquivo)
        texto = ""
        for p in reader.pages[:5]:
            texto = texto + (p.extract_text() or "")
        return texto

    if arquivo.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(arquivo)
        texto = ""
        for p in doc.paragraphs[:50]:
            texto = texto + p.text + "\n"
        return texto

    return ""

arquivo = st.file_uploader(
    "Envie um arquivo PDF ou DOCX",
    type=["pdf", "docx"]
)

if arquivo is not None:
    texto = extrair_texto(arquivo)

    if st.button("Gerar Estrategia"):
        if api_key == "":
            st.error("GOOGLE_API_KEY nao configurada")
        elif texto.strip() == "":
            st.error("Nao foi possivel extrair texto")
        else:
            st.info("Chamando a IA...")

            url = (
                "https://generativelanguage.googleapis.com/v1beta/"
                "models/gemini-1.0-pro:generateContent"
                "?key=" + api_key
            )

            prompt = (
                "Crie uma estrategia de marketing digital para o conteudo abaixo:\n\n"
                + texto[:3000]
            )

            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt}
                        ]
                    }
                ]
            }

            resposta = requests.post(url, json=payload)

            if resposta.status_code == 200:
                data = resposta.json()
                resultado = data["candidates"][0]["content"]["parts"][0]["text"]
                st.text_area("Resultado", resultado, height=300)
            else:
