import streamlit as st
import sqlite3
import hashlib
import secrets
import requests
import smtplib
import urllib.parse
import os
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from PyPDF2 import PdfReader
from docx import Document

# ================= CONFIG =================
st.set_page_config("FAMORTISCO AI", "🐦‍⬛", layout="centered")

API_KEY = st.secrets.get("GOOGLE_API_KEY")
EMAIL_USER = st.secrets.get("EMAIL_REMETENTE")
EMAIL_PASS = st.secrets.get("EMAIL_SENHA")
MEU_ZAP = st.secrets.get("MEU_WHATSAPP", "")
APP_URL = st.secrets.get("APP_URL", "")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ================= DATABASE =================
conn = sqlite3.connect("users.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT,
    plano TEXT DEFAULT 'free',
