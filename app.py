import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# Configuração visual
st.set_page_config(page_title="BoostEbook AI", layout="centered")
st.title("🧠 BoostEbook AI")

# Pega a chave dos Secrets que você já salvou
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    # Configuração oficial que resolve o erro 404
    genai.configure(api_key=api_key)
    
    file = st.file_uploader("Suba seu ebook (PDF)", type=['pdf'])
    
    if file:
        try:
            reader = PdfReader(file)
            texto = "".join([p.extract_text() or "" for p in reader.pages])
            st.success("✅ PDF pronto para análise!")
            
            if st.button("🚀 GERAR ESTRATÉGIA DE MARKETING"):
                with st.spinner('A IA está analisando seu conteúdo...'):
                    # Usando o modelo oficial para evitar 'Not Found'
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(f"Crie uma estratégia de marketing para este livro: {texto[:4000]}")
                    
                    st.markdown("---")
                    st.markdown("### 📈 Sua Estratégia Pronta:")
                    st.write(response.text)
                    st.balloons()
        except Exception as e:
            st.error(f"Erro ao processar: {e}")
else:
    st.error("⚠️ Configure a GOOGLE_API_KEY nos Secrets.")
