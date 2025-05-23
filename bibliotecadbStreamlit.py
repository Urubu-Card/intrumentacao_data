import streamlit as st
import re
import time
import bcrypt
import pandas as pd
from sqlalchemy import create_engine, text
import os 


DATABASE_URL = os.getenv("DATABASE_URL")


@st.cache_resource
def engine_pega():
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        st.error("Erro não conectado")
        st.stop()
    return create_engine(DATABASE_URL)

def conCursor():
    return engine_pega()

def validar_email(email):
    padrao = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(padrao, email) is not None

def adicionar_no_DB(nome, email, senha, admin=False):
    senha_bytes = senha.encode('utf-8')
    senha_hash = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())

    engine = conCursor()
    adicionar = "INSERT INTO usuarios (nome, email, senha, admin) VALUES (%s, %s, %s, %s)"

    conn = engine.raw_connection()
    cursor = conn.cursor()
    cursor.execute(adicionar, (nome, email, senha_hash.decode('utf-8'), admin))
    conn.commit()
    cursor.close()
    conn.close()

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
    engine = conCursor()

    st.subheader("Qual é o ID do usuário que deseja deletar? ")
    delid = st.number_input("ID do usuário:", min_value=1, step=1, label_visibility="collapsed")

    if 'deletar_confirmado' not in st.session_state:
        st.session_state.deletar_confirmado = False

    if delid and st.button("Deletar usuário"):
        buscar = "SELECT * FROM usuarios WHERE id = %s"
        resubusca = pd.read_sql(buscar, engine, params=(delid,))

        if not resubusca.empty:
            st.warning("Tem certeza que deseja deletar esse usuário? Não será possível recuperá-lo depois.")
            st.session_state.delid_pendente = delid
            st.session_state.confirmacao_pendente = True

    if st.session_state.get("confirmacao_pendente", False):
        if st.button("Sim, eu tenho certeza."):
            try:
                with engine.begin() as conn:
                    conn.execute(
                        text("DELETE FROM usuarios WHERE id = :id"),
                        {"id": st.session_state.delid_pendente}
                    )
                st.success("✅ Usuário deletado com sucesso!")
            except Exception as e:
                st.error(f"Erro ao deletar: {e}")

            st.session_state.confirmacao_pendente = False
            st.session_state.delid_pendente = None


@st.cache_data(ttl=10)
def stlistar():
    engine = conCursor()

    st.subheader("Lista de Usuários:")
    lista = "SELECT * FROM usuarios"
    listagem = pd.read_sql(lista, engine)

    if not listagem.empty:
        st.dataframe(listagem)
    else:
        st.error("Nenhum usuário cadastrado.")

def stpri():
    st.subheader("Menu do Admin:")
    escolha = st.selectbox("Qual ação deseja fazer?", ("Adicionar novo usuário", "Listar todos os usuários", "Deletar um usuário"))

    if escolha == "Adicionar novo usuário":
        stpesq()
    elif escolha == "Listar todos os usuários":
        stlistar()
    elif escolha == "Deletar um usuário":
        stdeletar()


