
import streamlit as st
import re
import time
import bcrypt
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

firebase_config = st.secrets["firebase"]

if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_config)
    firebase_admin.initialize_app(cred)

db = firestore.client()
def validar_email(email):
    padrao = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(padrao, email) is not None

def adicionar_no_DB(nome, email, senha, admin=False):
    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    contador_ref = db.collection("controle").document("contador_usuarios")
    doc = contador_ref.get()
    ultimo_id = doc.to_dict().get("ultimo_id", 0) if doc.exists else 0
    novo_id = ultimo_id + 1

    db.collection("usuarios").document(str(novo_id)).set({
        "nome": nome,
        "email": email,
        "senha": senha_hash,
        "admin": admin
    })

    contador_ref.set({ "ultimo_id": novo_id })
    st.success("✅ Usuário adicionado com sucesso!")

def stpesq():
    st.subheader("Cadastro de novo usuário:")
    nome = st.text_input("Nome do usuário:")
    email = st.text_input("E-mail do usuário:")
    senha = st.text_input("Senha:", type="password")
    admin = st.checkbox("É administrador?")

    if st.button("Adicionar usuário"):
        if not nome or not email or not senha:
            st.error("Preencha todos os campos.")
        elif not validar_email(email):
            st.error("O e-mail não é válido.")
        else:
            adicionar_no_DB(nome, email, senha, admin)

def stdeletar():
    st.subheader("Qual é o ID do usuário que deseja deletar? ")
    delid = st.number_input("ID do usuário:", min_value=1, step=1, label_visibility="collapsed")

    if "confirmar_delete" not in st.session_state:
        st.session_state.confirmar_delete = False
        st.session_state.id_para_deletar = None

    if st.button("Deletar usuário"):
        st.session_state.confirmar_delete = True
        st.session_state.id_para_deletar = delid
        st.info(f"Certeza que deseja deletar o usuário com o ID: {delid} (Ação irreversível).")

    if st.session_state.confirmar_delete:
        if st.button("Sim, eu tenho certeza."):
            doc_ref = db.collection("usuarios").document(str(st.session_state.id_para_deletar))
            if doc_ref.get().exists:
                doc_ref.delete()
                st.success("✅ Usuário deletado com sucesso!")
            else:
                st.warning("Usuário não encontrado.")

            # Resetar confirmação após deletar
            st.session_state.confirmar_delete = False
            st.session_state.id_para_deletar = None

@st.cache_data(ttl=10)
def stlistar():
    st.subheader("Lista de Usuários :")
    docs = db.collection("usuarios").stream()
    dados = []
    for doc in docs:
        user = doc.to_dict()
        user["id"] = doc.id
        dados.append(user)

    if dados:
        df = pd.DataFrame(dados)
        st.dataframe(df)
    else:
        st.warning("Nenhum usuário cadastrado.")

def stpri():
    st.subheader("Menu do Admin:")
    escolha = st.selectbox("Qual ação deseja fazer?", ("Adicionar novo usuário", "Listar todos os usuários", "Deletar um usuário"))

    if escolha == "Adicionar novo usuário":
        stpesq()
    elif escolha == "Listar todos os usuários":
        stlistar()
    elif escolha == "Deletar um usuário":
        stdeletar()
