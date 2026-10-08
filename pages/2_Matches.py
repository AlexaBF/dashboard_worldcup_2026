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

 

tab1,tab2=st.tabs(["All Matches","Team Matches"])


#--------------------------------------------------filtered rounds-----------------------------------------
with tab1:
    overview_df=df.copy()

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
#------------------------------------------------------------------------------------

    #tabla de datos
    all_matches=filtered_df[["round","home_team","away_team","score","attendance","venue"]]
    st.dataframe(all_matches)

    ta1, ta2, ta3, ta4, ta5 = st.tabs(["Overview","Goals","Match Stats","Discipline","Attendance"])

#------------------------------------overview----------------------------------------------------
    with ta1:
        #total matches, total goals, avg attendance)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Matches", total_matches, border=True,icon=":material/calendar_month:")
        col2.metric("Goals", total_goals, border=True, icon=":material/sports_soccer:")
        col3.metric("Average Attendance", f"{avg_attendance:,.0f}",border=True,icon=":material/event_seat:" )
        col4.metric("average goal", avg_goals,  border=True, icon=":material/sports_and_outdoors:") 

        #-----------------------------------home win, draw , away win-
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
        
        result_counts = (
            hda["result"]
            .value_counts()
            .reindex(["Home Win", "Draw", "Away Win"], fill_value=0)
        )

        with st.container(border=True):
            st.subheader("Wins for home vs away team")
            st.bar_chart(
                result_counts,
                sort=False,
                color="#f5a06e"
        )  

        #-------------------------------------------

        #-------------------------------------------goals by round
        round_goals = filtered_df[["round", "home_score", "away_score"]]

        round_goals["total_goals"] = (
            round_goals["home_score"] + round_goals["away_score"]
        )

        round_goals = (
            round_goals
            .groupby("round", as_index=False)["total_goals"]
            .sum()
        )

        round_order = [
            "Group stage",
            "Round of 32",
            "Round of 16",
            "Quarter-finals",
            "Semi-finals",
            "Third-place match",
            "Final"
        ]

        round_goals["round"] = pd.Categorical(
            round_goals["round"],
            categories=round_order,
            ordered=True
        )

        round_goals = round_goals.sort_values("round")

        with st.container(border=True):
            st.subheader("Goals by Round")
            st.bar_chart(
                round_goals,
                x="round",
                x_label="Round",
                y="total_goals",
                y_label="Goals",
                color="blue"
            )     
    
        #-------------------------------------------------------------------------

        formations = pd.concat([filtered_df["home_formation"], filtered_df["away_formation"]])
        formation_counts = formations.value_counts().head(10)

        
        with st.container(border=True):
            st.header("Most Common Formations")
            st.bar_chart(formation_counts, x_label="Formation", y_label="Count",sort="-count",
            color="#60a394")
        #------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------------------
