import streamlit as st
import requests
from PyPDF2 import PdfReader
from docx import Document

st.set_page_config(page_title="BoostEbook AI", page_icon="🧠")
st.title("🧠 BoostEbook AI")

# Puxa a chave dos Secrets do Streamlit Cloud
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
    uploaded_file = st.file_uploader("Upload do Ebook", type=['txt', 'pdf', 'docx'])
    
    if uploaded_file:
        texto = extrair_texto(uploaded_file)
        if texto:
            st.success("Arquivo carregado!")
            if st.button("Gerar Marketing Viral"):
                with st.spinner('Conectando ao Gemini v1...'):
                    # USAMOS A URL v1 (A MESMA QUE FUNCIONOU NO SEU TESTE)
                    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
                    payload = {"contents": [{"parts": [{"text": f"Crie uma estratégia de marketing para: {texto[:4000]}"}]}]}
                    
                    response = requests.post(url, json=payload)
                    
                    if response.status_code == 200:
                        resultado = response.json()
                        st.markdown("### 🚀 Resultado:")
                        st.write(resultado['candidates'][0]['content']['parts'][0]['text'])
                    else:
                        st.error(f"Erro {response.status_code}. Verifique se a chave nos Secrets está correta.")
else:
    st.warning("⚠️ Adicione a GOOGLE_API_KEY nos Secrets do Streamlit.")
