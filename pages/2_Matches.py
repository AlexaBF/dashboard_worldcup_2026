import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import numpy as np


st.title(":material/scoreboard: MATCHES") 

@st.cache_data
def load_data():
    df=pd.read_csv("datasets/matches.csv")
    df["attendance"] = df["attendance"].str.replace(",", "").astype(int)
    return df

df=load_data()

#tabs for al matches and team matches
tab1,tab2=st.tabs([":material/select_all: All Matches",":material/select: Team Matches"])
#--------------------------------------------------All matches-----------------------------------------
with tab1:
    st.header(":material/select_all: All Matches")
    #get rounds list
    rounds = df["round"].unique().tolist()
    rounds.insert(0, "All")
    #filtered rounds
    selected_round = st.selectbox(":material/filter_alt: Select round", rounds)

    if selected_round == "All":
        filtered_df = df
    else:
        filtered_df = df[df["round"] == selected_round]

    #total matches
    total_matches=len(filtered_df)
    #total goals
    total_goals=int( (filtered_df["home_score"] + filtered_df["away_score"]).sum() )
    #avg goals
    avg_goals=int( (filtered_df["home_score"] + filtered_df["away_score"]).mean() )
    #avg attendance
    avg_attendance=filtered_df["attendance"].mean()
#------------------------------------------------------------------------------------
    #matches df
    all_matches=filtered_df[["round","home_team","away_team","score","attendance","venue"]]
    st.dataframe(all_matches)

    #tabs for matches
    ta1, ta2, ta3, ta4, ta5 = st.tabs([":material/dashboard: Overview",":material/sports_soccer: Goals",":material/query_stats: Match Stats",":material/sports: Discipline",":material/crowdsource: Attendance"])
#------------------------------------overview----------------------------------------------------
    with ta1:
        st.header(":material/dashboard: Overview")
        #overview metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Matches", total_matches, border=True,icon=":material/calendar_month:")
        col2.metric("Goals", total_goals, border=True, icon=":material/sports_soccer:")
        col3.metric("Average Attendance", f"{avg_attendance:,.0f}",border=True,icon=":material/event_seat:" )
        col4.metric("average goal", avg_goals,  border=True, icon=":material/sports_and_outdoors:") 

        #df for home win, draw , away win
        hda=filtered_df[["home_score","away_score"]].copy()
        hda["home_score"] = pd.to_numeric(hda["home_score"])
        hda["away_score"] = pd.to_numeric(hda["away_score"])

        hda["result"]=np.select(
            [
                hda["home_score"]>hda["away_score"],
                hda["home_score"]==hda["away_score"],
                hda["home_score"]<hda["away_score"]
            ],
            ["Home Win","Draw","Away Win"],
            default="Unknown"
        )
        
        #df with count for home win, draw , away win
        result_counts=(hda["result"].value_counts().reindex(["Home Win", "Draw", "Away Win"], fill_value=0))
        #plot matches "wins for home vs away team" bar chart 
        with st.container(border=True):
            st.subheader("Wins for home vs away team")
            st.bar_chart(
                result_counts,
                sort=False,
                color="#f5a06e"
            )

        #df for goals by round
        round_goals = filtered_df[["round", "home_score", "away_score"]]

        round_goals["total_goals"] = ( round_goals["home_score"] + round_goals["away_score"])
        round_goals = ( round_goals.groupby("round", as_index=False)["total_goals"].sum() )
        round_order=["Group stage", "Round of 32", "Round of 16", "Quarter-finals", "Semi-finals", "Third-place match", "Final" ]
        #df for round goals sorted by round
        round_goals["round"] = pd.Categorical( round_goals["round"], categories=round_order, ordered=True )

        #matches round goals bar chart
        fig_matches_round_goals = px.bar(
                round_goals,
                x="round",
                y="total_goals",
                category_orders={
                    "round":["Group stage", "Round of 32", "Round of 16", "Quarter-finals", "Semi-finals", "Third-place match", "Final" ]
                },
                labels={
                    "total_goals":"Goals",
                    "round":"Round"
                }
                )

        #plot matches "Goals by Round" bar chart
        with st.container(border=True):
            st.subheader("Goals by Round")
            st.plotly_chart(fig_matches_round_goals,key="chart_o_matches_round_goals")

        #df for formations
        formations = pd.concat([filtered_df["home_formation"], filtered_df["away_formation"]])
        formation_counts = formations.value_counts().head(10)
        #matches "Most Common Formations" bar chart
        with st.container(border=True):
            st.header("Most Common Formations")
            st.bar_chart(
                formation_counts,
                x_label="Formation",
                y_label="Count",
                sort="-count",
                color="#60a394"
            )

