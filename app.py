import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document

# Configuração da página
st.set_page_config(page_title="BoostEbook AI", page_icon="🧠")
st.title("🧠 BoostEbook AI")

# Estilo rápido
st.markdown("""<style>.stButton>button { background-color: #6a0dad; color: white; width: 100%; }</style>""", unsafe_allow_html=True)

# Puxa a chave dos Secrets
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
        # AQUI ESTÁ A SOLUÇÃO: Forçamos a versão 'v1' (estável)
        genai.configure(api_key=api_key, transport='rest')
        
        # Criamos o modelo de forma simplificada
        model = genai.GenerativeModel('gemini-1.5-flash')

        uploaded_file = st.file_uploader("Upload do seu Ebook", type=['txt', 'pdf', 'docx'])

        if uploaded_file is not None:
            texto = extrair_texto(uploaded_file)
            if texto:
                st.success("Arquivo pronto!")
                if st.button("Gerar Estratégia de Marketing"):
                    with st.spinner('A IA está trabalhando...'):
                        # Usamos um prompt direto
                        response = model.generate_content(f"Crie 3 posts de marketing para: {texto[:4000]}")
                        st.markdown("---")
                        st.write(response.text)
            else:
                st.error("Não foi possível ler o arquivo.")
    except Exception as e:
        # Se o erro 404 aparecer, o problema é o nome do modelo
        st.error(f"Erro: {e}")
else:
    st.info("Aguardando chave da API.")
