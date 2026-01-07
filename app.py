import streamlit as st
import requests
from PyPDF2 import PdfReader

st.set_page_config(page_title="BoostEbook AI", layout="centered")
st.title("🧠 BoostEbook AI")

# Chave que você configurou no botão azul 'Gerenciar Aplicativo' -> 'Secrets'
api_key = st.secrets.get("GOOGLE_API_KEY")

file = st.file_uploader("Suba seu ebook (PDF)", type=['pdf'])

if file and api_key:
    try:
        reader = PdfReader(file)
        # Extrai texto apenas das primeiras páginas para não travar o plano Free
        texto = "".join([p.extract_text() or "" for p in reader.pages[:5]])
        
        if texto:
            st.success("✅ Documento lido com sucesso!")
            
            if st.button("🚀 GERAR ESTRATÉGIA"):
                # URL específica para quem NÃO usa Google Cloud (Plano Free AI Studio)
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                
                payload = {
                    "contents": [{"parts": [{"text": f"Crie um resumo de marketing para este conteúdo: {texto[:3000]}"}]}]
                }
                
                with st.spinner('IA Processando...'):
                    response = requests.post(url, json=payload)
                    
                    if response.status_code == 200:
                        resultado = response.json()
                        st.subheader("Sua Estratégia:")
                        st.write(resultado['candidates'][0]['content']['parts'][0]['text'])
                        st.balloons()
                    else:
                        st.error(f"O Google recusou a conexão. Erro: {response.status_code}")
                        st.write("Detalhe do erro:", response.text)
    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
else:
    if not api_key:
        st.info("Por favor, adicione sua chave API nos 'Secrets' do Streamlit com o nome GOOGLE_API_KEY.")