#-----------------------------------------------goals---------------------------------------------------------------

    with ta2:
        
        with st.container(border=True):
            st.subheader("Goals by Round")
            st.bar_chart(
                round_goals,
                x="round",
                x_label="Round",
                y="total_goals",
                y_label="Goals",
                color="blue"
            )

        #---------------------------------------------------------
        score_counts = (
            filtered_df["score"]
            .value_counts()
            .reset_index()
        )

        score_counts.columns = ["score", "matches"]

        with st.container(border=True):
            st.subheader("Most Common Scorelines")
            st.bar_chart(
                score_counts.head(10),
                x="score",
                y="matches",
                sort="-matches",
                color="#876ef5"
            )
        #-------------------------------------------------
        
        #----------------goals  vs shots----------------------------
        home_stats = filtered_df[ ["home_team", "home_score", "home_total_shots"]].copy()
        home_stats.columns = ["team", "goals", "shots"]

        away_stats = filtered_df[ ["away_team", "away_score", "away_total_shots"] ].copy()
        away_stats.columns = ["team", "goals", "shots"]

        goals_shots_df = pd.concat([home_stats, away_stats],ignore_index=True)
        goals_shots_df["goals"] = pd.to_numeric(goals_shots_df["goals"])
        goals_shots_df["shots"] = pd.to_numeric( goals_shots_df["shots"] )
        goals_shots_df = goals_shots_df.dropna( subset=["goals", "shots"])

        fig = px.scatter(
            goals_shots_df,
            x="shots",
            y="goals",
            hover_name="team",
            labels={
                "shots": "Total Shots",
                "goals": "Goals"
            }
        )

        with st.container(border=True):
            st.subheader("Goals vs Shots")

            st.plotly_chart(
                fig,
                use_container_width=True
            )


        

        #----goals vs shots by m,atch
        def create_match_goals_vs_shots():
            chart_df = filtered_df[ ["home_team","away_team","score","home_score","away_score","home_total_shots","away_total_shots"] ].copy()

            numeric_cols = ["home_score","away_score","home_total_shots","away_total_shots"]
            for col in numeric_cols:
                chart_df[col] = pd.to_numeric(chart_df[col])

            chart_df = chart_df.dropna(subset=numeric_cols)

            # Total goals in the match
            chart_df["total_goals"] =( chart_df["home_score"] + chart_df["away_score"])

            # Total shots in the match
            chart_df["total_shots"] =(chart_df["home_total_shots"] + chart_df["away_total_shots"])

            # Match name
            chart_df["match"]=(chart_df["home_team"] + " vs " + chart_df["away_team"])

            fig = px.scatter(
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

            return fig

        goals_shots_scatter = create_match_goals_vs_shots()
        with st.container(border=True):
            st.subheader("Goals vs Shots by Match")

            st.plotly_chart(
                goals_shots_scatter,
                use_container_width=True)
        
        


        #----------goals scored per day---------------------
        daily_goals = filtered_df.copy()
        daily_goals["date"]=pd.to_datetime(daily_goals["date"])
        daily_goals["total_goals"]=(daily_goals["home_score"] + daily_goals["away_score"])

        daily_goals = (daily_goals.groupby("date")["total_goals"].sum().reset_index().sort_values("date"))

        fig = px.line(
            daily_goals,
            x="date",
            y="total_goals",
            markers=True,
            labels={
                "date": "Date",
                "total_goals": "Goals"
            }
        )

        with st.container(border=True):
            st.subheader("Goals Scored per Day")
            st.plotly_chart(
                fig,
                use_container_width=True
            )

#------------------------------------------------------------------------------------
#-------------------------------------------------------Match Stats------------------------------------------
    with ta3:
        def create_comparison_scatter(home_col,away_col,x_label,y_label):
            chart_df = filtered_df[["home_team","away_team","score",home_col,away_col]].copy()

            chart_df[home_col] = pd.to_numeric(chart_df[home_col])
            chart_df[away_col] = pd.to_numeric(chart_df[away_col])
            chart_df = chart_df.dropna(subset=[home_col, away_col])
            chart_df["match"] = (chart_df["home_team"]+ " vs "+ chart_df["away_team"])

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



        st.subheader("Match Statistics")


        # ---------------- POSSESSION ----------------
        possession_df = filtered_df.copy()

        possession_df["home_possession"] = pd.to_numeric(possession_df["home_possession"])
        possession_df["away_possession"] = pd.to_numeric(possession_df["away_possession"])

        possession_df = possession_df.dropna(subset=["home_possession","away_possession"])
        possession_df["match"]=(possession_df["home_team"]+ " vs " +possession_df["away_team"])

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

        #
        with st.container(border=True):
            st.subheader("Match possession")
            st.plotly_chart(
                fig_possession,
                use_container_width=True
            )

        col1,col2=st.columns(2)
        with col1:
            # -------------------------------- SHOTS ----------------
            with st.container(border=True):
                st.subheader("Shots: Home vs Away")
                st.plotly_chart(
                    create_comparison_scatter("home_total_shots","away_total_shots","Home shots","Away shots"),
                    use_container_width=True
                )

            # ---------------- SAVES ----------------
            with st.container(border=True):
                st.subheader("Saves: Home vs Away")
                st.plotly_chart(
                    create_comparison_scatter("home_saves","away_saves","Home saves","Away saves"),
                    use_container_width=True
                )

            # ---------------- CROSSES ----------------
            with st.container(border=True):
                st.subheader("Crosses: Home vs Away")
                st.plotly_chart(
                    create_comparison_scatter("home_crosses","away_crosses","Home crosses","Away crosses"),
                    use_container_width=True
                )

        with col2:
            # ---------------------------- SHOTS ON TARGET ----------------
            with st.container(border=True):
                st.subheader("Shots on Target: Home vs Away")
                st.plotly_chart(
                    create_comparison_scatter("home_sot","away_sot","Home shots on target","Away shots on target"),
                    use_container_width=True
                )

            # ---------------- INTERCEPTIONS ----------------
            with st.container(border=True):
                st.subheader("Interceptions: Home vs Away")
                st.plotly_chart(
                    create_comparison_scatter("home_interceptions","away_interceptions","Home interceptions","Away interceptions"),
                    use_container_width=True
                )

            # ---------------- CORNERS ----------------
            with st.container(border=True):
                st.subheader("Corners: Home vs Away")
                st.plotly_chart(
                    create_comparison_scatter("home_corners","away_corners","Home corners","Away corners"),
                    use_container_width=True
                )

        

        

        

       




       
#--------------------------------------------------------------------------------------------------------------
#-------------------------Discipline------------------------------------------------------------------------------------
    with ta4:
        cards_by_round = filtered_df.copy()
        #yellow cards
        cards_by_round["yellow_cards"]=(cards_by_round["home_cards_yellow"] +cards_by_round["away_cards_yellow"])

        #red card
        cards_by_round["red_cards"] =(cards_by_round["home_cards_red"] +cards_by_round["away_cards_red"])

        cards_by_round=(cards_by_round.groupby("round")[["yellow_cards", "red_cards"]].sum().reset_index().sort_values("round"))

        fig = px.bar(
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

        with st.container(border=True):
            st.subheader("Cards by Round")
            st.plotly_chart(
                fig,
                use_container_width=True,
                
            )



        col1,col2=st.columns(2)
        with col1:
            with st.container(border=True):
                st.subheader("Yellow cards: Home vs Away")
                st.plotly_chart(
                    create_comparison_scatter("home_cards_yellow","away_cards_yellow","Home yellow cards","Away yellow cards"),
                    use_container_width=True
                )
            
            with st.container(border=True):
                st.subheader("Offsides: Home vs Away")
                st.plotly_chart(
                    create_comparison_scatter("home_offsides","away_offsides","Home offsides","Away offsides"),
                    use_container_width=True
                )
        with col2:
            with st.container(border=True):
                st.subheader("Red cards: Home vs Away")
                st.plotly_chart(
                    create_comparison_scatter("home_cards_red","away_cards_red","Home red cards","Away red cards"),
                    use_container_width=True
                )

            with st.container(border=True):
                st.subheader("Fouls: Home vs Away")
                st.plotly_chart(
                    create_comparison_scatter("home_fouls","away_fouls","Home fouls","Away fouls"),
                    use_container_width=True
                )
        



        

#-----------------------------------------------Attendance----------------------------------------------------------------------------------------------
    with ta5:
        attendance_df=filtered_df.copy()

        attendance_df["attendance"]= pd.to_numeric(attendance_df["attendance"])
        attendance_df["date"]= pd.to_datetime(attendance_df["date"])
        attendance_df["match"]= ( attendance_df["home_team"]+ " vs "+ attendance_df["away_team"] )

        attendance_df = attendance_df.dropna(subset=["attendance"])
        attendance_over_time = (attendance_df.groupby("date")["attendance"].mean().reset_index().sort_values("date"))
        
        fig = px.line(
            attendance_over_time,
            x="date",
            y="attendance",
            markers=True,
            labels={
                "date": "Date",
                "attendance": "Attendance"
            }
        )

        with st.container(border=True):
            st.subheader("Attendance Over Time")
            st.plotly_chart(
                fig,
                use_container_width=True
            )

        attendance_by_round= (attendance_df.groupby("round")["attendance"].mean().reset_index().sort_values("round"))
        
        fig = px.bar(
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

        with st.container(border=True):
            st.subheader("Average Attendance by Round")
            st.plotly_chart(
                fig,
                use_container_width=True
            )


        highest_attendance=(attendance_df.sort_values("attendance", ascending=False).head(15).sort_values("attendance"))   
        fig = px.bar(
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

        col1,col2=st.columns(2)
        with col1:
            with st.container(border=True):
                st.subheader("Highest Attended Matches")
                st.plotly_chart(
                    fig,
                    use_container_width=True
                )
        #-----
        

        lowest_attendance=(attendance_df.sort_values("attendance", ascending=True).head(15).sort_values("attendance", ascending=False))
        fig = px.bar(
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
        #--------
        
        with col2:
            with st.container(border=True):
                st.subheader("Lowest Attended Matches")
                st.plotly_chart(
                    fig,
                    use_container_width=True
                )
    
    
#----------------------------------------------------------------------------------------------------------------------------
#---------------------team matches
with tab2:

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


    match = match_metrics.iloc[0]
    metrics = ["Red cards","Yellow cards","Offsides","Fouls","Corners","Crosses","Interceptions","Saves","Shots on target","Shots"]

    data_home = pd.DataFrame({
        "Metric": metrics,
        "Value": [match["home_cards_red"],
        match["home_cards_yellow"],
        match["home_offsides"],
        match["home_fouls"],
        match["home_corners"],
        match["home_crosses"],
        match["home_interceptions"],
        match["home_saves"],
        match["home_sot"],
        match["home_total_shots"]]
    })


    data_away = pd.DataFrame({
        "Metric": metrics,
        "Value": [match["away_cards_red"],
        match["away_cards_yellow"],
        match["away_offsides"],
        match["away_fouls"],
        match["away_corners"],
        match["away_crosses"],
        match["away_interceptions"],
        match["away_saves"],
        match["away_sot"],
        match["away_total_shots"]]
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
  