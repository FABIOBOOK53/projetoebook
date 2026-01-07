import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

st.set_page_config(page_title="BoostEbook AI")
st.title("🧠 BoostEbook AI")

api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    # Configuração explícita da versão da API para 2026
    genai.configure(api_key=api_key)
    
    file = st.file_uploader("Suba seu ebook", type=['pdf'])
    
    if file:
        try:
            reader = PdfReader(file)
            texto = "".join([p.extract_text() for p in reader.pages])
            st.success("✅ Conteúdo lido!")
            
            if st.button("🚀 GERAR ESTRATÉGIA"):
                with st.spinner('IA Processando...'):
                    # Mudança crucial: usamos o modelo sem o prefixo 'models/'
                    # e deixamos a SDK decidir a rota estável v1 automaticamente
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(f"Resuma este conteúdo: {texto[:3000]}")
                    st.write(response.text)
                    st.balloons()
        except Exception as e:
            st.error(f"Erro: {e}")
else:
    st.error("Configure a GOOGLE_API_KEY nos Segredos (Secrets).")
