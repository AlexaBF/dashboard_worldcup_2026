import streamlit as st
import pandas as pd
import numpy as np

@st.cache_data
def load_data():
    df=pd.read_csv("datasets/matches.csv")
    df["attendance"] = df["attendance"].str.replace(",", "").astype(int)
    return df

df_matches=load_data()

st.title("Overview")

st.caption("Datasets retrieved from Kaggle Datasets")
col1, col2, col3 = st.columns(3)
with col1:
    st.link_button("Dataset FIFA Matches", "https://www.kaggle.com/datasets/swaptr/fifa-wc-2026-matches") 
with col2:
    st.link_button("Dataset FIFA Teams", "https://www.kaggle.com/datasets/swaptr/fifa-wc-2026-teams")
with col3:
    st.link_button("Dataset FIFA Players", "https://www.kaggle.com/datasets/swaptr/fifa-wc-2026-players")

st.divider()

#---------------------------------------------------------------------------------------------
places=df_matches[ ["round", "home_team", "away_team", "score", "home_score", "away_score"] ].copy()
# Final + 3rd-place matches
finals = places[ places["round"].isin(["Final", "Third-place match"]) ].copy()
# Find winner
finals["winner"] = np.where(
    finals["home_score"] > finals["away_score"],
    finals["home_team"],
    finals["away_team"]
)
finals["loser"] = np.where(
    finals["home_score"] < finals["away_score"],
    finals["home_team"],
    finals["away_team"]
)

result = finals[["round", "score","winner","loser"]]
first_place=result.loc[ result["round"]=="Final","winner"].iloc[0]
second_place=result.loc[ result["round"]=="Final","loser"].iloc[0]
third_place=result.loc[ result["round"]=="Third-place match","winner"].iloc[0]
final_score=result.loc[ result["round"]=="Final","score"].iloc[0]
third_score=result.loc[ result["round"]=="Third-place match","score"].iloc[0]

st.header(":material/social_leaderboard: World Cup Podium Finish")
n1,n2,n3 = st.columns(3)
n2.metric("First Place", first_place, delta=final_score, delta_arrow="off" , border=True,icon=":material/trophy:")
n1.metric("Second Place", second_place,delta=final_score,delta_color="red", delta_arrow="off", border=True,icon=":material/trophy:")
n3.metric("Third Place", third_place, delta=third_score, delta_arrow="off", border=True,icon=":material/trophy:")
st.divider()
#------------------------------------------------------------------------------------------------------

#Number of players
#Current top scorer
#--------------------------------------------------------------------------------------
#Number of teams
#Top team



#------------------------------------------------------------------------------------------------------------------------
#total matches
total_matches=len(df_matches)
#total goals
total_goals=int( (df_matches["home_score"] + df_matches["away_score"]).sum() )
#avg goals
avg_goals=int( (df_matches["home_score"] + df_matches["away_score"]).mean() )

#avg attendance
avg_attendance=df_matches["attendance"].mean()


#total matches, total goals, avg attendance)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Matches", total_matches, border=True,icon=":material/calendar_month:")
col2.metric("Total Goals", total_goals, border=True, icon=":material/sports_soccer:")
col3.metric("Average Attendance", f"{avg_attendance:,.0f}",border=True,icon=":material/event_seat:" )
col4.metric("average goal", avg_goals,  border=True, icon=":material/sports_and_outdoors:")


formations = pd.concat([df_matches["home_formation"], df_matches["away_formation"]])
formation_counts = formations.value_counts().head(10)

st.header("Most Common Formations")
with st.container(border=True):
    st.bar_chart(formation_counts, x_label="Formation", y_label="Count")

#------------------------------------------------------------------------------
#Yellow cards

#Red cards