import streamlit as st
import requests
from PyPDF2 import PdfReader
from docx import Document

st.set_page_config(page_title="FAMORTISCO AI")
st.title("FAMORTISCO AI")
st.write("Extração de PDF/DOCX + IA Gemini API")

API_KEY = st.secrets.get("GOOGLE_API_KEY")
if not API_KEY:
    st.error("GOOGLE_API_KEY nao configurada")
    st.stop()

def extrair_texto(arquivo):
    texto = ""
    if arquivo.type == "application/pdf":
        reader = PdfReader(arquivo)
        for p in reader.pages[:5]:
            texto += p.extract_text() or ""
    if arquivo.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(arquivo)
        for p in doc.paragraphs[:50]:
            texto += p.text + "\n"
    return texto.strip()

arquivo = st.file_uploader("Envie PDF ou DOCX", type=["pdf","docx"])

if arquivo:
    texto = extrair_texto(arquivo)
    if not texto:
        st.warning("Não foi possível extrair texto")
    else:
        st.success("Texto extraído com sucesso")
        if st.button("Gerar estratégia"):
            # Spinner seguro
            with st.spinner("Chamando a IA..."):
                modelo_funcional = "gemini-1.5"  # ajuste conforme chave
                url = f"https://generativelanguage.googleapis.com/v1/models/{modelo_funcional}:generateContent"
                prompt = "Crie uma estratégia prática com base no texto abaixo:\n\n" + texto[:2000]
                payload = {"contents":[{"parts":[{"text":prompt}]}]}
                headers = {"Content-Type":"application/json","x-goog-api-key":API_KEY}
                r = requests.post(url, headers=headers, json=payload)
                if r.status_code == 200:
                    resultado = r.json()["candidates"][0]["content"]["parts"][0]["text"]
                    st.text_area("Resultado", resultado, height=300)
                else:
                    st.error("Erro ao chamar a IA")
                    st.code(r.text)
