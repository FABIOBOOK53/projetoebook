import streamlit as st
import requests
from PyPDF2 import PdfReader

st.set_page_config(page_title="BoostEbook AI", page_icon="🧠")
st.title("🧠 BoostEbook AI")

# Tenta buscar a chave salva nos Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    uploaded_file = st.file_uploader("Upload do seu Ebook", type=['pdf'])
    
    if uploaded_file:
        reader = PdfReader(uploaded_file)
        texto = "".join([p.extract_text() for p in reader.pages])
        st.success("Arquivo pronto!")
        
        if st.button("Gerar Marketing Viral"):
            with st.spinner('Conectando ao Gemini v1...'):
                # URL DIRETA v1 PARA ELIMINAR O ERRO 404 V1BETA
                url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
                payload = {"contents": [{"parts": [{"text": f"Crie 3 posts de marketing para: {texto[:4000]}"}]}]}
                
                response = requests.post(url, json=payload)
                if response.status_code == 200:
                    st.markdown("### 🚀 Resultado:")
                    st.write(response.json()['candidates'][0]['content']['parts'][0]['text'])
                else:
                    st.error(f"Erro {response.status_code}: Verifique a chave nos Secrets.")
else:
    st.warning("⚠️ Chave API não configurada nos Secrets.")
