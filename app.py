import streamlit as st
import requests
from PyPDF2 import PdfReader

st.title("🧠 BoostEbook AI")

# Tenta ler a chave
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("⚠️ Chave GOOGLE_API_KEY não encontrada nos Secrets!")
else:
    file = st.file_uploader("Suba seu PDF", type=['pdf'])
    if file:
        reader = PdfReader(file)
        texto = "".join([p.extract_text() for p in reader.pages])
        st.success("PDF lido!")
        
        if st.button("Gerar Marketing"):
            # URL ESTÁVEL v1
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
            payload = {"contents": [{"parts": [{"text": f"Crie 3 posts de marketing para: {texto[:3000]}"}]}]}
            
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                st.write(response.json()['candidates'][0]['content']['parts'][0]['text'])
            elif response.status_code == 404:
                st.error("Erro 404: O Google não reconheceu este caminho. Verifique se a chave nos Secrets está correta e sem espaços.")
            elif response.status_code == 400:
                st.error("Erro 400: Chave inválida ou mal formatada. Gere uma nova no AI Studio.")
            else:
                st.error(f"Erro {response.status_code}: {response.text}")
