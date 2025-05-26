import streamlit as st

st.set_page_config(page_icon=":material/menu:",page_title="Menu",layout="centered")  #Pra nao dar erro né patrão

import instru_bliblioteca as bl

import calculadora as calc

import adicionarUsuariosStreamLit as adicionar

if "logado" not in st.session_state or not st.session_state["logado"]:
    st.warning("Você precisa fazer login primeiro.")
    st.page_link("https://entrar.streamlit.app", label="Voltar ao login", icon="⚠")
    st.stop()





bl.css()


if "pagina" not in st.session_state:
    st.session_state.pagina = "menu"

with st.sidebar:
    st.title("Menu: ")
    st.markdown("### Escolha para onde deseja ir : ")
    if st.button("Ir para a Calculadora Estatística", icon=":material/calculate:"):
        st.session_state.pagina = "calculadora"
    if st.session_state.get("admin"):  
        if st.button("Adicionar usuario : ",icon=":material/terminal:"):
            st.session_state.pagina = "adduser"

if st.session_state.pagina == "calculadora":
    calc.calculadora()

elif st.session_state.pagina == ("adduser"):
    adicionar.usuario()


else:
    st.title("Bem Vindo!!!")
    st.divider()
    st.markdown(f"## Olá, :red[{st.session_state['nome']}!] O que você gostaria de fazer hoje?")
    if st.session_state.get("admin"):  
        total = bl.contar_usuarios_online()
        st.success(f"{total} Usuarios Logados nesse momento")
