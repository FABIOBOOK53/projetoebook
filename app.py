import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document
import io

# Configuração da página
st.set_page_config(page_title="BoostEbook AI - Segredos Obscuros", page_icon="🧠")

# Estilo Dark Mode
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { background-color: #6a0dad; color: white; border-radius: 10px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 BoostEbook AI")
st.subheader("Transforme seu Ebook em Marketing Viral")

# Configuração da API Key automática
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = st.sidebar.text_input("Insira sua Gemini API Key", type="password")

# Função para extrair texto de diferentes arquivos
def extrair_texto(arquivo):
    nome_extensao = arquivo.name.lower()
    try:
        if nome_extensao.endswith('.txt'):
            return arquivo.read().decode("utf-8")
        elif nome_extensao.endswith('.pdf'):
            pdf_reader = PdfReader(arquivo)
            texto = ""
            for page in pdf_reader.pages:
                texto += page.extract_text() or ""
            return texto
        elif nome_extensao.endswith('.docx'):
            doc = Document(arquivo)
            return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")
    return None

if api_key:
    try:
        genai.configure(api_key=api_key)
        # Usando o modelo flash que é mais moderno e evita o erro 404 das imagens
        model = genai.GenerativeModel('gemini-1.5-flash')

        uploaded_file = st.file_uploader("Faça upload do seu Ebook (PDF, Word ou TXT)", type=['txt', 'pdf', 'docx'])

        if uploaded_file is not None:
            with st.spinner('Lendo conteúdo...'):
                contexto = extrair_texto(uploaded_file)
            
            if contexto:
                if st.button("Gerar Estratégia de Marketing"):
                    # Limitamos o texto para não estourar a memória da IA
                    prompt = f"""
                    Você é um especialista em marketing viral. 
                    Baseado neste conteúdo: '{contexto[:8000]}', crie:
                    1. Uma legenda para Instagram (curiosidade).
                    2. Um roteiro de 15 segundos para Reels.
                    3. 3 títulos magnéticos para anúncios.
                    Use um tom misterioso e provocativo.
                    """
                    
                    with st.spinner('A IA está criando sua campanha...'):
                        response = model.generate_content(prompt)
                        st.markdown("---")
                        st.markdown("### 🚀 Sua Campanha Gerada:")
                        st.write(response.text)
            else:
                st.warning("O arquivo parece estar vazio ou não pôde ser lido.")
    except Exception as e:
        st.error(f"Erro na IA: {e}")
else:
    st.info("Aguardando Chave da API...")
