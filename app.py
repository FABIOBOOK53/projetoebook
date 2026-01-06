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

# 2. CHAVE DE API (Puxa dos Secrets do Streamlit)
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = st.sidebar.text_input("Insira sua Gemini API Key", type="password")

# 3. FUNÇÃO PARA LER ARQUIVOS
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

# 4. LÓGICA DE GERAÇÃO (FORÇANDO VERSÃO ESTÁVEL)
if api_key:
    try:
        # Configuração forçando o transporte estável para evitar o erro 404
        genai.configure(api_key=api_key, transport='rest')
        
        # Criamos o modelo forçando a versão 'v1'
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
        )

        uploaded_file = st.file_uploader("Upload do Ebook (PDF, DOCX ou TXT)", type=['txt', 'pdf', 'docx'])

        if uploaded_file is not None:
            texto_extraido = extrair_texto(uploaded_file)
            if texto_extraido:
                st.success("Arquivo lido com sucesso!")
                if st.button("Gerar Estratégia de Marketing"):
                    with st.spinner('A IA está criando sua estratégia...'):
                        # Usamos um prompt direto e curto para testar a conexão
                        prompt = f"Aja como um mestre do marketing. Crie 3 chamadas virais para este texto: {texto_extraido[:5000]}"
                        
                        # Chamada simples para a API
                        response = model.generate_content(prompt)
                        
                        st.markdown("---")
                        st.markdown("### 🚀 Resultado:")
                        st.write(response.text)
            else:
                st.error("Não foi possível ler o texto do arquivo.")
    except Exception as e:
        st.error(f"Erro de conexão: {e}")
else:
    st.info("Aguardando chave da API.")
