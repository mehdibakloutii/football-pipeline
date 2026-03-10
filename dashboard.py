import streamlit as st
import plotly.express as px
import psycopg2
import pandas as pd

# Connexion PostgreSQL
@st.cache_data
def get_data(query):
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="football_db",
        user="postgres",
        password="Football2024!"
    )
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Config page
st.set_page_config(
    page_title="Football Dashboard",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ Premier League Dashboard")
st.markdown("Pipeline de données : API Football → Python → PostgreSQL → dbt → Streamlit")

# Classement
st.header("🏆 Classement Premier League")
df_standings = get_data("""
    SELECT team, games_played, wins, draws, losses, 
           goals_scored, goals_conceded, points,
           goals_scored - goals_conceded as goal_diff
    FROM mart_team_stats
    ORDER BY points DESC, goal_diff DESC
""")
st.dataframe(df_standings, use_container_width=True)

# Graphiques
col1, col2 = st.columns(2)

with col1:
    st.header("📊 Top 10 — Points")
    fig1 = px.bar(
        df_standings.head(10),
        x="team", y="points",
        color="points",
        color_continuous_scale="Greens",
        title="Top 10 équipes par points"
    )
    fig1.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.header("⚽ Top 10 — Buts marqués")
    fig2 = px.bar(
        df_standings.sort_values("goals_scored", ascending=False).head(10),
        x="team", y="goals_scored",
        color="goals_scored",
        color_continuous_scale="Blues",
        title="Top 10 équipes par buts marqués"
    )
    fig2.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig2, use_container_width=True)

# Victoires vs Défaites
st.header("📈 Victoires, Nuls et Défaites")
fig3 = px.bar(
    df_standings.head(10),
    x="team",
    y=["wins", "draws", "losses"],
    title="Résultats des 10 premières équipes",
    barmode="group",
    color_discrete_map={
        "wins": "green",
        "draws": "orange", 
        "losses": "red"
    }
)
fig3.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig3, use_container_width=True)

# Métriques clés
st.header("📊 Métriques clés")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Équipes", len(df_standings))
with col2:
    st.metric("Matchs joués", int(df_standings['games_played'].sum() / 2))
with col3:
    st.metric("Buts totaux", int(df_standings['goals_scored'].sum() / 2))
with col4:
    leader = df_standings.iloc[0]['team']
    st.metric("Leader", leader)