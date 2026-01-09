import streamlit as st
import requests
from PyPDF2 import PdfReader
from docx import Document

st.set_page_config(page_title="FAMORTISCO AI")
st.title("FAMORTISCO AI")

API_KEY = st.secrets.get("GOOGLE_API_KEY")

if not API_KEY:
    st.error("GOOGLE_API_KEY nao encontrada")
    st.stop()

def extrair_texto(arquivo):
    texto = ""

    if arquivo.type == "application/pdf":
        pdf = PdfReader(arquivo)
        for p in pdf.pages[:3]:
            texto += p.extract_text() or ""

    if arquivo.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(arquivo)
        for p in doc.paragraphs[:30]:
            texto += p.text + "\n"

    return texto.strip()

arquivo = st.file_uploader("Envie PDF ou DOCX", type=["pdf", "docx"])

if arquivo:
    texto = extrair_texto(arquivo)

    if texto:
        if st.button("Gerar estrategia"):
            endpoint = "https://generativelanguage.googleapis.com/v1/models/"
            endpoint += "gemini-1.5-flash:generateContent"

            prompt = "Crie uma estrategia de marketing:\n\n" + texto[:2000]

            body = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt}
                        ]
                    }
                ]
            }

            headers = {
                "Content-Type": "application/json",
                "x-goog-api-key": API_KEY
            }

            r = requests.post(endpoint, json=body, headers=headers)

            if r.status_code == 200:
                saida = r.json()["candidates"][0]["content"]["parts"][0]["text"]
                st.text_area("Resultado", saida, height=300)
            else:
                st.error("Erro na IA")
                st.code(r.text)
    else:
        st.warning("Texto nao extraido")