#-----------------------------------------------goals---------------------------------------------------------------
    with ta2:
        st.header(":material/sports_soccer: Goals")
        #plot goals by round bar chart
        with st.container(border=True):
            st.subheader("Goals by Round")
            st.plotly_chart(fig_matches_round_goals,key="chart_g_matches_round_goals")

        #df for scores
        score_counts = (filtered_df["score"].value_counts().reset_index())
        #rename columns
        score_counts.columns = ["score", "matches"]

        #bar chart common scorelines
        fig_scorelines=px.bar(
            score_counts.head(5),
            x="score",
            y="matches",
            color_discrete_sequence=["#876ef5"],
            labels={
                "score":"Score",
                "matches":"Matches"
            }
        )
        #plot chart common scorelines
        with st.container(border=True):
            st.subheader("Most Common Scorelines")
            st.plotly_chart(fig_scorelines)
        

        #df for goals vs shots by match
        chart_df = filtered_df[ ["home_team","away_team","score","home_score","away_score","home_total_shots","away_total_shots"] ].copy()

        #total goals in the match
        chart_df["total_goals"] =( chart_df["home_score"] + chart_df["away_score"])
        #total shots in the match
        chart_df["total_shots"] =(chart_df["home_total_shots"] + chart_df["away_total_shots"])
        #Match name
        chart_df["match"]=(chart_df["home_team"] + " vs " + chart_df["away_team"])

        #scatter chart goals vs shots
        fig_goals_shots = px.scatter(
            chart_df,
            x="total_shots",
            y="total_goals",
            hover_name="match",
            hover_data={
                "home_total_shots":True,
                "away_total_shots":True,
                "total_shots": True,
                "total_goals": True,
                "score": True
            },
            labels={
                "total_shots": "Total Shots",
                "total_goals": "Total Goals"
            }
        )
        #plot scatter chart goals vs shots
        with st.container(border=True):
            st.subheader("Goals vs Shots by Match")
            st.plotly_chart(fig_goals_shots)
        

        #df for goals scored per day
        daily_goals = filtered_df.copy()
        daily_goals["date"]=pd.to_datetime(daily_goals["date"])
        daily_goals["total_goals"]=(daily_goals["home_score"] + daily_goals["away_score"])
        daily_goals = (daily_goals.groupby("date")["total_goals"].sum().reset_index().sort_values("date"))

        #lines chart total goals by day
        fig_goals_by_day = px.line(
            daily_goals,
            x="date",
            y="total_goals",
            markers=True,
            labels={
                "date": "Date",
                "total_goals": "Goals"
            }
        )
        #plot line chart total goals by day 
        with st.container(border=True):
            st.subheader("Goals Scored per Day")
            st.plotly_chart(fig_goals_by_day)

