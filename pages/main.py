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

    st.title("Créditos")
    
    st.markdown("Desenvolvedores")
    st.markdown("""
    - Bianca de Oliveira Almeida - Programação da calculadora, desenvolvendo os cálculos e gráficos e programação da página de créditos.
    - Eduardo da Silva Oliveira  - Progrmação da Pagina de Login e Cadastro, Otimização da pagina e Inegração ao banco de dados de forma Online.
    """)

    st.markdown("Sobre os desenvolvedores")
    st.markdown("""
    - Bianca de Oliveira Almeida - "Estudante do curso técnico em Desenvolvimento de Sistemas do SENAI Jairo Cândido, tenho foco em construção de aplicações web. Tenho experiência no desenvolvimento de interfaces responsivas utilizando HTML, CSS e JavaScript, além de conhecimentos em integração com back-end em linguagens como Python e PHP."
    - Eduardo da Silva Oliveira  -"Estudante do curso técnico em Desenvolvimento de Sistemas do SENAI Jairo Cândido,focado no momento na linguagem Python e Banco de Dados com uma experiência boa. Buscando mexer com HTML, CSS e C++ ."
    """)

    st.markdown("Bibliotecas Utilizadas")
    st.markdown("""
    - [Streamlit](https://streamlit.io/) – Criação da interface interativa  
    - [Pandas](https://pandas.pydata.org/) – Manipulação e análise de dados  
    - [NumPy](https://numpy.org/) – Cálculos matemáticos e estatísticos  
    - [Matplotlib](https://matplotlib.org/) e [Seaborn](https://seaborn.pydata.org/) – Visualização gráfica  
    - [Scikit-learn](https://scikit-learn.org/) – Modelos de regressão linear  
    - [SciPy](https://scipy.org/) – Estatística e intervalos de confiança
    """)

    st.markdown("Agradecimentos")
    st.markdown("""
    Agradecemos a todos que contribuíram direta ou indiretamente para o desenvolvimento deste site, em especial, ao professor Fabiano Luizon Campos, no qual foi docente responsável por nos guiar nesse projeto, e ao Everton [...], por solicitar o projeto e nos guiar quanto ao conteúdo do mesmo.
    Este site foi feito e pensado para cumprir com a função de ajudar a produção de projetos e cálculos para a turma de Instrumentação do SENAI Jairo Cândido, cursando em 2025.
    Para dúvidas, sugestões ou contribuições, entre em contato com os desenvolvedores.  
    """)


elif st.session_state.pagina =="menu":
    st.title("Bem Vindo!!!")
    st.divider()
    st.markdown(f"## Olá, :red[{st.session_state['nome']}!] O que você gostaria de fazer hoje?")
    if st.session_state.get("admin"):  
        total = bl.contar_usuarios_online()
        st.success(f"{total} Usuarios Logados nesse momento")



st.caption("")
