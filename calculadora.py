def calculadora():

    import streamlit as st
    import numpy as np
    import matplotlib.pyplot as plt
    import scipy.stats as stats

    
    # Detecta o tema atual do Streamlit ('light' ou 'dark')
    tema = st.get_option('theme.base')

    def deixar_virgula(num):
        return str(round(num,4)).replace('.',',')

    # Define cores e estilos conforme o tema
    def cores_por_tema(tema):
        if tema == 'dark':
            return {
                'fundo_fig': 'none',
                'cor_fundo_ax': 'none',
                'cor_texto': 'white',
                'cor_borda': 'white',
                'cor_hist': '#8051b5',
                'cor_media': 'red',
                'cor_regressao': 'orange',
                'cor_scatter': 'purple',
                'cor_fill': '#8E38F0FF',
                'cor_intervalo': 'yellow',
                'cor_edge_hist': 'white'
            }
        else:
            return {
                'fundo_fig': 'white',
                'cor_fundo_ax': 'white',
                'cor_texto': 'black',
                'cor_borda': 'black',
                'cor_hist': '#5a2a8a',
                'cor_media': 'red',
                'cor_regressao': 'orange',
                'cor_scatter': 'purple',
                'cor_fill': '#c8a8f9',
                'cor_intervalo': 'gold',
                'cor_edge_hist': 'black'
            }

    cores = cores_por_tema(tema)

    # ------------------- INICIALIZAÇÃO DA SESSÃO -------------------

    if "mostrar_resultado" not in st.session_state:
        st.session_state.mostrar_resultado = False

    # ------------------- CONFIGURAÇÃO DA PÁGINA -------------------

    st.title("Calculadora Estatística : ")
    st.write("Insira dados para calcular média, variância, desvio padrão, incertezas e visualizar gráficos.")

    # ------------------- INTERFACE INICIAL -------------------

    st.subheader("1. Escolha se as informações que ira querer serão resultados como População ou como Amostra :")
    esco = st.selectbox("Selecione entre População ou Amostra : ",("População","Amostra"))

    st.subheader("2. Escolha a quantidade de valores e insira os dados")
    qtd = st.selectbox("Selecione a quantidade de valores (2 a 50):", options=list(range(2, 51)), key="qtd")
    valores = []
    cols = st.columns(9)

    for i in range(qtd):
        col = cols[i % 9]
        with col:
            num = st.number_input(f"{i+1}° Valor", key=f"valor_{i}", step=0.01)
            valores.append(num)

    if st.button("Confirmar e calcular"):
        st.session_state.mostrar_resultado = True
        st.session_state.valores = valores

    # ------------------- RESULTADOS -------------------

    if st.session_state.mostrar_resultado:

        dados = np.array(st.session_state.valores)
        n = len(dados)
        media = np.mean(dados)

        # População
        var_pop = np.var(dados)
        desvio_pop = np.std(dados)

        # Amostra
        var_amostral = np.var(dados, ddof=1)
        desvio_amostral = np.std(dados, ddof=1)

        # Incerteza padrão
        u_padrao = desvio_amostral / np.sqrt(n)

        # Incerteza expandida (k=2)
        k = 2
        u_expandida = k * u_padrao

        # Intervalo de confiança (95%) com t de Student
        gl = n - 1
        t_student = stats.t.ppf(0.975, df=gl)  # 95% bilateral
        margem_erro = t_student * u_padrao
        intervalo = (media - margem_erro, media + margem_erro)

        st.divider()
        st.subheader("Resultados Estatísticos : ")

        st.markdown(f"### **Média :** {deixar_virgula(media)}")
        st.divider()
        col1, col2 = st.columns(2)

        if esco == "População":
            st.markdown("### Cálculos como População:")
            st.markdown(f"### Variância:  {deixar_virgula(var_pop)}")
            st.markdown(f"### Desvio padrão: {deixar_virgula(desvio_pop)}")
        elif esco == "Amostra":
            st.markdown("### Cálculos como Amostra:")
            st.markdown(f"### Variância: {deixar_virgula(var_amostral)}")
            st.markdown(f"### Desvio padrão: {deixar_virgula(desvio_amostral)}")
            st.markdown(f"### Incerteza padrão (u): {deixar_virgula(u_padrao)}")
            st.markdown(f"### Incerteza expandida (U, k=2): {deixar_virgula(u_expandida)}")
            st.markdown(f"### Intervalo de confiança 95%: [{deixar_virgula(intervalo[0])}, {deixar_virgula  (intervalo[1])}]")

        # ------------------- GRÁFICO 1: HISTOGRAMA + MÉDIA -------------------

        fig1, ax1 = plt.subplots(facecolor=cores['fundo_fig'])
        ax1.set_facecolor(cores['cor_fundo_ax'])
        ax1.spines['bottom'].set_color(cores['cor_borda'])
        ax1.spines['left'].set_color(cores['cor_borda'])
        ax1.xaxis.label.set_color(cores['cor_texto'])
        ax1.yaxis.label.set_color(cores['cor_texto'])
        ax1.title.set_color(cores['cor_texto'])
        ax1.tick_params(axis='x', colors=cores['cor_texto'])
        ax1.tick_params(axis='y', colors=cores['cor_texto'])

        ax1.hist(dados, bins='auto', color=cores['cor_hist'], edgecolor=cores['cor_edge_hist'])
        ax1.axvline(media, color=cores['cor_media'], linestyle='--', label='Média')
        ax1.set_title("Histograma dos Valores")
        ax1.set_xlabel("Valor")
        ax1.set_ylabel("Frequência")
        ax1.legend()
        st.pyplot(fig1)

        # ------------------- GRÁFICO 2: CURVA GAUSSIANA -------------------

        x = np.linspace(min(dados), max(dados), 100)
        y = stats.norm.pdf(x, media, desvio_amostral)

        fig2, ax2 = plt.subplots(facecolor=cores['fundo_fig'])
        ax2.set_facecolor(cores['cor_fundo_ax'])
        ax2.spines['bottom'].set_color(cores['cor_borda'])
        ax2.spines['left'].set_color(cores['cor_borda'])
        ax2.xaxis.label.set_color(cores['cor_texto'])
        ax2.yaxis.label.set_color(cores['cor_texto'])
        ax2.title.set_color(cores['cor_texto'])
        ax2.tick_params(axis='x', colors=cores['cor_texto'])
        ax2.tick_params(axis='y', colors=cores['cor_texto'])

        ax2.plot(x, y, color=cores['cor_hist'], label='Curva Gaussiana')
        ax2.axvline(media, color=cores['cor_media'], linestyle='--', label='Média')
        ax2.fill_between(x, y, alpha=0.2, color=cores['cor_fill'])
        ax2.set_title("Distribuição Normal (Curva Gaussiana)")
        ax2.set_xlabel("Valor")
        ax2.set_ylabel("Densidade de Probabilidade")
        ax2.legend()
        st.pyplot(fig2)

        # ------------------- GRÁFICO 3: INTERVALO DE CONFIANÇA -------------------

        fig3, ax3 = plt.subplots(facecolor=cores['fundo_fig'])
        ax3.set_facecolor(cores['cor_fundo_ax'])
        ax3.spines['bottom'].set_color(cores['cor_borda'])
        ax3.spines['left'].set_color(cores['cor_borda'])
        ax3.xaxis.label.set_color(cores['cor_texto'])
        ax3.yaxis.label.set_color(cores['cor_texto'])
        ax3.title.set_color(cores['cor_texto'])
        ax3.tick_params(axis='x', colors=cores['cor_texto'])
        ax3.tick_params(axis='y', colors=cores['cor_texto'])

        ax3.hist(dados, bins='auto', color='lightgray', edgecolor='black')
        ax3.axvline(media, color='blue', linestyle='--', label='Média')
        ax3.axvspan(intervalo[0], intervalo[1], color=cores['cor_intervalo'], alpha=0.4, label='Intervalo 95%')
        ax3.set_title("Intervalo de Confiança 95%")
        ax3.set_xlabel("Valor")
        ax3.set_ylabel("Frequência")
        ax3.legend()
        st.pyplot(fig3)

        # ------------------- GRÁFICO 4: DISPERSÃO + REGRESSÃO LINEAR -------------------

        x_simulado = np.arange(1, n + 1)
        y_simulado = dados
        coef = np.polyfit(x_simulado, y_simulado, deg=1)
        y_pred = np.polyval(coef, x_simulado)

        fig4, ax4 = plt.subplots(facecolor=cores['fundo_fig'])
        ax4.set_facecolor(cores['cor_fundo_ax'])
        ax4.spines['bottom'].set_color(cores['cor_borda'])
        ax4.spines['left'].set_color(cores['cor_borda'])
        ax4.xaxis.label.set_color(cores['cor_texto'])
        ax4.yaxis.label.set_color(cores['cor_texto'])
        ax4.title.set_color(cores['cor_texto'])
        ax4.tick_params(axis='x', colors=cores['cor_texto'])
        ax4.tick_params(axis='y', colors=cores['cor_texto'])

        ax4.scatter(x_simulado, y_simulado, color=cores['cor_scatter'], label='Dados')
        ax4.plot(x_simulado, y_pred, color=cores['cor_regressao'], label='Regressão Linear')
        ax4.set_title("Regressão Linear Simulada")
        ax4.set_xlabel("Índice")
        ax4.set_ylabel("Valor")
        ax4.legend()
        st.pyplot(fig4)

        from fpdf import FPDF
        import io

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Relatório Estatístico", ln=True, align="C")
        pdf.ln(10)
        pdf.set_font("Arial", "", 12)

        pdf.cell(0, 10, f"Média: {deixar_virgula(media)}", ln=True)

        if esco == "População":
            pdf.cell(0, 10, f"Variância (População): {deixar_virgula(var_pop)}", ln=True)
            pdf.cell(0, 10, f"Desvio padrão (População): {deixar_virgula(desvio_pop)}", ln=True)
        else:
            pdf.cell(0, 10, f"Variância (Amostra): {deixar_virgula(var_amostral)}", ln=True)
            pdf.cell(0, 10, f"Desvio padrão (Amostra): {deixar_virgula(desvio_amostral)}", ln=True)
            pdf.cell(0, 10, f"Incerteza padrão (u): {deixar_virgula(u_padrao)}", ln=True)
            pdf.cell(0, 10, f"Incerteza expandida (U, k=2): {deixar_virgula(u_expandida)}", ln=True)
            pdf.cell(0, 10, f"Intervalo de confiança 95%:", ln=True)
            pdf.cell(0, 10, f"[{deixar_virgula(intervalo[0])} , {deixar_virgula(intervalo[1])}]", ln=True)

        # Gerar o arquivo em memória
        buffer = io.BytesIO()
        pdf.output(buffer)
        buffer.seek(0)

        st.download_button(
            label="📄 Baixar relatório em PDF",
            data=buffer,
            file_name="relatorio_estatistico.pdf",
            mime="application/pdf"
        )


