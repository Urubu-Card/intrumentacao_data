import streamlit as st

st.set_page_config(page_icon=":material/menu:",page_title="Menu",layout="centered")  #Pra nao dar erro né patrão

import instru_bliblioteca as bl

import calculadora as calc

import adicionarUsuariosStreamLit as adicionar

if "logado" not in st.session_state or not st.session_state["logado"]:
    st.warning("Você precisa fazer login primeiro.")
    st.page_link("instumentacao_login.py", label="Voltar ao login", icon="⚠")
    st.stop()




bl.css()


if "pagina" not in st.session_state:
    st.session_state.pagina = "menu"




with st.sidebar:
    st.title("Menu: ")
    st.markdown("### Escolha para onde deseja ir : ")
    if st.button("Menu",icon=":material/home:"):
        st.session_state.pagina = "menu"
    if st.button("Ir para a Calculadora Estatística", icon=":material/calculate:"):
        st.session_state.pagina = "calculadora"
    if st.session_state.get("admin"):  
        if st.button("Adicionar usuario : ",icon=":material/terminal:"):
            st.session_state.pagina = "adduser"
    if st.button("Creditos : ",icon=":material/group:"):
        st.session_state.pagina = "creditos"




if st.session_state.pagina == "calculadora":
    calc.calculadora()


elif st.session_state.pagina == ("adduser"):
    adicionar.usuario()


elif st.session_state.pagina == "creditos":
    st.markdown('''
        <style>
        .login-title1 {
            text-align: center;
            font-size: 48px;
            font-weight: bold;
            margin-bottom: 15px;
        }
        </style>
                ''',unsafe_allow_html=True)


    st.markdown('<div class="login-title1">Créditos :</div>', unsafe_allow_html=True)

    st.markdown("## Programação Base (Parte do Login e Navegação) foi feita por : " \
    "\n ### [:violet[. . . . . .  . . . . .Eduardo da Silva Oliveira. . . . . .  . . . . ..]](https://github.com/Urubu-Card)")
    st.markdown("## Programação dos Calculos (Parte da Calculadora e Graficos) foi feito por : " \
    "\n ### [:red[. . . . . .  . . . . .Bianca de Oliveira Almeida. . . . . .  . . . . .]](https://github.com/Binlameida)")


elif st.session_state.pagina =="menu":
    st.title("Bem Vindo!!!")
    st.divider()
    st.markdown(f"## Olá, :red[{st.session_state['nome']}!] O que você gostaria de fazer hoje?")
    if st.session_state.get("admin"):  
        total = bl.contar_usuarios_online()
        st.success(f"{total} Usuarios Logados nesse momento")



st.caption("")