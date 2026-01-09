import streamlit as st
from PyPDF2 import PdfReader
from docx import Document

st.set_page_config(page_title="FAMORTISCO AI", layout="centered")
st.title("FAMORTISCO AI")
st.write("Upload PDF/DOCX + geração de estratégia (simulação para conta Free)")

# ---------------- API KEY ----------------
API_KEY = st.secrets.get("GOOGLE_API_KEY")
if not API_KEY:
    st.warning("GOOGLE_API_KEY não configurada. O app usará resposta simulada.")

# ---------------- FUNÇÃO PARA EXTRAIR TEXTO ----------------
def extrair_texto(arquivo):
    texto = ""
    if arquivo.type == "application/pdf":
        reader = PdfReader(arquivo)
        for p in reader.pages[:5]:  # limita a 5 páginas
            t = p.extract_text()
            if t:
                texto += t + "\n"
    elif arquivo.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(arquivo)
        for p in doc.paragraphs[:50]:  # limita a 50 parágrafos
            texto += p.text + "\n"
    return texto.strip()

# ---------------- UPLOAD ----------------
arquivo = st.file_uploader("Envie PDF ou DOCX", type=["pdf","docx"])

# ---------------- SELEÇÃO DE MODELO ----------------
modelos_disponiveis = [
    "models/gemini-2.5-flash",
    "models/gemini-2.5-pro",
    "models/gemini-2.0-flash",
    "models/gemini-2.0-flash-001",
    "models/gemini-2.0-flash-lite-001",
    "models/gemini-2.0-flash-lite",
    "models/gemini-2.5-flash-lite"
]

# Mostrar selectbox só depois do upload
if arquivo:
    texto = extrair_texto(arquivo)
    if not texto:
        st.warning("Não foi possível extrair texto do arquivo")
    else:
        st.success("Texto extraído com sucesso")
        modelo_funcional = st.selectbox("Escolha o modelo", modelos_disponiveis, index=0)

        # ---------------- BOTÃO GERAR ESTRATÉGIA ----------------
        if st.button("Gerar Estratégia"):
            with st.spinner("Processando..."):
                # ---------------- SIMULAÇÃO PARA CONTA FREE ----------------
                resultado_simulado = (
                    "=== SIMULAÇÃO DE RESULTADO ===\n\n"
                    "Resumo do seu arquivo:\n"
                    + texto[:500]
                    + "\n\nSugestão de estratégia: Use títulos chamativos, poste snippets do conteúdo nas redes sociais e incentive engajamento com perguntas aos seguidores."
                )
                st.text_area("Resultado da IA (simulado)", resultado_simulado, height=400)
