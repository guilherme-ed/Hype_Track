import streamlit as st
import pandas as pd
import plotly.express as px
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="Hype Track", page_icon="📊", layout='wide')

@st.cache_data
def carregar_dados():
    produtos = ['Óculos VR Neo', 'Smartphone Holográfico', 'Neural Link Lite', 'Console Quântico']
    sentimentos = ['Positivo', 'Neutro', 'Negativo']

    dados = []
    hoje = datetime.now()

    for _ in range(200):
        dados.append({
            "data": hoje - timedelta(days=random.randint(0, 30)),
            "produto": random.choice(produtos),
            "sentimentos": random.choice(sentimentos),
            "engajamento": random.randint(100, 5000),
            "nota": random.uniform(1, 5)        
        })

    return pd.DataFrame(dados)

df = carregar_dados()

# 🔧 garante padrão
df.columns = df.columns.str.strip().str.lower()

# SIDEBAR
st.sidebar.header("Painel de Controle")
st.sidebar.markdown("Filtro de dados em tempo real:")

produto_selecionado = st.sidebar.multiselect(
    "Escolha o Produto:",
    options=df["produto"].unique(),
    default=df["produto"].unique()
)

# FILTRO
df_filtrado = df[df["produto"].isin(produto_selecionado)]

# TÍTULO
st.title("📊 Rastreador de Hype")
st.subheader("Análise visual de sentimentos e engajamento tech")
st.markdown("---")

# MÉTRICAS
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total de Menções", len(df_filtrado), "+12%")

with col2:
    st.metric("Média de Engajamento", f"{int(df_filtrado['engajamento'].mean())} cliques")

with col3:
    st.metric("Nota Média", round(df_filtrado['nota'].mean(), 1), "🌟")

st.markdown("---")

# GRÁFICOS
col_esq, col_dir = st.columns(2)

with col_esq:
    st.markdown("### 🔥 Volume de Hype por Produto")
    fig_bar = px.bar(
        df_filtrado,
        x="produto",
        y="engajamento",
        color="sentimentos",
        title="Engajamento total por categoria",
        color_discrete_map={
            'Positivo': '#00CC96',
            'Neutro': '#636EFA',
            'Negativo': '#EF553B'
        }
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col_dir:
    st.markdown("### 🧠 Distribuição de Sentimentos")
    fig_pie = px.pie(
        df_filtrado,
        names="sentimentos",
        hole=0.4,
        title="O que o mundo está achando?"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# TABELA
with st.expander("📂 Ver dados brutos (Tabela do Pandas)"):
    st.dataframe(
        df_filtrado.sort_values(by="data", ascending=False),
        use_container_width=True
    )

st.sidebar.info("Projeto criado para o tutorial")
