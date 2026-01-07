import streamlit as st
import requests
from PyPDF2 import PdfReader

st.set_page_config(page_title="BoostEbook AI", layout="centered")
st.title("🧠 BoostEbook AI")

# Puxa a chave dos Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

file = st.file_uploader("Suba seu ebook (PDF)", type=['pdf'])

if file and api_key:
    try:
        reader = PdfReader(file)
        texto = "".join([p.extract_text() or "" for p in reader.pages[:5]])
        
        if texto:
            st.success("✅ Documento lido com sucesso!")
            
            if st.button("🚀 GERAR ESTRATÉGIA"):
                # TESTAMOS AS DUAS ROTAS POSSÍVEIS PARA EVITAR O ERRO 404
                rotas = [
                    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}",
                    f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
                ]
                
                sucesso = False
                for url in rotas:
                    with st.spinner(f'Tentando conexão...'):
                        response = requests.post(url, json={
                            "contents": [{"parts": [{"text": f"Resuma: {texto[:3000]}"}]}]
                        })
                        
                        if response.status_code == 200:
                            res = response.json()
                            st.subheader("Sua Estratégia:")
                            st.write(res['candidates'][0]['content']['parts'][0]['text'])
                            st.balloons()
                            sucesso = True
                            break
                
                if not sucesso:
                    st.error(f"O Google ainda recusa a chave (Erro {response.status_code})")
                    st.json(response.json()) # Mostra o motivo real do bloqueio
    except Exception as e:
        st.error(f"Erro técnico: {e}")
else:
    st.info("Aguardando PDF e Chave API válida nos Secrets.")
