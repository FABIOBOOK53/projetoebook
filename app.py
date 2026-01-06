import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="BoostEbook AI", page_icon="🧠")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { background-color: #6a0dad; color: white; border-radius: 10px; width: 100%; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 BoostEbook AI")

# 2. CHAVE DE API
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = st.sidebar.text_input("Insira sua Gemini API Key", type="password")

# 3. LEITOR DE ARQUIVOS
def extrair_texto(arquivo):
    ext = arquivo.name.lower()
    try:
        if ext.endswith('.txt'): return arquivo.read().decode("utf-8")
        if ext.endswith('.pdf'):
            reader = PdfReader(arquivo)
            return "".join([p.extract_text() or "" for p in reader.pages])
        if ext.endswith('.docx'):
            from docx import Document as DocxReader
            doc = DocxReader(arquivo)
            return "\n".join([p.text for p in doc.paragraphs])
    except: return None
    return None

# 4. LÓGICA DE GERAÇÃO
if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # USANDO O NOME DE MODELO MAIS COMPATÍVEL POSSÍVEL
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")

        uploaded_file = st.file_uploader("Upload do Ebook", type=['txt', 'pdf', 'docx'])

        if uploaded_file is not None:
            texto = extrair_texto(uploaded_file)
            if texto:
                st.success("Arquivo pronto!")
                if st.button("Gerar Marketing"):
                    with st.spinner('A IA está trabalhando...'):
                        # O segredo está em passar o conteúdo de forma simples aqui
                        response = model.generate_content(
                            f"Aja como especialista em marketing. Crie 3 posts para este conteúdo: {texto[:5000]}"
                        )
                        st.markdown("### 🚀 Resultado:")
                        st.write(response.text)
            else:
                st.error("Erro ao ler o arquivo.")
    except Exception as e:
        # Mostra o erro de forma mais amigável
        st.error(f"Erro de conexão: {e}")
else:
    st.info("Aguardando chave da API.")
