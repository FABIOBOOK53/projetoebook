import streamlit as st
import requests
from PyPDF2 import PdfReader
from docx import Document

st.set_page_config(page_title="BoostEbook AI", page_icon="🧠")
st.title("🧠 BoostEbook AI")

# Puxa a chave dos Secrets
api_key = st.secrets.get("GOOGLE_API_KEY") or st.sidebar.text_input("Gemini API Key", type="password")

def extrair_texto(arquivo):
    ext = arquivo.name.lower()
    try:
        if ext.endswith('.txt'): return arquivo.read().decode("utf-8")
        if ext.endswith('.pdf'):
            return "".join([p.extract_text() or "" for p in PdfReader(arquivo).pages])
        if ext.endswith('.docx'):
            return "\n".join([p.text for p in Document(arquivo).paragraphs])
    except: return None

if api_key:
    uploaded_file = st.file_uploader("Upload do seu Ebook", type=['txt', 'pdf', 'docx'])
    
    if uploaded_file:
        texto = extrair_texto(uploaded_file)
        if texto:
            st.success("Conteúdo carregado!")
            if st.button("Gerar Estratégia de Marketing"):
                with st.spinner('Conectando ao Google...'):
                    # FORÇAMOS A VERSÃO ESTÁVEL (v1) VIA URL DIRETA
                    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
                    payload = {"contents": [{"parts": [{"text": f"Crie 3 posts de marketing para: {texto[:4000]}"}]}]}
                    
                    response = requests.post(url, json=payload)
                    
                    if response.status_code == 200:
                        resultado = response.json()
                        st.markdown("### 🚀 Resultado:")
                        st.write(resultado['candidates'][0]['content']['parts'][0]['text'])
                    else:
                        st.error(f"Erro {response.status_code}: {response.text}")
else:
    st.info("Insira sua API Key.")
