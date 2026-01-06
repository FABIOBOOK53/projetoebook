import streamlit as st
import requests
from PyPDF2 import PdfReader

st.set_page_config(page_title="BoostEbook AI", layout="centered")
st.title("🧠 BoostEbook AI")

api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    file = st.file_uploader("Suba seu PDF", type=['pdf'])
    if file:
        reader = PdfReader(file)
        texto = "".join([p.extract_text() or "" for p in reader.pages])
        st.success("PDF lido com sucesso!")
        
        if st.button("🚀 GERAR ESTRATÉGIA"):
            with st.spinner('A IA está processando...'):
                # Tentativa 1: A rota mais comum para chaves novas
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                payload = {"contents": [{"parts": [{"text": f"Crie um post de marketing para: {texto[:3000]}"}]}]}
                
                res = requests.post(url, json=payload)
                
                # Se a tentativa 1 falhar (Erro 404), tentamos a rota alternativa (Plano B)
                if res.status_code != 200:
                    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
                    res = requests.post(url, json=payload)

                if res.status_code == 200:
                    st.markdown("### 📈 Resultado:")
                    st.write(res.json()['candidates'][0]['content']['parts'][0]['text'])
                else:
                    st.error(f"Erro {res.status_code}. O Google não aceitou o pedido. Verifique se a chave foi copiada corretamente do Google AI Studio.")
else:
    st.error("Configure a GOOGLE_API_KEY nos Secrets.")
