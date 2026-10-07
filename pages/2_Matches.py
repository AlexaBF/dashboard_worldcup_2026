import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px


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

    #match_metrics=df[[  ate","start_time","attendance","venue","referee","home_manager","away_manager","home_captain","away_captain"]].copy()
    match_metrics=df.copy()

    team = match_metrics["home_team"].unique().tolist()
    team.sort()
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

    st.header(f"{match_metrics["home_team"].iloc[0]} | {match_metrics["score"].iloc[0]} | {match_metrics["away_team"].iloc[0]}",text_alignment="center")
    

    c1,c2,c3=st.columns(3)
    with c1:
        st.caption(f":material/schedule: Date and Time:{match_metrics["date"].iloc[0]}, {match_metrics["start_time"].iloc[0]}",text_alignment="center")
    with c2:
        st.caption(f":material/globe_location_pin: Location: {match_metrics["venue"].iloc[0]}",text_alignment="center")
    with c3:
        st.caption(f":material/crowdsource: Attendance: {match_metrics["attendance"].iloc[0]}",text_alignment="center")


    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(f"{match_metrics["home_team"].iloc[0]} Manager", match_metrics["home_manager"].iloc[0],  border=True, icon=":material/badge:")
        st.metric(f"{match_metrics["home_team"].iloc[0]} Captain", match_metrics["home_captain"].iloc[0],  border=True, icon=":material/assignment_ind:")

    with col2:
        st.metric(f"{match_metrics["away_team"].iloc[0]} Manager", match_metrics["away_manager"].iloc[0],  border=True, icon=":material/badge:")
        st.metric(f"{match_metrics["away_team"].iloc[0]} Captain", match_metrics["away_captain"].iloc[0],  border=True, icon=":material/assignment_ind:")

    with col3:
        st.metric("Referee", match_metrics["referee"].iloc[0], border=True,icon=":material/sports:")
        st.metric("Round", match_metrics["round"].iloc[0], border=True,icon=":material/calendar_month:")


    st.divider()
    st.header(":material/query_stats: Match Statistics")

    
    home_team = match_metrics["home_team"].iloc[0]
    away_team = match_metrics["away_team"].iloc[0]

    home_possession = match_metrics["home_possession"].iloc[0]
    away_possession = match_metrics["away_possession"].iloc[0]

    possession = pd.DataFrame({
        "Team": [home_team, away_team],
        "Possession": [home_possession, away_possession],
        "Order": [1, 2]
    })

    chart = alt.Chart(possession).mark_bar(
        height=35
    ).encode(
        x=alt.X(
            "Possession:Q",
            stack="normalize",
            scale=alt.Scale(domain=[0, 1]),
            axis=None
        ),
        y=alt.value(0),
        color=alt.Color(
            "Team:N",
            scale=alt.Scale(
                domain=[home_team, away_team],
                range=['#eb9736','#36A2EB']
            ),
            legend=None
        )
    ).properties(
        width=700,
        height=50
    )



    # Get the match
    match = match_metrics.iloc[0]
    # Metrics
    metrics = ["Shots","Shots on target","Corners","Offsides","Yellow cards","Red cards"]

    data_home = pd.DataFrame({
        "Metric": metrics,
        "Value": [match["home_total_shots"],match["home_sot"],match["home_corners"],match["home_offsides"],match["home_cards_yellow"],match["home_cards_red"] ]
    })


    data_away = pd.DataFrame({
        "Metric": metrics,
        "Value": [match["away_total_shots"],match["away_sot"],match["away_corners"],match["away_offsides"],match["away_cards_yellow"],match["away_cards_red"]]
    })


    def create_stats_chart(data, color):
        fig = px.bar(
            data,
            x="Value",
            y="Metric",
            orientation="h"
        )

        fig.update_traces(marker_color=color)

        fig.update_layout(
            height=300,
            showlegend=False,
            xaxis_title=None,
            yaxis_title=None
        )

        return fig


    chart_home = create_stats_chart(data_home, "#eb9736")
    chart_away = create_stats_chart(data_away, "#36A2EB")


    st.subheader(":material/percent: Possession",text_alignment="center")
    st.altair_chart(chart, use_container_width=True)
    
    teamA, teamB=st.columns(2)
    with teamA:
        st.subheader(match_metrics["home_team"].iloc[0])
        st.plotly_chart(chart_home, use_container_width=True,config={"displayModeBar": False})
        #st.bar_chart(match_metrics,x="home_team",x_label=" ",y=["home_total_shots","home_sot","home_corners","home_offsides","home_cards_yellow","home_cards_red" ],horizontal=True,stack=False)
    
    with teamB:
        st.subheader(match_metrics["away_team"].iloc[0])
        #st.bar_chart(match_metrics,x="away_team",x_label=" ",y=["away_total_shots","away_sot","away_corners","away_offsides","away_cards_yellow","away_cards_red" ],horizontal=True,stack=False)
        st.plotly_chart(chart_away, use_container_width=True,config={"displayModeBar": False})
    
    
        
    f1,f2=st.columns(2)
    f1.metric(f"{match_metrics["home_team"].iloc[0]} formation", match_metrics["home_formation"].iloc[0],  border=True, icon=":material/tactic:")
    f2.metric(f"{match_metrics["away_team"].iloc[0]} formation", match_metrics["away_formation"].iloc[0],  border=True, icon=":material/tactic:")

    


   