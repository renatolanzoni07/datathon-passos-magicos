import streamlit as st
import pandas as pd
import joblib

arquivo = "BASE DE DADOS PEDE 2024 - DATATHON.xlsx"

df2022 = pd.read_excel(
    arquivo,
    sheet_name="PEDE2022"
)

df2023 = pd.read_excel(
    arquivo,
    sheet_name="PEDE2023"
)

df2024 = pd.read_excel(
    arquivo,
    sheet_name="PEDE2024"
)

# ======================
# CONFIGURAÇÃO DA PÁGINA
# ======================

st.set_page_config(
    page_title="Passos Mágicos",
    page_icon="🎓",
    layout="wide"
)


# ======================
# CARREGAR MODELO
# ======================

modelo = joblib.load("modelo_risco.pkl")

menu = st.sidebar.radio(
    "Navegação",
    [
        "🏠 Home",
        "📊 Indicadores",
        "📈 Efetividade",
        "🎯 Preditor"
    ]
)


# ======================
# HOME
# ======================

if menu == "🏠 Home":

    st.title("🎓 Arquitetura do Impacto Educacional")

    st.subheader(
        "Passos Mágicos | Datathon FIAP 2026"
    )

    st.markdown("""
    Aplicação para identificação precoce de risco de defasagem educacional.
    """)

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Alunos Analisados", "1156")

    with col2:
        st.metric("Em Defasagem", "46%")

    with col3:
        st.metric("Mantiveram ou Evoluíram Pedra", "79,6%")

    with col4:
        st.metric("Recall do Modelo", "81%")

    st.divider()

    st.markdown("""
    ### Principais Descobertas

    - 46% dos estudantes apresentam algum grau de defasagem.
    - Aprendizagem (IDA), Engajamento (IEG) e Ponto de Virada (IPV) foram os indicadores mais associados ao INDE.
    - 79,6% dos estudantes mantiveram ou evoluíram sua classificação de Pedra.
    - O modelo identifica 81% dos estudantes que entrarão em situação de risco.
    """)

    st.divider()

    st.subheader("Panorama da Defasagem Educacional (2024)")

    dados_defasagem = pd.DataFrame({
        "Situação": [
            "Adequados",
            "Defasados"
        ],
        "Quantidade": [
            624,
            532
        ]
    })

    st.bar_chart(
        dados_defasagem.set_index("Situação")
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Adequados",
            "624 alunos (54%)"
        )

    with col2:
        st.metric(
            "Defasados",
            "532 alunos (46%)"
        )

# ======================
# PREDITOR
# ======================

if menu == "🎯 Preditor":

    st.header("🎯 Predição de Risco Educacional")

    st.info(
        """
        Este modelo estima a probabilidade de um estudante entrar em situação de risco educacional futuro.

        A previsão é calculada com base nos indicadores de Aprendizagem (IDA), Engajamento (IEG), Adequação ao Nível (IAN), Ponto de Virada (IPV) e características do estudante.

        O objetivo é apoiar ações preventivas e a priorização de acompanhamento pedagógico.
        """
    )

    col1, col2 = st.columns(2)

    with col1:
        iaa = st.slider("IAA", 0.0, 10.0, 8.0)
        ieg = st.slider("IEG", 0.0, 10.0, 8.0)
        ips = st.slider("IPS", 0.0, 10.0, 7.0)
        ida = st.slider("IDA", 0.0, 10.0, 6.0)

    with col2:
        ipv = st.slider("IPV", 0.0, 10.0, 7.0)
        ian = st.selectbox("IAN", [2.5, 5.0, 10.0])
        idade = st.number_input("Idade", 10, 30, 17)

        ano_ingresso = st.number_input(
            "Ano de Ingresso",
            2018,
            2025,
            2022
        )

    if st.button("Calcular Risco"):

        entrada = pd.DataFrame({
            "IAA": [iaa],
            "IEG": [ieg],
            "IPS": [ips],
            "IDA": [ida],
            "IPV": [ipv],
            "IAN": [ian],
            "Ano ingresso": [ano_ingresso],
            "Idade 22": [idade]
        })

        probabilidade = modelo.predict_proba(entrada)[0][1]

        st.subheader("Resultado")

        st.metric(
            "Probabilidade de Risco",
            f"{probabilidade*100:.1f}%"
        )

        if probabilidade < 0.30:
            st.success("🟢 Baixo Risco")

        elif probabilidade < 0.70:
            st.warning("🟡 Médio Risco")

        else:
            st.error("🔴 Alto Risco")

    st.divider()

    st.header("Principais Fatores do Modelo")

    st.markdown("""
    1. IPV (Ponto de Virada)

    2. IDA (Aprendizagem)

    3. IEG (Engajamento)

    Esses foram os fatores mais importantes para prever risco futuro de defasagem educacional.
    """)

# ======================
# INDICADORES
# ======================

if menu == "📊 Indicadores":

    st.title("📊 Indicadores Educacionais")

    indicador = st.selectbox(
        "Escolha um indicador",
        [
            "IAN",
            "IAA",
            "IEG",
            "IPS",
            "IDA",
            "IPP",
            "IPV"
        ]
    )

    ano = st.selectbox(
        "Selecione o ano",
        [
            "2022",
            "2023",
            "2024"
        ]
    )

    if ano == "2022":
        df = df2022
    elif ano == "2023":
        df = df2023
    else:
        df = df2024

    st.subheader(f"{indicador} - Ano {ano}")

    if indicador in df.columns:

        stats = df[indicador].describe()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Total de Alunos",
                int(stats["count"])
            )

        with col2:
            st.metric(
                "Média",
                round(stats["mean"], 2)
            )

        with col3:
            st.metric(
                "Mediana",
                round(stats["50%"], 2)
            )

        with col4:
            st.metric(
                "Máximo",
                round(stats["max"], 2)
            )

        st.bar_chart(
            df[indicador].value_counts().sort_index()
        )

    else:

        st.warning(
            f"O indicador {indicador} não existe para o ano selecionado."
        )

# ======================
# EFETIVIDADE
# ======================

if menu == "📈 Efetividade":

    st.title("📈 Efetividade do Programa")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Alunos que Melhoraram",
            "242"
        )

    with col2:
        st.metric(
            "Alunos que Pioraram",
            "226"
        )

    with col3:
        st.metric(
            "Mantiveram ou Evoluíram Pedra",
            "79,6%"
        )

    st.divider()

    st.subheader("Classificação Pedra")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🟢 Evoluíram",
            "35,2%"
        )

    with col2:
        st.metric(
            "🟡 Mantiveram",
            "44,4%"
        )

    with col3:
        st.metric(
            "🔴 Regrediram",
            "20,4%"
        )

    st.subheader("Retenção e Evolução")

    dados_pedra = pd.DataFrame({
        "Categoria": [
            "Evoluíram",
            "Mantiveram",
            "Regrediram"
        ],
        "Percentual": [
            35.21,
            44.38,
            20.41
        ]
    })

    st.bar_chart(
        dados_pedra.set_index("Categoria")
    )

    st.subheader("Principais Evidências")

    st.markdown("""
    ✅ Os estudantes com menor INDE inicial apresentaram a maior evolução ao longo do programa.

    ✅ 79,6% dos estudantes mantiveram ou evoluíram sua classificação de Pedra.

    ✅ A classificação por Pedra apresentou forte associação com a evolução do INDE.

    ✅ Os resultados sugerem impacto positivo especialmente entre estudantes com maior necessidade educacional.
    """)