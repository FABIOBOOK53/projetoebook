import streamlit as st
import requests
from PyPDF2 import PdfReader

st.set_page_config(page_title="BoostEbook AI", page_icon="🧠")
st.title("🧠 BoostEbook AI")

# Busca a chave sem o caractere estranho que estava antes
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    file = st.file_uploader("Suba seu PDF", type=['pdf'])
    if file:
        reader = PdfReader(file)
        texto = "".join([p.extract_text() or "" for p in reader.pages])
        st.success("PDF pronto!")
        
        if st.button("Gerar Marketing"):
            with st.spinner('IA processando...'):
                # Usando a URL estável v1
                url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
                payload = {"contents": [{"parts": [{"text": f"Crie 3 posts de marketing para este livro: {texto[:3000]}"}]}]}
                
                try:
                    response = requests.post(url, json=payload)
                    if response.status_code == 200:
                        st.markdown("### 🚀 Resultado:")
                        st.write(response.json()['candidates'][0]['content']['parts'][0]['text'])
                    else:
                        st.error(f"Erro {response.status_code}: Verifique se removeu o ponto antes de GOOGLE nos Secrets.")
                except Exception as e:
                    st.error(f"Falha: {e}")
else:
    st.warning("⚠️ Configure a chave GOOGLE_API_KEY corretamente nos Secrets.")
