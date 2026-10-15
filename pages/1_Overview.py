import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


@st.cache_data
def load_data():
    df=pd.read_csv("datasets/matches.csv")
    df["attendance"] = df["attendance"].str.replace(",", "").astype(int)
    df_p=pd.read_csv("datasets/players.csv")
    df_t=pd.read_csv("datasets/teams.csv")
    df_v=pd.read_csv("datasets/venues_locations.csv")
    return df,df_p,df_t,df_v

df_matches,df_players,df_team,df_venues=load_data()
#------------------------------------------------------------------------------------------------------------
st.title(":material/dashboard: Overview")

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
#df for podium 
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

#get the teams in podium
result = finals[["round", "score","winner","loser"]]
first_place=result.loc[ result["round"]=="Final","winner"].iloc[0]
second_place=result.loc[ result["round"]=="Final","loser"].iloc[0]
third_place=result.loc[ result["round"]=="Third-place match","winner"].iloc[0]
final_score=result.loc[ result["round"]=="Final","score"].iloc[0]
third_score=result.loc[ result["round"]=="Third-place match","score"].iloc[0]

st.header(":material/social_leaderboard: World Cup Podium Finish")
#show podium 
n1,n2,n3 = st.columns(3)
n2.metric("First Place", first_place, delta=final_score, delta_arrow="off" , border=True,icon=":material/trophy:")
n1.metric("Second Place", second_place,delta=final_score,delta_color="red", delta_arrow="off", border=True,icon=":material/trophy:")
n3.metric("Third Place", third_place, delta=third_score, delta_arrow="off", border=True,icon=":material/trophy:")

#the most countries metric
st.metric(label="Host Countries", value="CANADA , MÉXICO, USA", border=True, icon=":material/globe_location_pin:")

st.divider()
#------------------------------------------------------------------------------------------------------------------------
#total matches
total_matches=len(df_matches)
#total goals
total_goals=int( (df_matches["home_score"] + df_matches["away_score"]).sum() )
#avg attendance
avg_attendance=df_matches["attendance"].mean()
#top scorer
top_scorer=df_players.sort_values(by=["goals","assists"], ascending=False).head(1)
#total venues
total_venues=len(df_venues)

#overview metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric( "Total Teams", len(df_team), border=True, icon=":material/flag:")

    st.metric( "Top team", first_place,  border=True, icon=":material/trophy:")
    
with col2:
    st.metric("Total Matches", total_matches, border=True, icon=":material/calendar_month:")

    st.metric("Total Goals", total_goals, border=True, icon=":material/sports_soccer:")

with col3:
    st.metric("Total players", len(df_players), border=True, icon=":material/group:" )

    st.metric("Tops scorer", value=top_scorer["player"].iloc[0], border=True, icon=":material/trophy:")

with col4:
    st.metric("Total Venues", total_venues, border=True, icon=":material/stadium:")

    st.metric("Average Attendance", f"{avg_attendance:,.0f}", border=True, icon=":material/event_seat:" )

#df for formaitons
formations = pd.concat([df_matches["home_formation"], df_matches["away_formation"]])
formation_counts = formations.value_counts().head(5)
#common formations bar chart
with st.container(border=True):
    st.header(":material/tactic: Most Common Formations")
    st.bar_chart(
        formation_counts,
        x_label="Formation",
        y_label="Count",
        sort="-count")

#df teams goals
teams_goals=df_team[["team","goals","minutes"]].copy().reset_index()
#Teams: goals scored vs minutes scatter chart
with st.container(border=True):
    st.header(":material/sports_soccer: Teams: goals scored vs minutes")
    fig = px.scatter(
        teams_goals,
        x="goals",
        y="minutes",
        color="team",
        size="minutes",
        labels={
            "goals": "Goals",
            "minutes": "Minutes"
            }
        )
    st.plotly_chart(fig)

#df players age
players_age=df_players[["player","age","team","minutes"]].copy().reset_index()
#players age scatter chart
fig = px.scatter(
    players_age,
    x="age",
    y="minutes",
    color="player",
    hover_data=["team"],
    size="age",
    labels={
        "age":"Age",
        "player":"Player",
        "minutes":"Minutes played",
        "team":"Team"
    }
    )
#plot scatter chart
with st.container(border=True):
    st.header(":material/emoji_people: Players: age and minutes played")
    st.plotly_chart(fig)
