import streamlit as st
import requests
from PyPDF2 import PdfReader
from docx import Document

st.set_page_config(page_title="FAMORTISCO AI")

st.title("FAMORTISCO AI")

API_KEY = st.secrets.get("GOOGLE_API_KEY")

if not API_KEY:
    st.error("GOOGLE_API_KEY nao encontrada nos Secrets")
    st.stop()

def extrair_texto(arquivo):
    texto = ""

    if arquivo.type == "application/pdf":
        reader = PdfReader(arquivo)
        for page in reader.pages[:5]:
            texto = texto + (page.extract_text() or "")

    if arquivo.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(arquivo)
        for p in doc.paragraphs[:50]:
            texto = texto + p.text + "\n"

    return texto.strip()

arquivo = st.file_uploader("Envie um PDF ou DOCX", type=["pdf", "docx"])

if arquivo:
    texto = extrair_texto(arquivo)

    if texto == "":
        st.warning("Nao foi possivel extrair texto")
    else:
        if st.button("Gerar estrategia"):
            url = "https://generativelanguage.googleapis.
