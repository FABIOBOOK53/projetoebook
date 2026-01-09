import streamlit as st
from PyPDF2 import PdfReader
from docx import Document
import requests

st.set_page_config(page_title="FAMORTISCO AI", layout="centered")
st.title("FAMORTISCO AI")
st.write("Teste de upload e geração de estratégia")

# ---------------- API KEY ----------------
API_KEY = st.secrets.get("GOOGLE_API_KEY")
if not API_KEY:
    st.warning("GOOGLE_API_KEY não configurada. O app vai usar modelos fictícios para teste.")

# ---------------- FUNÇÃO PARA LISTAR MODELOS ----------------
def listar_modelos(api_key):
    if not api_key:
        # Chave não configurada → retorna modelos fictícios
        return ["modelo-teste-001", "modelo-teste-002"]
    try:
        url = f"https://generativelanguage.googleapis.com/v1/models?key={api_key}"
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            modelos = r.json().get("models", [])
            if not modelos:
                # Nenhum modelo real → retornar fictício
                return ["modelo-teste-001", "modelo-teste-002"]
            return [m["name"] for m in modelos]
        else:
            return ["modelo-teste-001", "modelo-teste-002"]
    except:
        return ["modelo-teste-001", "modelo-teste-002"]

# ---------------- FUNÇÃO PARA EXTRAIR TEXTO ----------------
def extrair_texto(arquivo):
    texto = ""
    if arquivo.type == "application/pdf":
        reader = PdfReader(arquivo)
        for p in reader.pages[:5]:
            t = p.extract_text()
            if t:
                texto += t + "\n"
    if arquivo.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(arquivo)
        for p in doc.paragraphs[:50]:
            texto += p.text + "\n"
    return texto.strip()

# ---------------- UPLOAD ----------------
arquivo = st.file_uploader("Envie PDF ou DOCX", type=["pdf","docx"])

# ---------------- LISTAR MODELOS ----------------
modelos_disponiveis = listar_modelos(API_KEY)
st.write("Modelos disponíveis para teste:", modelos_disponiveis)

if modelos_disponiveis:
    modelo_funcional = st.selectbox("Escolha o modelo", modelos_disponiveis)
else:
    st.warning("Nenhum modelo disponível")
    modelo_funcional = None

# ---------------- GERAR ESTRATÉGIA ----------------
if arquivo and modelo_funcional:
    texto = extrair_texto(arquivo)
    if not texto:
        st.warning("Não foi possível extrair texto do arquivo")
    else:
        st.success("Texto extraído com sucesso")

        if st.button("Gerar Estratégia"):
            with st.spinner("Processando..."):
                # ---------------- SE MODELO REAL DISPONÍVEL ----------------
                if API_KEY and "teste" not in modelo_funcional:
                    url = f"https://generativelanguage.googleapis.com/v1/models/{modelo_funcional}:generateContent"
                    prompt = "Crie uma estratégia prática baseada no texto abaixo:\n\n" + texto[:2000]
                    payload = {"contents":[{"parts":[{"text":prompt}]}]}
                    headers = {"Content-Type":"application/json","x-goog-api-key":API_KEY}
                    try:
                        r = requests.post(url, headers=headers, json=payload, timeout=60)
                        if r.status_code == 200:
                            resultado = r.json()["candidates"][0]["content"]["parts"][0]["text"]
                            st.text_area("Resultado da IA", resultado, height=400)
                        else:
                            st.error(f"Erro ao chamar a IA: {r.status_code}")
                            st.code(r.text)
                    except Exception as e:
                        st.error(f"Erro de conexão: {e}")
                # ---------------- SE MODELO FICTÍCIO ----------------
                else:
                    st.info("Simulando resultado com modelo fictício")
                    resultado = (
                        "Este é um resultado simulado da IA.\n\n"
                        "Resumo do seu arquivo:\n" + texto[:500]
                    )
                    st.text_area("Resultado da IA (simulado)", resultado, height=400)
