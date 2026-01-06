import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document

# Configuração da Página
st.set_page_config(page_title="Mkt Ebook26 AI", page_icon="🧠")
st.title("🧠 Mkt Ebook26 AI")

# Chave de API (Pega dos Secrets do Streamlit)
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
        # FORÇANDO A VERSÃO ESTÁVEL (v1) E O TRANSPORTE REST
        genai.configure(api_key=api_key, transport='rest')
        
        # Usamos o modelo flash que é o mais compatível
        model = genai.GenerativeModel('gemini-1.5-flash')

        uploaded_file = st.file_uploader("Upload do Ebook", type=['txt', 'pdf', 'docx'])

        if uploaded_file is not None:
            texto = extrair_texto(uploaded_file)
            if texto:
                st.success("Arquivo carregado com sucesso!")
                if st.button("Gerar Estratégia de Marketing"):
                    with st.spinner('A IA está processando...'):
                        # Chamada simplificada para evitar erro de rota
                        response = model.generate_content(f"Crie 3 posts de marketing para este livro: {texto[:5000]}")
                        st.markdown("---")
                        st.write(response.text)
            else:
                st.error("Não foi possível ler o arquivo.")
    except Exception as e:
        st.error(f"Erro Crítico: {e}")
else:
    st.info("Aguardando chave da API.")


