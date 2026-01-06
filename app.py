import streamlit as st
import requests
from PyPDF2 import PdfReader
from docx import Document

st.set_page_config(page_title="BoostEbook AI", page_icon="🧠")
st.title("🧠 BoostEbook AI")

# Puxa a chave dos Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

def extrair_texto(arquivo):
    try:
        if arquivo.name.lower().endswith('.pdf'):
            return "".join([p.extract_text() or "" for p in PdfReader(arquivo).pages])
        if arquivo.name.lower().endswith('.docx'):
            return "\n".join([p.text for p in Document(arquivo).paragraphs])
        return arquivo.read().decode("utf-8")
    except: return None

if api_key:
    uploaded_file = st.file_uploader("Upload do seu Ebook", type=['txt', 'pdf', 'docx'])
    
    if uploaded_file:
        texto = extrair_texto(uploaded_file)
        if texto:
            st.success("Arquivo pronto para análise!")
            if st.button("Gerar Marketing Viral"):
                with st.spinner('Conectando ao cérebro da IA (v1)...'):
                    # FORÇAMOS A URL ESTÁVEL PARA EVITAR O ERRO 404
                    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
                    payload = {
                        "contents": [{
                            "parts": [{"text": f"Aja como um mestre do marketing. Crie 3 posts de Instagram para: {texto[:4000]}"}]
                        }]
                    }
                    
                    try:
                        response = requests.post(url, json=payload)
                        if response.status_code == 200:
                            res_json = response.json()
                            st.markdown("### 🚀 Resultado:")
                            st.write(res_json['candidates'][0]['content']['parts'][0]['text'])
                        else:
                            st.error(f"Erro {response.status_code}: {response.text}")
                    except Exception as e:
                        st.error(f"Erro de conexão: {e}")
else:
    st.warning("⚠️ Chave API não encontrada nos Secrets.")
