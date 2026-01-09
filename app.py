import streamlit as st
import requests
from PyPDF2 import PdfReader
from docx import Document

# =====================================================
# CONFIGURAÇÃO DO APP
# =====================================================
st.set_page_config(
    page_title="FAMORTISCO AI",
    layout="centered"
)

st.title("FAMORTISCO AI")
st.subheader("Análise de PDF e DOCX com IA (Gemini)")

# =====================================================
# CHAVE DA API (STREAMLIT SECRETS)
# =====================================================
API_KEY = st.secrets.get("GOOGLE_API_KEY")

if not API_KEY:
    st.error("G
