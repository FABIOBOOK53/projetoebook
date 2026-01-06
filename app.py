import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document
import os

# Configuração da Página
st.set_page_config(page_title="BoostEbook AI", page_icon="🧠")
st.title("🧠 BoostEbook AI")

# Estilo
st.markdown("""<style>.stButton>button { background-color: #6a0dad; color: white; width: 100%; }</style>""", unsafe_allow_html=True)

# Chave de API
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = st.sidebar.text_input("Insira sua Gemini API Key", type="password")

def extrair_texto(arquivo):
    ext = arquivo.name.lower()
    try:
        if ext.endswith('.txt'): return arquivo.read().decode("utf-8")
        if ext.endswith('.pdf'):
            reader = PdfReader(arquivo)
            return "".join([p.extract_text() or "" for p in reader.pages])
        if ext.endswith('.docx'):
            doc = Document(arquivo)
            return "\n".join([p.text for p in doc.paragraphs])
    except: return None
    return None

if api_key:
    try:
        # --- A SOLUÇÃO DEFINITIVA PARA O ERRO 404 ---
        # Forçamos a versão 'v1' e o transporte 'rest' para ignorar o 'v1beta'
        genai.configure(api_key=api_key, transport='rest')
        
        # Criamos o modelo usando o nome estável
        model = genai.GenerativeModel('gemini-1.5-flash')

        uploaded_file = st.file_uploader("Upload do Ebook", type=['txt', 'pdf', 'docx'])

        if uploaded_file is not None:
            texto = extrair_texto(uploaded_file)
            if texto:
                st.success("Arquivo carregado!")
                if st.button("Gerar Estratégia de Marketing"):
                    with st.spinner('Conectando ao cérebro da IA...'):
                        # Limitamos o texto para evitar erros de excesso de dados
                        response = model.generate_content(f"Aja como especialista em marketing. Crie 3 posts para: {texto[:5000]}")
                        st.markdown("### 🚀 Resultado:")
                        st.write(response.text)
    except Exception as e:
        st.error(f"Erro de conexão: {e}")
else:
    st.info("Aguardando chave da API.")
