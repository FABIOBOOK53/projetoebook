import streamlit as st
import requests
from PyPDF2 import PdfReader
from docx import Document

st.set_page_config(page_title="FAMORTISCO AI", layout="centered")
st.title("FAMORTISCO AI")
st.write("Upload PDF/DOCX + geração de estratégia com Gemini 2.5")

# ---------------- API KEY ----------------
API_KEY = st.secrets.get("GOOGLE_API_KEY")
if not API_KEY:
    st.error("GOOGLE_API_KEY não configurada")
    st.stop()

# ---------------- FUNÇÃO PARA EXTRAIR TEXTO ----------------
def extrair_texto(arquivo):
    texto = ""
    if arquivo.type == "application/pdf":
        reader = PdfReader(arquivo)
        for p in reader.pages[:5]:
            t = p.extract_text()
            if t:
                texto += t + "\n"
    if arquivo.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(arquivo)
        for p in doc.paragraphs[:50]:
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

st.write("Modelos disponíveis para teste:")
st.write(modelos_disponiveis)

modelo_funcional = st.selectbox("Escolha o modelo", modelos_disponiveis, index=0)

# ---------------- GERAR ESTRATÉGIA ----------------
if arquivo and modelo_funcional:
    texto = extrair_texto(arquivo)
    if not texto:
        st.warning("Não foi possível extrair texto do arquivo")
    else:
        st.success("Texto extraído com sucesso")

        if st.button("Gerar Estratégia"):
            with st.spinner("Chamando a IA..."):
                url = f"https://generativelanguage.googleapis.com/v1/models/{modelo_funcional}:generateContent"
                prompt = "Você é um especialista em marketing digital. Crie uma estratégia prática baseada no texto abaixo:\n\n" + texto[:3000]
                payload = {"contents":[{"parts":[{"text":prompt}]}]}
                headers = {"Content-Type":"application/json","x-goog-api-key":API_KEY}

                try:
                    r = requests.post(url, headers=headers, json=payload, timeout=60)
                    if r.status_code == 200:
                        resultado = r.json()["candidates"][0]["content"]["parts"][0]["text"]
                        st.text_area("Resultado da IA", resultado, height=400)
                    else:
                        st.error(f"Erro ao chamar a IA: {r.status_code}")
                        st.code(r.text)
                except Exception as e:
                    st.error(f"Erro de conexão: {e}")