#-------------------------------------------------------Match Stats------------------------------------------
    with ta3:
        st.header(":material/query_stats: Match Statistics")
        #funtion to create scatter chart comparison
        def create_comparison_scatter(home_col,away_col,x_label,y_label):
            #df for chart
            chart_df= filtered_df[["home_team","away_team","score",home_col,away_col]].copy()
            chart_df["match"]= ( chart_df["home_team"]+ " vs "+ chart_df["away_team"] )
            #scatter chart
            fig = px.scatter(
                chart_df,
                x=home_col,
                y=away_col,
                hover_name="match",
                hover_data=["score"],
                labels={
                    home_col: x_label,
                    away_col: y_label
                }
            )

            return fig


        #df for possession
        possession_df = filtered_df.copy()
        possession_df["match"]=(possession_df["home_team"]+ " vs " +possession_df["away_team"])
        
        #bar chart for match possession
        fig_possession = px.bar(
            possession_df,
            x="match",
            y=["home_possession","away_possession"],
            orientation="v",
            barmode="stack",
            labels={
                "value": "Possession (%)",
                "match": "Match"
            }
        )
        #plot match possession
        with st.container(border=True):
            st.subheader("Match possession")
            st.plotly_chart(fig_possession)

        #scatter charts home,away comparison for match stats
        col1,col2=st.columns(2)
        with col1:
            #shots scatter chart
            with st.container(border=True):
                st.subheader("Shots: Home vs Away")
                st.plotly_chart( create_comparison_scatter("home_total_shots","away_total_shots","Home shots","Away shots") )

            #saves scatter chart
            with st.container(border=True):
                st.subheader("Saves: Home vs Away")
                st.plotly_chart( create_comparison_scatter("home_saves","away_saves","Home saves","Away saves"))

            #crosses scatter chart
            with st.container(border=True):
                st.subheader("Crosses: Home vs Away")
                st.plotly_chart( create_comparison_scatter("home_crosses","away_crosses","Home crosses","Away crosses"))

        with col2:
            #SoT scatter chart
            with st.container(border=True):
                st.subheader("Shots on Target: Home vs Away")
                st.plotly_chart( create_comparison_scatter("home_sot","away_sot","Home shots on target","Away shots on target"))

            #interceptions scatter chart
            with st.container(border=True):
                st.subheader("Interceptions: Home vs Away")
                st.plotly_chart( create_comparison_scatter("home_interceptions","away_interceptions","Home interceptions","Away interceptions"))

            #corners scatter chart
            with st.container(border=True):
                st.subheader("Corners: Home vs Away")
                st.plotly_chart( create_comparison_scatter("home_corners","away_corners","Home corners","Away corners"))
    
#-------------------------Discipline------------------------------------------------------------------------------------
    with ta4:
        st.header(":material/sports: Discipline")

        #df for cards
        cards_by_round = filtered_df.copy()
        #yellow cards
        cards_by_round["yellow_cards"]=(cards_by_round["home_cards_yellow"] +cards_by_round["away_cards_yellow"])
        #red card
        cards_by_round["red_cards"] =(cards_by_round["home_cards_red"] +cards_by_round["away_cards_red"])
        cards_by_round=(cards_by_round.groupby("round")[["yellow_cards", "red_cards"]].sum().reset_index().sort_values("round"))    

        #bar chart for cards
        fig_cards_by_round = px.bar(
            cards_by_round,
            x="round",
            y=["yellow_cards", "red_cards"],
            barmode="group",
            labels={
                "round": "Round",
                "value": "Cards",
                "variable": "Card Type"
            },
            color_discrete_map={
                "yellow_cards": "#ebe959",
                "red_cards": "#e33b3b"
            },
            category_orders={
                "round": ["Group stage","Round of 32","Round of 16","Quarter-finals","Semi-finals","Third-place match","Final"]
            }
        )
        #plot bar chart for cards
        with st.container(border=True):
            st.subheader("Cards by Round")
            st.plotly_chart(fig_cards_by_round)

        #scatter charts home,away comparison for discipline stats
        col1,col2=st.columns(2)
        with col1:
            #yellow cards scatter chart
            with st.container(border=True):
                st.subheader("Yellow cards: Home vs Away")
                st.plotly_chart( create_comparison_scatter( "home_cards_yellow","away_cards_yellow","Home yellow cards","Away yellow cards") )
            
            #offsides scatter chart
            with st.container(border=True):
                st.subheader("Offsides: Home vs Away")
                st.plotly_chart( create_comparison_scatter("home_offsides","away_offsides","Home offsides","Away offsides"))
        with col2:
            #red cards scatter chart
            with st.container(border=True):
                st.subheader("Red cards: Home vs Away")
                st.plotly_chart(create_comparison_scatter("home_cards_red","away_cards_red","Home red cards","Away red cards"))
            
            #Fouls scatter chart
            with st.container(border=True):
                st.subheader("Fouls: Home vs Away")
                st.plotly_chart(create_comparison_scatter("home_fouls","away_fouls","Home fouls","Away fouls"))
        
