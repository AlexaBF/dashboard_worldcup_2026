import streamlit as st
import pandas as pd

st.title(":material/scoreboard: MATCHES") 

@st.cache_data
def load_data():
    df=pd.read_csv("datasets/matches.csv")
    df["attendance"] = df["attendance"].str.replace(",", "").astype(int)
    return df

df=load_data()

#total matches
total_matches=len(df)
#total goals
total_goals=int( (df["home_score"] + df["away_score"]).sum() )
#avg goals
avg_goals=int( (df["home_score"] + df["away_score"]).mean() )

col1,col2,col3=st.columns(3)
with col1:
    st.metric(
        "Total Matches",
        total_matches,
        border=True, 
        icon=":material/calendar_month:")
with col2:
    st.metric(
        "Total Goals",
        total_goals,
        border=True, 
        icon=":material/sports_soccer:")

with col3:
    st.metric(
        "Average goals per match",
        avg_goals,
        border=True, 
        icon=":material/sports_and_outdoors:")

st.divider()  

tab1,tab2=st.tabs(["All Matches","Team Matches"])


#--------------------------------------------------filtered rounds-----------------------------------------
with tab1:
    overview_df=df[["round","home_team", "away_team", "score", "attendance", "venue","referee", "home_formation","away_formation","home_manager","away_manager","home_captain","away_captain", "home_score", "away_score" ]].copy()

    rounds = df["round"].unique().tolist()
    rounds.insert(0, "All")

    selected_round = st.selectbox("Select round", rounds)

    if selected_round == "All":
        filtered_df = overview_df
    else:
        filtered_df = overview_df[overview_df["round"] == selected_round]
    #------------------------------------------------------------------------------------------------------------------------
    #total matches
    total_matches=len(filtered_df)
    #total goals
    total_goals=int( (filtered_df["home_score"] + filtered_df["away_score"]).sum() )
    #avg goals
    avg_goals=int( (filtered_df["home_score"] + filtered_df["away_score"]).mean() )

    #avg attendance
    avg_attendance=filtered_df["attendance"].mean()
    #


    #total matches, total goals, avg attendance)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Matches", total_matches, border=True,icon=":material/calendar_month:")
    col2.metric("Total Goals", total_goals, border=True, icon=":material/sports_soccer:")
    col3.metric("Average Attendance", f"{avg_attendance:,.0f}",border=True,icon=":material/event_seat:" )
    col4.metric("average goal", avg_goals,  border=True, icon=":material/sports_and_outdoors:")

    #tabla de datos
    st.dataframe(filtered_df)

    formations = pd.concat([filtered_df["home_formation"], filtered_df["away_formation"]])
    formation_counts = formations.value_counts().head(10)

    st.header("Most Common Formations")
    with st.container(border=True):
        st.bar_chart(formation_counts, x_label="Formation", y_label="Count")


with tab2:

    match_metrics=df[["home_team","away_team","round","date","start_time","attendance","venue","referee","home_manager","away_manager","home_captain","away_captain"]].copy()


    team = match_metrics["home_team"].unique().tolist()
    selected_team= st.selectbox("Select team", team)

    mm_home = match_metrics[match_metrics["home_team"] == selected_team]
    mm_away = match_metrics[match_metrics["away_team"] == selected_team]
    frames = [mm_home, mm_away]
    match_metrics = pd.concat(frames)

    dates = match_metrics["date"].unique().tolist()
    dates.sort()
    selected_date = st.selectbox("Select date", dates)

    match_metrics = match_metrics[match_metrics["date"] == selected_date]
    #st.dataframe(match_metrics)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Home Team", match_metrics["home_team"].iloc[0],  border=True, icon=":material/sports_and_outdoors:")
        st.metric("Home Manager", match_metrics["home_manager"].iloc[0],  border=True, icon=":material/sports_and_outdoors:")
        st.metric("home Captain", match_metrics["home_captain"].iloc[0],  border=True, icon=":material/sports_and_outdoors:")

        st.metric("Round", match_metrics["round"].iloc[0], border=True,icon=":material/calendar_month:")
        st.metric("Venue", match_metrics["venue"].iloc[0], border=True,icon=":material/calendar_month:")
        st.metric("Attendance", match_metrics["attendance"].iloc[0],  border=True, icon=":material/sports_and_outdoors:")

    with col2:
        st.metric("Away Team", match_metrics["away_team"].iloc[0],  border=True, icon=":material/sports_and_outdoors:")
        st.metric("Away Manager", match_metrics["away_manager"].iloc[0],  border=True, icon=":material/sports_and_outdoors:")
        st.metric("Away Captain", match_metrics["away_captain"].iloc[0],  border=True, icon=":material/sports_and_outdoors:")
        st.metric("Date", match_metrics["date"].iloc[0], border=True, icon=":material/sports_soccer:")
        st.metric("Referee", match_metrics["referee"].iloc[0], border=True,icon=":material/calendar_month:")
        st.metric("Start Time", match_metrics["start_time"].iloc[0],border=True,icon=":material/event_seat:" )

    st.subheader("Results")

    st.subheader("Match Statistics")
    st.text("home vs away")
    st.text(" % possession")
    st.text("shots")
    st.text("  corner kicks")
    st.text("  offsides")
    st.text("  yellow cards")
    st.text("  red cards")
    st.text(" formation of each team")
