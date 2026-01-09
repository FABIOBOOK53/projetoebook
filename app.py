import streamlit as st
import requests
from PyPDF2 import PdfReader
from docx import Document

# ---------------- CONFIGURAÇÃO ----------------
st.set_page_config(page_title="FAMORTISCO AI", layout="centered")
st.title("FAMORTISCO AI")
st.write("Extração de PDF/DOCX + IA Google AI Studio")

# ---------------- API KEY ----------------
API_KEY = st.secrets.get("GOOGLE_API_KEY")
if not API_KEY:
    st.error("GOOGLE_API_KEY não configurada")
    st.stop()

# ---------------- FUNÇÃO PARA EXTRAIR TEXTO ----------------
def extrair_texto(arquivo):
    texto = ""
    # PDF
    if arquivo.type == "application/pdf":
        reader = PdfReader(arquivo)
        for p in reader.pages[:5]:
            t = p.extract_text()
            if t:
                texto += t + "\n"
    # DOCX
    if arquivo.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(arquivo)
        for p in doc.paragraphs[:50]:
            texto += p.text + "\n"
    return texto.strip()

# ---------------- UPLOAD ----------------
arquivo = st.file_uploader("Envie PDF ou DOCX", type=["pdf", "docx"])

if arquivo:
    texto = extrair_texto(arquivo)
    if not texto:
        st.warning("Não foi possível extrair texto")
    else:
        st.success("Texto extraído com sucesso")

        if st.button("Gerar Estratégia"):
            with st.spinner("Chamando a IA..."):
                modelo = "text-bison-001"  # modelo funcional
                url = f"https://generativelanguage.googleapis.com/v1/models/{modelo}:generateContent"

                # Dividir o prompt em pedaços curtos para evitar quebra
                prompt1 = "Crie uma estratégia de marketing digital baseada no texto abaixo:"
                prompt2 = texto[:1500]  # limita a 1500 caracteres
                prompt = prompt1 + "\n\n" + prompt2

                payload = {"contents":[{"parts":[{"text":prompt}]}]}
                headers = {"Content-Type":"application/json","x-goog-api-key":API_KEY}

                try:
                    r = requests.post(url, headers=headers, json=payload, timeout=60)
                    if r.status_code == 200:
                        resultado = r.json()["candidates"][0]["content"]["parts"][0]["text"]
                        st.text_area("Resultado da IA", resultado, height=400)
                    else:
                        st.error("Erro ao chamar a IA")
                        st.code(r.text)
                except Exception as e:
                    st.error("Erro de conexão")
                    st.text(str(e))
