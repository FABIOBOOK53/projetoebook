import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document

# 1. Configuração Visual
st.set_page_config(page_title="BoostEbook AI", page_icon="🧠")
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { background-color: #6a0dad; color: white; border-radius: 10px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 BoostEbook AI")

# 2. Chave de API (Secrets)
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = st.sidebar.text_input("Insira sua Gemini API Key", type="password")

# 3. Função de Leitura de Arquivos
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

# 4. Conexão e Geração (Forçando Versão Estável)
if api_key:
    try:
        # Forçamos o transporte REST para evitar o erro v1beta das imagens anteriores
        genai.configure(api_key=api_key, transport='rest')
        model = genai.GenerativeModel('gemini-1.5-flash')

        uploaded_file = st.file_uploader("Upload do Ebook", type=['txt', 'pdf', 'docx'])

        if uploaded_file is not None:
            texto = extrair_texto(uploaded_file)
            if texto:
                st.success("Arquivo pronto!")
                if st.button("Gerar Estratégia de Marketing"):
                    with st.spinner('Criando sua campanha...'):
                        # Usamos os primeiros 5000 caracteres para segurança
                        response = model.generate_content(f"Aja como especialista em marketing viral. Crie 3 chamadas para: {texto[:5000]}")
                        st.markdown("---")
                        st.markdown("### 🚀 Resultado:")
                        st.write(response.text)
            else:
                st.error("Não foi possível ler o arquivo.")
    except Exception as e:
        st.error(f"Erro de conexão: {e}")
else:
    st.info("Aguardando chave da API.")
