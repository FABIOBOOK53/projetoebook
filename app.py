import streamlit as st
import requests
import sqlite3
import os
from PyPDF2 import PdfReader
from docx import Document
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import urllib.parse
from PIL import Image

# ================= CONFIG =================
st.set_page_config(page_title="FAMORTISCO AI", page_icon="🐦‍⬛", layout="centered")

api_key = st.secrets.get("GOOGLE_API_KEY", "")
email_user = st.secrets.get("EMAIL_REMETENTE", "")
email_pass = st.secrets.get("EMAIL_SENHA", "")
meu_zap = st.secrets.get("MEU_WHATSAPP", "")

# ================= DATABASE =================
conn = sqlite3.connect("users.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT,
    plano TEXT DEFAULT 'free',
    uso
