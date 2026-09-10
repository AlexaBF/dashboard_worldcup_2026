import streamlit as st
import pandas as pd

st.title("PLAYERS")

@st.cache_data
def load_data():
    df=pd.read_csv("datasets/players.csv")
    df['club'] = df['club'].fillna('No Club')
    return df

df=load_data()
st.dataframe(df)

st.header("Player Performance and Statistics")
#------------------------------------------Top scorers------------------------------------------
st.subheader("Top Scorers :material/social_leaderboard: ")
top_scorers=df.sort_values(by=["goals","assists"], ascending=False).head()

place1,place2,place3 = st.columns(3)
with place1:
    st.metric(label="2nd Place",
    value=top_scorers["player"].iloc[1],
    delta=f"GOALS: {top_scorers["goals"].iloc[1]:.0f}",
    border=True,
    icon=":material/trophy:",
    delta_arrow="off")
with place2:
    st.metric(label="1st Place",
    value=top_scorers["player"].iloc[0],
    delta=f"GOALS: {top_scorers["goals"].iloc[0]:.0f}",
    border=True,
    icon=":material/trophy:",
    delta_arrow="off")
    
with place3:
    st.metric(label="3rd Place",
    value=top_scorers["player"].iloc[2],
    delta=f"GOALS: {top_scorers["goals"].iloc[2]:.0f}",
    border=True,
    icon=":material/trophy:",
    delta_arrow="off")
# ---------------------------------------
# ------------------------------Top assists------------------------------------------

st.subheader("Top Assists :material/social_leaderboard: ")
top_assists=df.sort_values(by=["assists","goals"], ascending=False).head()

place1,place2,place3 = st.columns(3)
with place1:
    st.metric(label="2nd Place",
    value=top_assists["player"].iloc[1],
    delta=f"ASSISTS: {top_assists["assists"].iloc[1]:.0f}",
    border=True,
    icon=":material/trophy:",
    delta_arrow="off")
with place2:
    st.metric(label="1st Place",
    value=top_assists["player"].iloc[0],
    delta=f"ASSISTS: {top_assists["assists"].iloc[0]:.0f}",
    border=True,
    icon=":material/trophy:",
    delta_arrow="off")
    
with place3:
    st.metric(label="3rd Place",
    value=top_assists["player"].iloc[2],
    delta=f"ASSISTS: {top_assists["assists"].iloc[2]:.0f}",
    border=True,
    icon=":material/trophy:",
    delta_arrow="off")

