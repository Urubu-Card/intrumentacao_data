import streamlit as st

def pagina_creditos():
    st.title("Créditos")
    
    st.markdown("Desenvolvedores")
    st.markdown("""
    - Bianca de Oliveira Almeida - Programação da calculadora, desenvolvendo os cálculos e gráficos e programação da página de créditos.
    - Eduardo da Silva Oliveira  - Progrmação da Pagina de Login e Cadastro, Otimização da pagina, Inegração ao banco de dados de forma Online, 
    """)

    st.markdown("Sobre os desenvolvedores")
    st.markdown("""
    - Bianca de Oliveira Almeida - "Estudante do curso técnico em Desenvolvimento de Sistemas do SENAI Jairo Cândido, tenho foco em construção de aplicações web. Tenho experiência no desenvolvimento de interfaces responsivas utilizando HTML, CSS e JavaScript, além de conhecimentos em integração com back-end em linguagens como Python e PHP."
    - Eduardo -
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


if __name__ == "__main__":
    pagina_creditos()
