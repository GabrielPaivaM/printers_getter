import streamlit as st
import pandas as pd
import plotly.express as px
import glob
import os

st.set_page_config(layout="wide")
st.title("📠 Dashboard de Impressoras - Páginas por Mês")

@st.cache_data
def load_all_data(folder="dados"):
    all_files = glob.glob(os.path.join(folder, "*.csv"))
    dfs = []
    for file in all_files:
        df = pd.read_csv(file, parse_dates=["collection_date"])
        dfs.append(df)
    if dfs:
        full_df = pd.concat(dfs, ignore_index=True)
        full_df['month'] = full_df['collection_date'].dt.to_period("M")
        return full_df
    else:
        return pd.DataFrame()

df = load_all_data()

if df.empty:
    st.warning("Nenhum dado encontrado na pasta 'dados/'.")
    st.stop()

# 🕓 Mostra dados mais recentes de cada impressora
df = df.sort_values("collection_date")
mes_mais_recente = df['month'].max()
df_recente = df[df['month'] == mes_mais_recente]

st.subheader(f"📋 Dados coletados no mês mais recente ({str(mes_mais_recente)})")
st.dataframe(
    df_recente[['collection_date', 'name', 'ip', 'serie', 'pages_this_month']].rename(columns={
        "collection_date": "Data da coleta",
        "name": "Impressora",
        "ip": "IP",
        "serie": "Número de série",
        "pages_this_month": "Páginas no mês"
    }),
    use_container_width=True,
    hide_index=True
)

# 📊 Gráficos por impressora
st.subheader("📊 Gráficos - Páginas impressas por mês")

# Limpa dados ausentes e ajusta o mês antes de qualquer filtro
df = df.dropna(subset=["pages_this_month"])
df['month'] = df['collection_date'].dt.to_period("M")

# Dropdown para seleção de impressora
impressoras = sorted(df['name'].dropna().unique())
opcao = st.selectbox("🖨️ Selecione uma impressora", options=["Todas"] + impressoras)

# Filtra conforme a opção
df_filtrado = df if opcao == "Todas" else df[df['name'] == opcao]

# Gráficos
if opcao == "Todas":
    for name in df_filtrado['name'].unique():
        sub = df_filtrado[df_filtrado['name'] == name]

        # Gráfico de barras
        fig_barra = px.bar(
            sub,
            x=sub['month'].astype(str),
            y='pages_this_month',
            title=f"{name} - Páginas por mês",
            labels={'pages_this_month': 'Páginas no mês', 'month': 'Mês'},
            color='pages_this_month',
            color_continuous_scale='Blues'
        )

        # Gráfico de pizza (distribuição mensal dessa impressora)
        df_pizza = sub.groupby('month')['pages_this_month'].sum().reset_index()
        fig_pizza = px.pie(
            df_pizza,
            names=df_pizza['month'].astype(str),
            values='pages_this_month',
            title=f"{name} - Distribuição mensal"
        )

        col1, col2 = st.columns([2, 1])  # col1 = 2/3 da largura, col2 = 1/3

        with col1:
            st.plotly_chart(fig_barra, use_container_width=True)

        with col2:
            st.plotly_chart(fig_pizza, use_container_width=True)

else:
    # Gráfico de barras
    fig_barra = px.bar(
        df_filtrado,
        x=df_filtrado['month'].astype(str),
        y='pages_this_month',
        title=f"{opcao} - Páginas por mês",
        labels={'pages_this_month': 'Páginas no mês', 'month': 'Mês'},
        color='pages_this_month',
        color_continuous_scale='Blues'
    )

    # Gráfico de pizza
    df_pizza = df_filtrado.groupby('month')['pages_this_month'].sum().reset_index()
    fig_pizza = px.pie(
        df_pizza,
        names=df_pizza['month'].astype(str),
        values='pages_this_month',
        title=f"{opcao} - Distribuição mensal"
    )

    col1, col2 = st.columns([2, 1])  # col1 = 2/3 da largura, col2 = 1/3

    with col1:
        st.plotly_chart(fig_barra, use_container_width=True)

    with col2:
        st.plotly_chart(fig_pizza, use_container_width=True)


# 📈 Totais acumulados (último total_pages de cada impressora)
st.subheader("📈 Total de páginas registradas por impressora (última coleta)")

# Pega o total_pages mais recente por impressora
df_ultimos = df.sort_values("collection_date").groupby("name").tail(1)

totais = df_ultimos[["name", "total_pages"]].rename(columns={
    "name": "Impressora",
    "total_pages": "Total de páginas impressas"
})

st.dataframe(
    totais,
    use_container_width=True,
    hide_index=True
)