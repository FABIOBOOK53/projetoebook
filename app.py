import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document

st.set_page_config(page_title="BoostEbook AI", page_icon="🧠")

st.title("🧠 BoostEbook AI")

# Puxa a Key que você salvou nos Segredos
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
        # O COMANDO ABAIXO FORÇA A CONEXÃO A FUNCIONAR SEM ERRO 404
        genai.configure(api_key=api_key, transport='rest')
        
        model = genai.GenerativeModel('gemini-1.5-flash')

        uploaded_file = st.file_uploader("Upload do seu Ebook", type=['txt', 'pdf', 'docx'])

        if uploaded_file is not None:
            texto = extrair_texto(uploaded_file)
            if texto:
                st.success("Arquivo lido com sucesso!")
                if st.button("Gerar Estratégia de Marketing"):
                    with st.spinner('Criando sua campanha...'):
                        # Usamos os primeiros 6000 caracteres para o marketing
                        prompt = f"Crie uma legenda de Instagram e 3 títulos de anúncios para: {texto[:6000]}"
                        response = model.generate_content(prompt)
                        st.markdown("### 🚀 Campanha Gerada:")
                        st.write(response.text)
    except Exception as e:
        st.error(f"Erro de conexão com o Google: {e}")
else:
    st.info("Aguardando configuração da chave API.")
