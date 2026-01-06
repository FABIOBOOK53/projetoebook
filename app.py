import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document
import io

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

# Configuração da API Key (Busca no Secrets do Streamlit)
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = st.sidebar.text_input("Insira sua Gemini API Key", type="password")

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
        st.error(f"Erro ao ler arquivo: {e}")
    return None

if api_key:
    try:
        # Configuração da IA com o modelo mais estável
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        uploaded_file = st.file_uploader("Faça upload do seu Ebook (PDF, Word ou TXT)", type=['txt', 'pdf', 'docx'])

        if uploaded_file is not None:
            contexto = extrair_texto(uploaded_file)
            
            if contexto:
                st.success("Conteúdo carregado com sucesso!")
                if st.button("Gerar Estratégia de Marketing"):
                    # Limitamos o texto para evitar erros de limite da API
                    prompt = f"""
                    Você é um especialista em marketing viral. 
                    Baseado neste conteúdo: '{contexto[:8000]}', crie:
                    1. Uma legenda para Instagram focada em curiosidade.
                    2. Um roteiro de 15 segundos para Reels/TikTok.
                    3. 3 títulos magnéticos para anúncios.
                    Use um tom misterioso, elegante e provocativo.
                    """
                    
                    with st.spinner('A IA está analisando seu conteúdo...'):
                        # Chamada simplificada para evitar erro de versão
                        response = model.generate_content(prompt)
                        st.markdown("---")
                        st.markdown("### 🚀 Sua Campanha Gerada:")
                        st.write(response.text)
            else:
                st.warning("Não foi possível extrair texto deste arquivo.")
    except Exception as e:
        # Se der erro 404, avisamos de forma clara
        if "404" in str(e):
            st.error("Erro: Modelo não encontrado. Verifique se sua API Key está ativa no Google AI Studio.")
        else:
            st.error(f"Erro na IA: {e}")
else:
    st.info("Aguardando configuração da API Key.")
