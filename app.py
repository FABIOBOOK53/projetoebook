Python
import streamlit as st
import google.generativeai as genai

# Configuração da página
st.set_page_config(page_title="BoostEbook AI - Segredos Obscuros", page_icon="🧠")

# Estilo Dark Mode Personalizado
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { background-color: #6a0dad; color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 BoostEbook AI")
st.subheader("Transforme seu Ebook em Marketing Viral")

# Configurar a API Key (O usuário insere a dele ou você deixa a sua escondida)
api_key = st.sidebar.text_input("Insira sua Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

    uploaded_file = st.file_uploader("Faça upload de um capítulo ou resumo do seu Ebook", type=['txt', 'md'])

    if uploaded_file is not None:
        contexto = uploaded_file.read().decode("utf-8")
        
        if st.button("Gerar Estratégia de Marketing"):
            prompt = f"""
            Você é um especialista em marketing viral e psicologia escura. 
            Baseado neste conteúdo de ebook: '{contexto}', crie:
            1. Uma legenda para Instagram focada em curiosidade.
            2. Um roteiro de 15 segundos para Reels/TikTok.
            3. 3 títulos magnéticos para anúncios.
            Use um tom misterioso, elegante e provocativo.
            """
            
            with st.spinner('A IA está lendo as sombras do seu livro...'):
                response = model.generate_content(prompt)
                st.markdown("### 🚀 Sua Campanha Gerada:")
                st.write(response.text)
else:
    st.warning("Por favor, insira sua chave da API do Google no menu lateral para começar de graça.")