#-----------------------------------------------Attendance----------------------------------------------------------------------------------------------
    with ta5:
        st.header(":material/crowdsource: Attendance")
        #df for attendance
        attendance_df=filtered_df.copy()
        attendance_df["attendance"]= pd.to_numeric(attendance_df["attendance"])
        attendance_df["date"]= pd.to_datetime(attendance_df["date"])
        attendance_df["match"]= ( attendance_df["home_team"]+ " vs "+ attendance_df["away_team"] )
        attendance_df = attendance_df.dropna(subset=["attendance"])
        #attendance over time
        attendance_over_time = (attendance_df.groupby("date")["attendance"].mean().reset_index().sort_values("date"))
        
        #line chart for attendace over time
        fig_attendance_over_time = px.line(
            attendance_over_time,
            x="date",
            y="attendance",
            markers=True,
            labels={
                "date": "Date",
                "attendance": "Attendance"
            }
        )
        #plot line chart for attendace over time
        with st.container(border=True):
            st.subheader("Attendance Over Time")
            st.plotly_chart(fig_attendance_over_time)

        #df for average attendance by round
        attendance_by_round= (attendance_df.groupby("round")["attendance"].mean().reset_index().sort_values("round"))
        
        #bar chart average attendance by round
        fig_average_attendance = px.bar(
            attendance_by_round,
            x="round",
            y="attendance",
            labels={
                "round": "Round",
                "attendance": "Average Attendance"
            },
            category_orders={
                "round": ["Group stage","Round of 32","Round of 16","Quarter-finals","Semi-finals","Third-place match","Final"]
            }
        )
        #plot bar chart average attendance by round
        with st.container(border=True):
            st.subheader("Average Attendance by Round")
            st.plotly_chart( fig_average_attendance )

        #df for Highest Attended Matches
        highest_attendance=(attendance_df.sort_values("attendance", ascending=False).head(15).sort_values("attendance"))   
        #bar chart highest_attendance
        fig_highest_attendance = px.bar(
            highest_attendance,
            x="attendance",
            y="match",
            orientation="h",
            labels={
                "attendance": "Attendance",
                "match": "Match"
            },
            color="attendance"
        )

        #df for lowest_attendance matches
        lowest_attendance=(attendance_df.sort_values("attendance", ascending=True).head(15).sort_values("attendance", ascending=False))
        #bar chart lowest_attendance
        fig_lowest_attendance = px.bar(
            lowest_attendance,
            x="attendance",
            y="match",
            orientation="h",
            labels={
                "attendance":"Attendance",
                "match":"Match"
            },
            color="attendance"
        )

        #plot charts highest and lowest attendance
        col1,col2=st.columns(2)
        with col1:
            #plot bar chart highest attendance
            with st.container(border=True):
                st.subheader("Highest Attended Matches")
                st.plotly_chart( fig_highest_attendance )

        #plot bar chart lowest_attendance
        with col2:
            with st.container(border=True):
                st.subheader("Lowest Attended Matches")
                st.plotly_chart( fig_lowest_attendance )
    
    
