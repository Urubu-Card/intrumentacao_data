import streamlit as st
import re
import time
from sqlalchemy import create_engine
import pandas as pd
import hashlib
import bcrypt  
from datetime import datetime
import os



def gerar_hash(senha):
    return hashlib.sha256(senha.encode()).hexdigest()



@st.cache_resource
def pega_db():
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        st.error("Erro não conectado")
        st.stop()
    return create_engine(DATABASE_URL)


def conCursor():
    return pega_db()



def registrar_atividade(email):
    engine = conCursor()
    agora = datetime.now()
    conn = engine.raw_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sessoes_ativas WHERE email = %s", (email,))
    result = cursor.fetchone()
    if result:
        cursor.execute("UPDATE sessoes_ativas SET ultima_atividade = %s WHERE email = %s", (agora, email))
    else:
        cursor.execute("INSERT INTO sessoes_ativas (email, ultima_atividade) VALUES (%s, %s)", (email, agora))
    conn.commit()
    cursor.close()
    conn.close()

def css():
    is_dark = st.get_option("theme.base") == "dark"
    st.markdown("""
        <style>
        .login-title {
            text-align: center;
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .stButton>button {
            background-color: #262730;
            color: white;
            border: none;
            padding: 15px 32px;
            text-align: center;
            font-size: 32px;
            cursor: pointer;
            border-radius: 8px;
            width: 200px;
        }
        .stButton {
            display: flex;
            justify-content: center;
        }
        </style>
    """, unsafe_allow_html=True)

def titulo():
    st.markdown('<div class="login-title">Login :</div>', unsafe_allow_html=True)

def validar_email(email):
    padrao = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(padrao, email) is not None

def verificar_no_db(email, senha):
    engine = conCursor()
    conn = engine.raw_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT nome, senha, admin FROM usuarios WHERE email = %s", (email,))
        result = cursor.fetchone()
    except Exception as e:
        st.error(f"Erro ao consultar o banco de dados: {e}")
        cursor.close()
        conn.close()
        return
    if result:
        nome, senha_hash, admin = result
        if bcrypt.checkpw(senha.encode('utf-8'), senha_hash.encode('utf-8')):
            with st.spinner("Login Bem-Sucedido! Redirecionando..."):
                time.sleep(3)
                registrar_atividade(email)
                st.session_state["logado"] = True
                st.session_state["admin"] = admin
                st.session_state["nome"] = nome
                st.session_state["email"] = email
                st.page_link("http://www.google.com")
        else:
            st.error("Senha incorreta.")
    else:
        st.error("Usuário não cadastrado.")
    cursor.close()
    conn.close()

def login1():
    email = st.text_input("E-Mail : ")
    senha = st.text_input("Senha : ", type="password")
    if st.button("Entrar"):
        if not email or not senha:
            st.error("Erro : E-mail ou senha não inseridos.")   
        elif not validar_email(email):
            st.error("Erro : O e-mail digitado não é válido!")
        else:
            verificar_no_db(email, senha)
    return email

def contar_usuarios_online():
    engine = conCursor()
    conn = engine.raw_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM sessoes_ativas")
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado[0] if resultado else 0
