import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# Configuração da página
st.set_page_config(page_title="BoostEbook AI", layout="centered")
st.title("🧠 BoostEbook AI")

# Pega a chave dos Secrets (que já está salva!)
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    # Configuração oficial do Google
    genai.configure(api_key=api_key)
    
    file = st.file_uploader("Suba seu ebook (PDF)", type=['pdf'])
    
    if file:
        try:
            reader = PdfReader(file)
            texto = "".join([p.extract_text() or "" for p in reader.pages])
            st.success("✅ PDF pronto!")
            
            if st.button("🚀 GERAR ESTRATÉGIA DE MARKETING"):
                with st.spinner('A IA está trabalhando...'):
                    # O modelo flash agora via biblioteca oficial para evitar erro 404
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(f"Crie um post de marketing para: {texto[:4000]}")
                    
                    st.markdown("### 📈 Resultado:")
                    st.write(response.text)
                    st.balloons()
        except Exception as e:
            st.error(f"Erro ao processar: {e}")
else:
    st.error("⚠️ Configure a GOOGLE_API_KEY nos Secrets.")
