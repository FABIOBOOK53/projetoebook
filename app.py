import streamlit as st
import requests
from PyPDF2 import PdfReader
from docx import Document

# ---------------- CONFIG ----------------
st.set_page_config(page_title="FAMORTISCO AI", page_icon="🐦‍⬛")

st.title("🐦‍⬛ FAMORTISCO AI")
st.write("Versão de TESTE – integração Gemini")

api_key = st.secrets.get("GOOGLE_API_KEY", "")

# ---------------- FUNÇÕES ----------------
def extrair_texto(arquivo):
    if arquivo is None:
        return ""

    if arquivo.type == "application/pdf":
        reader = PdfReader(arquivo)
        texto = ""
        for p in reader.pages[:5]:
            texto += p.extract_text() or ""
        return texto

    if arquivo.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(arquivo)
        texto = ""
        for p in doc.paragraphs[:50]:
            texto += p.text + "\n"
        return texto

    return ""

# ---------------- INTERFACE ----------------
arquivo = st.file_uploader(
    "Envie um arquivo PDF ou DOCX",
    type=["pdf", "docx"]
)

if arquivo:
    texto = extrair_texto(arquivo)

    if st.button("🚀 Gerar Estratégia"):
