import streamlit as st
import pandas as pd

st.title("TEAMS") 

@st.cache_data
def load_data():
    df=pd.read_csv("datasets/teams.csv")
    return df

df=load_data()
st.dataframe(df)

#Team Analysis?
# Team ranking????

#------------------------------------------team overview-------------------------------------
st.header("team overview :material/scoreboard:")

#most goals scored
max_gf=df["goals"].max() 
max_gf_teams=df.loc[ df["goals"] == max_gf, "team" ].tolist() 
max_gf_team = ", ".join(max_gf_teams)

#most goals conceded
max_ga=df["goals_against"].max() 
max_ga_teams=df.loc[ df["goals_against"] == max_ga, "team" ].tolist() 
max_ga_team = ", ".join(max_ga_teams)

most_gf, most_ga=st.columns(2)
with most_gf:
    st.metric("Team with the most goals scored", 
    max_gf_team,
    delta= f"{max_gf:.0f} goals",
    border=True, 
    icon=":material/sentiment_excited:", delta_color="blue", delta_arrow="off")
with most_ga:
    st.metric("Team with the most goals conceded", 
    max_ga_team,
    delta= f"{max_ga:.0f} goals",
    border=True, 
    icon=":material/sentiment_neutral:", delta_color="blue", delta_arrow="off")

##least goals scored
min_gf=df["goals"].min()
min_gf_teams=df.loc[ df["goals"] == min_gf, "team" ].tolist() 
min_gf_team = ", ".join(min_gf_teams)

#least goals conceded
min_ga=df["goals_against"].min() 
min_ga_teams=df.loc[ df["goals_against"] == min_ga, "team" ].tolist() 
min_ga_team = ", ".join(min_ga_teams)

least_gf, least_ga=st.columns(2)
with least_gf:
    st.metric("Team with the least goals scored", 
    min_gf_team,
    delta= f"{min_gf:.0f} goals",
    border=True, 
    icon=":material/sentiment_stressed:", delta_color="blue", delta_arrow="off")
with least_ga:
    st.metric("Team with the least goals conceded", 
    min_ga_team,
    delta= f"{min_ga:.0f} goals",
    border=True, 
    icon=":material/sentiment_content:", delta_color="blue", delta_arrow="off")

#---------------------------------------
#----------------------------------------------------offensive performance--------------------------------------
st.divider()
st.header("Offensive performance :material/scoreboard:")


#-----------------------------------------------defensive-------------------------------------------------
st.divider()
st.header("Defensive performance :material/scoreboard:")

# ------------------------------------------possession--------------------------------------------------------
st.divider()
st.header("possesion :material/scoreboard:")



#-------------------------------------offensive vs defensive performance---------
st.divider()
st.header("Offensive vs Defensive Performance")
