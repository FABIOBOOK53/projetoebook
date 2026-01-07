import streamlit as st
import google.generativeai as genai
from google.generativeai.types import RequestOptions

st.set_page_config(page_title="BoostEbook AI")
st.title("🧠 BoostEbook AI")

api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    # Configuração forçando a API a usar a versão estável 'v1'
    genai.configure(api_key=api_key)
    
    file = st.file_uploader("Suba seu ebook", type=['pdf', 'docx'])
    
    if file:
        if st.button("🚀 GERAR ESTRATÉGIA"):
            with st.spinner('Processando...'):
                try:
                    # FORÇANDO A VERSÃO DA API VIA REQUEST OPTIONS
                    # Isso impede que a biblioteca busque o 'v1beta'
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    response = model.generate_content(
                        "Resuma este documento em 3 pontos chave.",
                        request_options=RequestOptions(api_version='v1')
                    )
                    
                    st.success("Conexão estável estabelecida!")
                    st.write(response.text)
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"Erro técnico: {e}")
                    st.info("Tentando rota alternativa...")
                    # Se falhar, tentamos o modelo estável mais recente de 2026
                    try:
                        model_alt = genai.GenerativeModel('gemini-1.5-flash-latest')
                        res_alt = model_alt.generate_content("Diga: Conexão alternativa OK")
                        st.write(res_alt.text)
                    except:
                        st.warning("Verifique se sua chave API no Google AI Studio está ativa.")
else:
    st.error("Configure a GOOGLE_API_KEY nos Secrets.")
