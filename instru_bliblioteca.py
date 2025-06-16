
import streamlit as st
import re
import time
import hashlib
import bcrypt  
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

firebase_config = st.secrets["firebase"].copy()
firebase_config["private_key"] = firebase_config["private_key"].replace("\\n", "\n")

if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_config)
    firebase_admin.initialize_app(cred)
db = firestore.client()




def gerar_hash(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def registrar_atividade(email):
    agora = datetime.now().isoformat()
    ref = db.collection("sessoes_ativas").document(email)
    doc = ref.get()
    if doc.exists:
        ref.update({ "ultima_atividade": agora })
    else:
        ref.set({ "email": email, "ultima_atividade": agora })

def css():
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
    usuarios_ref = db.collection("usuarios").where("email", "==", email).stream()
    user = None
    for doc in usuarios_ref:
        user = doc.to_dict()
        break

    if user:
        if bcrypt.checkpw(senha.encode('utf-8'), user['senha'].encode('utf-8')):
            with st.spinner("Login Bem-Sucedido! Redirecionando..."):
                time.sleep(3)
                registrar_atividade(email)
                st.session_state["logado"] = True
                st.session_state["admin"] = user["admin"]
                st.session_state["nome"] = user["nome"]
                st.session_state["email"] = email
                st.switch_page("pages/main.py")
        else:
            st.error("Senha incorreta.")
    else:
        st.error("Usuário não cadastrado.")

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
    docs = db.collection("sessoes_ativas").stream()
    return sum(1 for _ in docs)
