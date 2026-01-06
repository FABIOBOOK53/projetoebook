import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document

st.set_page_config(page_title="BoostEbook AI", page_icon="🧠")
st.title("🧠 BoostEbook AI")

# Puxa a chave dos Secrets do Streamlit
api_key = st.secrets.get("GOOGLE_API_KEY")

def extrair_texto(arquivo):
    try:
        if arquivo.name.lower().endswith('.pdf'):
            return "".join([p.extract_text() or "" for p in PdfReader(arquivo).pages])
        if arquivo.name.lower().endswith('.docx'):
            return "\n".join([p.text for p in Document(arquivo).paragraphs])
        return arquivo.read().decode("utf-8")
    except: return None

if api_key:
    try:
        genai.configure(api_key=api_key)
        # Usamos o modelo que funcionou no seu teste anterior
        model = genai.GenerativeModel('gemini-1.5-flash')

        uploaded_file = st.file_uploader("Upload do Ebook", type=['txt', 'pdf', 'docx'])

        if uploaded_file:
            texto = extrair_texto(uploaded_file)
            if texto:
                st.success("Conteúdo carregado!")
                if st.button("Gerar Marketing Viral"):
                    with st.spinner('A IA está trabalhando...'):
                        response = model.generate_content(f"Crie 3 posts para Instagram sobre: {texto[:4000]}")
                        st.markdown("### 🚀 Resultado:")
                        st.write(response.text)
    except Exception as e:
        st.error(f"Erro: {e}")
else:
    st.warning("⚠️ Chave API não configurada nos Secrets do Streamlit.")
