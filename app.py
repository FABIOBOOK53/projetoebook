import streamlit as st
import requests
from PyPDF2 import PdfReader

st.title("🧠 BoostEbook AI")

# Busca a chave nos Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    file = st.file_uploader("Suba seu PDF", type=['pdf'])
    if file:
        # Extração simples do texto
        reader = PdfReader(file)
        texto = "".join([p.extract_text() for p in reader.pages])
        st.success("PDF lido com sucesso!")
        
        if st.button("Gerar Marketing"):
            with st.spinner('IA trabalhando...'):
                # URL V1 DIRETA (A que funciona!)
                url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
                payload = {"contents": [{"parts": [{"text": f"Crie 3 posts de Instagram para este livro: {texto[:3000]}"}]}]}
                
                res = requests.post(url, json=payload)
                if res.status_code == 200:
                    st.write(res.json()['candidates'][0]['content']['parts'][0]['text'])
                else:
                    st.error(f"Erro {res.status_code}. Verifique se a chave no Secret é a mesma do Google AI Studio.")
else:
    st.warning("Aguardando chave API nos Secrets...")