#-----------------------------------------------------team matches--------------------------------
with tab2:
    st.header(":material/select: Team Matches")

    #df for team matches
    match_metrics=df.copy()

    #select team
    team = match_metrics["home_team"].unique().tolist()
    team.sort()
    selected_team= st.selectbox(":material/filter_alt: Select team", team)
    mm_home = match_metrics[match_metrics["home_team"] == selected_team]
    mm_away = match_metrics[match_metrics["away_team"] == selected_team]
    frames = [mm_home, mm_away]
    match_metrics = pd.concat(frames)
    #date selection
    dates = match_metrics["date"].unique().tolist()
    dates.sort()
    selected_date = st.selectbox(":material/filter_alt: Select date", dates)
    #df for team selected metrics considering the date 
    match_metrics = match_metrics[match_metrics["date"] == selected_date]

    #home and away metrics
    h_team = match_metrics["home_team"].iloc[0]
    a_team = match_metrics["away_team"].iloc[0]
    
    #team selected and rival of said matchday
    st.header(f"{h_team} | {match_metrics["score"].iloc[0]} | {a_team}",text_alignment="center")
    
    #match datetime, location, attendance
    c1,c2,c3=st.columns(3)
    with c1:#datetime
        st.caption(f":material/schedule: Date and Time:{match_metrics["date"].iloc[0]}, {match_metrics["start_time"].iloc[0]}",text_alignment="center")
    with c2:#location
        st.caption(f":material/globe_location_pin: Location: {match_metrics["venue"].iloc[0]}",text_alignment="center")
    with c3:#attendance
        st.caption(f":material/crowdsource: Attendance: {match_metrics["attendance"].iloc[0]}",text_alignment="center")

    #match details home and away , manager, captain, referee, round
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(f"{h_team} Manager", match_metrics["home_manager"].iloc[0],  border=True, icon=":material/badge:")
        st.metric(f"{h_team} Captain", match_metrics["home_captain"].iloc[0],  border=True, icon=":material/assignment_ind:")

    with col2:
        st.metric(f"{a_team} Manager", match_metrics["away_manager"].iloc[0],  border=True, icon=":material/badge:")
        st.metric(f"{a_team} Captain", match_metrics["away_captain"].iloc[0],  border=True, icon=":material/assignment_ind:")

    with col3:
        st.metric("Referee", match_metrics["referee"].iloc[0], border=True,icon=":material/sports:")
        st.metric("Round", match_metrics["round"].iloc[0], border=True,icon=":material/calendar_month:")
    st.divider()

    #match Stats 
    st.header(":material/query_stats: Match Statistics")

    #home and away possesion
    home_possession = match_metrics["home_possession"].iloc[0]
    away_possession = match_metrics["away_possession"].iloc[0]
    #df for possesion
    possession = pd.DataFrame({
        "Team": [h_team, a_team],
        "Possession": [home_possession, away_possession],
        "Order": [1, 2]
    })

    #bar chart for possesion of each team, left home possesion, right away possesion
    chart_possession = alt.Chart(possession).mark_bar(height=35).encode(
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
                domain=[h_team, a_team],
                range=['#eb9736','#36A2EB']
            ),
            legend=None
        )
    ).properties( width=700, height=50 )

    #df for match performance by team
    match = match_metrics.iloc[0]
    #name of metrics displayed
    metrics = ["Red cards","Yellow cards","Offsides","Fouls","Corners","Crosses","Interceptions","Saves","Shots on target","Shots"]
    #df for home team performance
    data_home = pd.DataFrame({
        "Metric": metrics,
        "Value": [match["home_cards_red"],match["home_cards_yellow"], match["home_offsides"], match["home_fouls"], match["home_corners"], match["home_crosses"], match["home_interceptions"], match["home_saves"], match["home_sot"], match["home_total_shots"]]
    })
    #df for away team performance
    data_away = pd.DataFrame({
        "Metric": metrics,
        "Value": [match["away_cards_red"], match["away_cards_yellow"], match["away_offsides"], match["away_fouls"], match["away_corners"], match["away_crosses"], match["away_interceptions"], match["away_saves"], match["away_sot"], match["away_total_shots"]]
    })

    #function for bar chart of performance
    def create_stats_chart(data, color):
        fig = px.bar(
            data,
            x="Value",
            y="Metric",
            orientation="h"
        )
        fig.update_traces(marker_color=color)
        fig.update_layout( height=300, showlegend=False, xaxis_title=None, yaxis_title=None)

        return fig

    #create bar charts for home team and away team performance
    chart_home = create_stats_chart(data_home, "#eb9736")
    chart_away = create_stats_chart(data_away, "#36A2EB")

    #plot possesion of each team
    st.subheader(":material/percent: Possession",text_alignment="center")
    st.altair_chart( chart_possession )
    
    #plot performance of each team
    teamA, teamB=st.columns(2)
    with teamA:#home team: name, performance stats, team formation
        st.subheader(h_team)
        st.plotly_chart(chart_home, config={"displayModeBar": False})
        st.metric(f"{h_team} formation", match_metrics["home_formation"].iloc[0], icon=":material/tactic:")

    with teamB:#away team: name, performance stats, team formation
        st.subheader(a_team)
        st.plotly_chart(chart_away, config={"displayModeBar": False})
        st.metric(f"{a_team} formation", match_metrics["away_formation"].iloc[0], icon=":material/tactic:", )
