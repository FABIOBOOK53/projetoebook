import streamlit as st
import google.generativeai as genai

# Configuração da interface
st.set_page_config(page_title="BoostEbook AI", layout="centered")
st.title("🧠 BoostEbook AI")

# Recupera a chave dos Secrets do Streamlit
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    # Configura a biblioteca para usar a versão estável
    genai.configure(api_key=api_key)
    
    file = st.file_uploader("Suba seu ebook", type=['pdf', 'docx'])
    
    if file:
        if st.button("🚀 GERAR ESTRATÉGIA"):
            with st.spinner('A IA está analisando seu conteúdo...'):
                try:
                    # Chamada direta ao modelo estável (evita o erro v1beta)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    # Teste rápido de resposta
                    response = model.generate_content("Olá! O sistema está pronto. Diga 'Conexão OK'!")
                    
                    st.success("✅ Conexão estabelecida com sucesso!")
                    st.write(response.text)
                    st.balloons()
                except Exception as e:
                    st.error(f"Erro na conexão: {e}")
                    st.info("Verifique se sua chave API está correta nas Configurações Avançadas.")
else:
    st.error("Chave API não configurada. Vá em 'Advanced settings' no Streamlit e adicione GOOGLE_API_KEY.")
