def calculadora():
    import streamlit as st
    import numpy as np
    import matplotlib.pyplot as plt
    import scipy.stats as stats
    from fpdf import FPDF
    import io
    from datetime import datetime

    # Detecta o tema atual do Streamlit ('light' ou 'dark')
    tema = st.get_option('theme.base')

    def deixar_virgula(num):
        return str(round(num, 4)).replace('.', ',')

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

    # ------------------- Entrada do nome do usuário -------------------
    st.title("Calculadora Estatística Completa")
    usuario = st.text_input("Digite seu nome (usuário):")

    # Inicializa flag mostrar resultado
    if "mostrar_resultado" not in st.session_state:
        st.session_state.mostrar_resultado = False

    # ------------------- Interface inicial -------------------
    st.subheader("1. Escolha se as informações são para População ou Amostra:")
    esco = st.selectbox("Selecione:", ("População", "Amostra"))

    st.subheader("2. Quantidade de valores (2 a 50) e insira os dados")
    qtd = st.selectbox("Quantidade de valores:", options=list(range(2, 51)), key="qtd")
    valores = []
    cols = st.columns(9)

    for i in range(qtd):
        col = cols[i % 9]
        with col:
            num = st.number_input(f"{i + 1}° Valor", key=f"valor_{i}", step=0.01, format="%.4f")
            valores.append(num)

    if st.button("Confirmar e calcular"):
        if usuario.strip() == "":
            st.error("Por favor, digite seu nome antes de calcular.")
        else:
            st.session_state.mostrar_resultado = True
            st.session_state.valores = valores
            st.session_state.usuario = usuario
            st.session_state.esco = esco

    # ------------------- Resultados -------------------
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

        # Incertezas e intervalo (só para amostra)
        u_padrao = desvio_amostral / np.sqrt(n)
        k = 2
        u_expandida = k * u_padrao
        gl = n - 1
        t_student = stats.t.ppf(0.975, df=gl)
        margem_erro = t_student * u_padrao
        intervalo = (media - margem_erro, media + margem_erro)

        st.divider()
        st.subheader("Resultados Estatísticos")

        st.markdown(f"**Usuário:** {st.session_state.usuario}")
        st.markdown(f"**Data/Hora:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        st.markdown(f"### Média: {deixar_virgula(media)}")
        st.divider()

        if st.session_state.esco == "População":
            st.markdown("### Cálculos como População:")
            st.markdown(f"- Variância:  {deixar_virgula(var_pop)}")
            st.markdown(f"- Desvio padrão: {deixar_virgula(desvio_pop)}")
        else:
            st.markdown("### Cálculos como Amostra:")
            st.markdown(f"- Variância: {deixar_virgula(var_amostral)}")
            st.markdown(f"- Desvio padrão: {deixar_virgula(desvio_amostral)}")
            st.markdown(f"- Incerteza padrão (u): {deixar_virgula(u_padrao)}")
            st.markdown(f"- Incerteza expandida (U, k=2): {deixar_virgula(u_expandida)}")
            st.markdown(f"- Intervalo de confiança 95%: [{deixar_virgula(intervalo[0])}, {deixar_virgula(intervalo[1])}]")

        # ------------------- Criação dos gráficos -------------------

        # Gráfico 1 - Histograma + Média
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

        # Gráfico 2 - Curva Gaussiana
        x = np.linspace(min(dados), max(dados), 100)
        y = stats.norm.pdf(x, media, desvio_amostral if st.session_state.esco == "Amostra" else desvio_pop)

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

        # Gráfico 3 - Intervalo de Confiança
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

        # Gráfico 4 - Dispersão + Regressão Linear
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
        ax4.set_title("Dispersão dos Valores e Regressão Linear")
        ax4.set_xlabel("Índice")
        ax4.set_ylabel("Valor")
        ax4.legend()
        st.pyplot(fig4)

        # ------------------- PDF (botão para gerar) -------------------
        if st.button("Gerar PDF com resultados e gráficos"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, "Relatório de Cálculos Estatísticos", 0, 1, 'C')
            pdf.set_font("Arial", '', 12)
            pdf.cell(0, 10, f"Usuário: {st.session_state.usuario}", 0, 1)
            pdf.cell(0, 10, f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", 0, 1)
            pdf.ln(10)
            pdf.cell(0, 10, f"Média: {deixar_virgula(media)}", 0, 1)
            if st.session_state.esco == "População":
                pdf.cell(0, 10, f"Variância: {deixar_virgula(var_pop)}", 0, 1)
                pdf.cell(0, 10, f"Desvio padrão: {deixar_virgula(desvio_pop)}", 0, 1)
            else:
                pdf.cell(0, 10, f"Variância: {deixar_virgula(var_amostral)}", 0, 1)
                pdf.cell(0, 10, f"Desvio padrão: {deixar_virgula(desvio_amostral)}", 0, 1)
                pdf.cell(0, 10, f"Incerteza padrão (u): {deixar_virgula(u_padrao)}", 0, 1)
                pdf.cell(0, 10, f"Incerteza expandida (U, k=2): {deixar_virgula(u_expandida)}", 0, 1)
                pdf.cell(0, 10, f"Intervalo 95%: [{deixar_virgula(intervalo[0])}, {deixar_virgula(intervalo[1])}]", 0, 1)

            # Salva os gráficos em imagens e insere no PDF
            imagens = []
            for fig in [fig1, fig2, fig3, fig4]:
                buf = io.BytesIO()
                fig.savefig(buf, format='PNG', bbox_inches='tight', transparent=True)
                buf.seek(0)
                imagens.append(buf)

            # Insere as imagens (4 gráficos em duas páginas)
            for i, img in enumerate(imagens):
                if i % 2 == 0 and i != 0:
                    pdf.add_page()
                x_pos = 10 if i % 2 == 0 else 110
                y_pos = 60 if i % 2 == 0 else 60
                pdf.image(img, x=x_pos, y=y_pos, w=90)
                img.close()

            # Download do PDF
            pdf_output = pdf.output(dest='S').encode('latin1')
            st.download_button(
                label="Baixar PDF",
                data=pdf_output,
                file_name=f"Relatorio_Estatistico_{usuario}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf"
            )
