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
st.subheader(":material/social_leaderboard: Top Scorers")
top_scorers=df.sort_values(by=["goals","assists"], ascending=False).head()

s_place1,s_place2,s_place3 = st.columns(3)
with s_place1:
    st.metric(label="2nd Place",
    value=top_scorers["player"].iloc[1],
    delta=f"GOALS: {top_scorers["goals"].iloc[1]:.0f}",
    border=True,
    icon=":material/trophy:",
    delta_arrow="off")
with s_place2:
    st.metric(label="1st Place",
    value=top_scorers["player"].iloc[0],
    delta=f"GOALS: {top_scorers["goals"].iloc[0]:.0f}",
    border=True,
    icon=":material/trophy:",
    delta_arrow="off")
    
with s_place3:
    st.metric(label="3rd Place",
    value=top_scorers["player"].iloc[2],
    delta=f"GOALS: {top_scorers["goals"].iloc[2]:.0f}",
    border=True,
    icon=":material/trophy:",
    delta_arrow="off")
# ---------------------------------------
# ------------------------------Top assists------------------------------------------

st.subheader(":material/social_leaderboard: Top Assists")
top_assists=df.sort_values(by=["assists","goals"], ascending=False).head()

a_place1,a_place2,a_place3 = st.columns(3)
with a_place1:
    st.metric(label="2nd Place",
    value=top_assists["player"].iloc[1],
    delta=f"ASSISTS: {top_assists["assists"].iloc[1]:.0f}",
    border=True,
    icon=":material/trophy:",
    delta_arrow="off")
with a_place2:
    st.metric(label="1st Place",
    value=top_assists["player"].iloc[0],
    delta=f"ASSISTS: {top_assists["assists"].iloc[0]:.0f}",
    border=True,
    icon=":material/trophy:",
    delta_arrow="off")
    
with a_place3:
    st.metric(label="3rd Place",
    value=top_assists["player"].iloc[2],
    delta=f"ASSISTS: {top_assists["assists"].iloc[2]:.0f}",
    border=True,
    icon=":material/trophy:",
    delta_arrow="off")

