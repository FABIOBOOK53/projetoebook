import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader

st.set_page_config(page_title="BoostEbook AI")
st.title("🧠 BoostEbook AI - Modo Estável")

# Puxa a chave dos Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    # Configura o cliente para usar o endpoint do Google via protocolo OpenAI
    client = OpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    
    file = st.file_uploader("Suba seu ebook (PDF)", type=['pdf'])
    
    if file:
        try:
            reader = PdfReader(file)
            texto = "".join([p.extract_text() for p in reader.pages])
            st.success("✅ Conteúdo lido!")
            
            if st.button("🚀 GERAR ESTRATÉGIA"):
                with st.spinner('IA Processando...'):
                    response = client.chat.completions.create(
                        model="gemini-1.5-flash",
                        messages=[
                            {"role": "system", "content": "Você é um especialista em marketing."},
                            {"role": "user", "content": f"Crie uma estratégia para este conteúdo: {texto[:4000]}"}
                        ]
                    )
                    st.subheader("Sua Estratégia:")
                    st.write(response.choices[0].message.content)
                    st.balloons()
        except Exception as e:
            st.error(f"Erro: {e}")
else:
    st.error("Configure a GOOGLE_API_KEY nos Secrets.")
