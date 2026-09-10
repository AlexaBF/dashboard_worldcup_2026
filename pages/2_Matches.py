import streamlit as st
import pandas as pd

st.title("MATCHES") 

@st.cache_data
def load_data():
    df=pd.read_csv("datasets/matches.csv")
    df["attendance"] = df["attendance"].str.replace(",", "").astype(int)
    return df

df=load_data()
st.dataframe(df)

#total_mtches--
#Average goals per match
#total goals


"""
- Matches
filter: team, round, venue?
round, date, start_time, attendance, venue, referee
home_manager, away_manager
home_captain, away_captain

Results score

-Home vs Away
Match statistics:
. % possession
. shots
. shots on target (sot)
.  corner kicks
. passes
. offsides
. yellow cards
. red cards?
formation of each team

"""