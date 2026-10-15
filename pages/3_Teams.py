import streamlit as st
import pandas as pd

st.title(":material/groups_3: TEAMS") 

@st.cache_data
def load_data():
    df=pd.read_csv("datasets/teams.csv")
    return df

df=load_data()

#------------------------------------basic info-----------------------------------
def get_team_with_the_most_or_least(the_most,most_or_least,dataframe):
    if most_or_least: #check for min or max
        best_num=dataframe[the_most].min()
    else:
        best_num=dataframe[the_most].max()
    #get list of teams
    best_teams=dataframe.loc[ dataframe[the_most] == best_num, "team" ].tolist() 
    best_team = ", ".join(best_teams)

    return best_num,best_team

#most goals scored
max_gf, max_gf_team = get_team_with_the_most_or_least("goals",0,df)
#most goals conceded
max_ga, max_ga_team = get_team_with_the_most_or_least("goals_against",0,df)
#least goals scored
min_gf, min_gf_team = get_team_with_the_most_or_least("goals",1,df)
#least goals conceded
min_ga, min_ga_team = get_team_with_the_most_or_least("goals_against",1,df)

#general metrics of teams
col1, col2=st.columns(2)
with col1:
    st.metric("Most goals scored", max_gf_team,
    delta= f"Goals: {max_gf:.0f}", delta_color="blue", delta_arrow="off",
    border=True, icon=":material/sentiment_excited:")

    st.metric("Least goals scored", min_gf_team,
    delta= f"Goals: {min_gf:.0f}", delta_color="blue", delta_arrow="off",
    border=True, icon=":material/sentiment_stressed:")

with col2:
    st.metric("Most goals conceded", max_ga_team,
    delta= f"Goals: {max_ga:.0f}", delta_color="blue", delta_arrow="off",
    border=True, icon=":material/sentiment_neutral:")

    st.metric("Least goals conceded", min_ga_team,
    delta= f"Goals: {min_ga:.0f}",  delta_color="blue", delta_arrow="off",
    border=True, icon=":material/sentiment_content:")
#---------------------------------------------------------------------------------
tab1,tab2= st.tabs([":material/groups_2: Multi-Team Stats", ":material/group_search: Team Profile"])
#-------------------------------------------------team profile----------------------------------------------------------
with tab2: 
    with st.container(border=True):
        st.header(":material/group_search: Team Profile")

        #select team 
        team_profile = st.selectbox(":material/filter_alt: Select a team",sorted(df["team"].unique()))
        filtered_team_profile = df[df["team"] == team_profile]

        #df of team selected
        df_team_selected=filtered_team_profile.copy()
        team_metric = df_team_selected.iloc[0]

        #team profile metrics
        tp1,tp2,tp3=st.columns(3)
        with tp1:
            st.metric("Age Average", team_metric["avg_age"],border=True, icon=":material/date_range:")
            st.metric("Goals", team_metric["goals"], border=True, icon=":material/sports_and_outdoors:")
            st.metric("Possession", f"{team_metric["possession"]:.2f} %", border=True, icon=":material/percent:")
            st.metric("Fouls", team_metric["fouls"], border=True, icon=":material/sports:")
        with tp2:
            st.metric("Number of Players", team_metric["players_used"], border=True, icon=":material/groups_2:")
            st.metric("Goals Conceded", team_metric["goals_against"], border=True, icon=":material/sports_soccer:")
            st.metric("Shots", team_metric["shots"], border=True, icon=":material/shoe_cleats:")
            st.metric("Yellow Cards", team_metric["cards_yellow"],border=True, icon=":material/crop_2_3:")

        with tp3:
            st.metric("Games played", team_metric["games"], border=True, icon=":material/scoreboard:")
            st.metric("Own Goals", team_metric["own_goals"], border=True, icon=":material/sports_soccer:")
            st.metric("Shot Accuracy", f"{team_metric["shots_on_target_pct"]:.2f} %", border=True, icon=":material/percent:")
            st.metric("Red Cards", team_metric["cards_red"],border=True, icon=":material/crop_2_3:")

    #team profile charts
    c1,c2=st.columns(2)
    with c1:
        #team goals comparison bar chart
        with st.container(border=True):
            st.subheader("Goals Comparison")
            st.bar_chart(
                df_team_selected,
                x="team",
                y=["goals","goals_against"],
                stack=False,
                color=["orange","blue"]
                )
        #team possession comparison bar chart
        with st.container(border=True):
            st.subheader("Possession Comparison")
            st.bar_chart(
                df_team_selected,
                x="team",
                y=["possession","possession_against"],
                stack=False,
                color=["orange","blue"]
            )
    with c2:
        #team shooting stats bar chart
        with st.container(border=True):
            st.subheader("Shooting Statistics")
            st.bar_chart(
                df_team_selected,
                x="team",
                y=["shots","shots_on_target"],
                stack=False
                )
        #team defensive bar chart
        with st.container(border=True):
            st.subheader("Defensive")
            st.bar_chart(
                df_team_selected,
                x="team",
                y=["fouls","tackles_won"],
                stack=False
            )
#----------------------------------------------------Teams-----------------------------------------------------------
with tab1:
    with st.container(border=True):
        st.header(":material/groups_2: Multi-Team Stats")
        #select teams to compare
        teams_selected = st.multiselect(":material/filter_alt: Select Teams", df["team"].unique(), default=df["team"].unique())
        filtered_team=df[ df["team"].isin(teams_selected) ]#df for teams selected
        #choose at least three teams
        if len(teams_selected)<3:
            st.warning("Select at least three teams")
            st.stop()

        tab1,tab2,tab3,tab4,tab5 = st.tabs([":material/shoe_cleats: Offensive",":material/shield: Defensive", ":material/percent: Possesion", ":material/balance: Offensive vs Defensive",":material/sports: Discipline"])
#----------------------------------------------------offensive performance--------------------------------------
    with tab1:
        st.header(":material/shoe_cleats: Offensive performance")

        #df for teams offensive charts
        teams_offensive=filtered_team[ ["team","minutes", "goals_per90", "shots_on_target_pct","goals_per_shot_on_target","shots_per90","shots_on_target_per90","assists_per90","goals_per_shot","possession"] ].copy()
        
        #best scoring team
        best_scoring,best_scoring_team= get_team_with_the_most_or_least("goals_per90",0,teams_offensive)
        #Most Attacking Volume
        most_attacks, most_attacks_team=get_team_with_the_most_or_least("shots_per90",0,teams_offensive)
        #best finishing
        best_finish,best_finish_team= get_team_with_the_most_or_least("goals_per_shot_on_target",0,teams_offensive)
        #Most shots on target
        most_sot,most_sot_team = get_team_with_the_most_or_least("shots_on_target_per90",0,teams_offensive)
        #best  assist
        most_assist,most_assist_team = get_team_with_the_most_or_least("assists_per90",0,teams_offensive)
        # Shot accuracy
        most_shot_accuracy,most_shot_accuracy_team= get_team_with_the_most_or_least("shots_on_target_pct",0,teams_offensive)
        # Goals per shot
        most_goal_sper_shot, goals_per_shot_team = get_team_with_the_most_or_least("goals_per_shot",0,teams_offensive)
        # Possession
        most_possession, most_possession_team = get_team_with_the_most_or_least("possession",0,teams_offensive)

        #teams offensive comparison metrics
        o1, o2=st.columns(2)
        with o1:
            st.metric("Best Scoring Team", best_scoring_team,
            delta= f"Goals per 90: {best_scoring:.1f}", delta_color="blue", delta_arrow="off",
            border=True, icon=":material/sports_soccer:")

            st.metric("Best Shot Conversion", best_finish_team,
            delta= f"SoT scored: {best_finish:.1%}", delta_color="blue", delta_arrow="off",
            border=True, icon=":material/target:")

            st.metric("Most Assists per 90", most_assist_team,
            delta= f"Assists: {most_assist:.2f}", delta_color="blue", delta_arrow="off",
            border=True, icon=":material/partner_exchange:")

            st.metric("Most Goals per shot", goals_per_shot_team,
            delta= f"Goals: {most_goal_sper_shot:.2f}", delta_color="blue", delta_arrow="off",
            border=True, icon=":material/sports_and_outdoors:")
        
        with o2:
            st.metric("Most Shots per 90", most_attacks_team,
            delta= f"Shots per 90: {most_attacks:.1f}", delta_color="blue", delta_arrow="off",
            border=True, icon=":material/shoe_cleats:")

            st.metric("Most shots on target", most_sot_team,
            delta= f"SoT per 90: {most_sot:.1f}", delta_color="blue", delta_arrow="off",
            border=True, icon=":material/target:")

            st.metric("Best shot accuracy", most_shot_accuracy_team,
            delta= f"Accuracy: {most_shot_accuracy:.2f}%", delta_color="blue", delta_arrow="off",
            border=True, icon=":material/percent:")
            
            st.metric("Possesion", most_possession_team,
            delta= f"Possesion: {most_possession:.2f}%", delta_color="blue", delta_arrow="off",
            border=True, icon=":material/percent:")
        
        #Shots per 90 vs Goals per 90 scatter chart
        with st.container(border=True):
            st.subheader("Shots per 90 vs Goals per 90")
            st.scatter_chart(teams_offensive,
                x="shots_per90",
                y="goals_per90",
                x_label="Shots per 90",
                y_label="Goals per 90",
                color="team",
                size="minutes")

        #shot and Sot per 90 scatter chart
        with st.container(border=True):
            st.subheader("Shot per 90 vs SoT per 90")
            st.scatter_chart(teams_offensive,
                x="shots_per90",
                y="shots_on_target_per90",
                x_label="Shots per 90",
                y_label="Shots on Target per 90",
                color="team",
                size="minutes")
        
        #shot accuracy bar chart
        with st.container(border=True):
            st.subheader("Shot Accuracy (%) Ranking")
            st.bar_chart(teams_offensive,
            x="team",
            y="shots_on_target_pct",
            x_label="Team",
            y_label="shots on target %",
            sort="-shots_on_target_pct")

        #goals pershot on target bar chart
        with st.container(border=True):
            st.subheader("Goals per shot on target")
            st.bar_chart(teams_offensive,
            x="team",
            y="goals_per_shot_on_target",
            x_label="Team",
            y_label="goals per shot",
            sort="-goals_per_shot_on_target")        

#-----------------------------------------------defensive-------------------------------------------------
    with tab2:
        st.header(":material/shield: Defensive performance")

        #df for team defensive
        teams_defensive=filtered_team[ ["team","minutes", "goals_per90_against", "shots_per90_against","goals_per_shot_against","shots_on_target_per90_against","gk_save_pct","gk_clean_sheets_pct", "interceptions","tackles_won"] ].copy()

        #best defense
        best_defense,best_defense_team  = get_team_with_the_most_or_least("goals_per90_against",1,teams_defensive)
        #best shot blocking
        shot_block, shot_block_team  = get_team_with_the_most_or_least("shots_per90_against",1,teams_defensive)
        #best defensive efficiency
        defense_efficiency, defense_efficiency_team  = get_team_with_the_most_or_least("goals_per_shot_against",1,teams_defensive)
        #best SOT blocking
        sot_block,sot_block_team = get_team_with_the_most_or_least("shots_on_target_per90_against",1,teams_defensive)
    
        #most saves
        most_saves, most_saves_team = get_team_with_the_most_or_least("gk_save_pct",0,teams_defensive)
        #clean sheets 
        most_clean, most_clean_team = get_team_with_the_most_or_least("gk_clean_sheets_pct",0,teams_defensive)
        # Interceptions
        most_interceptions, most_interceptions_team = get_team_with_the_most_or_least("interceptions",0,teams_defensive)
        # Tackles won
        most_tackles_won, most_tackles_won_team = get_team_with_the_most_or_least("tackles_won",0,teams_defensive)

        #teams defensive comparison metrics
        d1, d2=st.columns(2)
        with d1:
            st.metric("Best Defense", best_defense_team,
            delta= f"Goals conceded per 90: {best_defense:.2f}", delta_color="blue", delta_arrow="off",
            border=True, icon=":material/shield_person:")

            st.metric("Best Shot Blocking", shot_block_team,
            delta= f"Shots conceded per 90: {shot_block:.2f}", delta_color="blue", delta_arrow="off",
            border=True, icon=":material/guardian:")

            st.metric("Most Saves by Gk", most_saves_team,
            delta= f"Saves: {most_saves:.2f}%", delta_color="blue", delta_arrow="off",
            border=True, icon=":material/percent:")

            st.metric("Most Interceptions", most_interceptions_team,
            delta=f"Interceptions: {most_interceptions:.0f}", delta_color="blue", delta_arrow="off",
            border=True, icon=":material/cheer:")

        with d2:
            st.metric("Best Defensive Efficiency", defense_efficiency_team,
            delta= f"Goals per shots conceded: {defense_efficiency:.2f}", delta_color="blue", delta_arrow="off",
            border=True, icon=":material/speed_2:")

            st.metric("Best SOT Blocking", sot_block_team,
            delta= f"SoT conceded per 90: {sot_block:.2f}", delta_color="blue", delta_arrow="off",
            border=True, icon=":material/crisis_alert:")

            st.metric("Most Clean Sheets", most_clean_team,
            delta= f"Clean Sheets: {most_clean:.2f}%", delta_color="blue", delta_arrow="off",
            border=True, icon=":material/percent:")

            st.metric("Most Tackles Won", most_tackles_won_team,
            delta= f"Tackles: {most_tackles_won:.0f}", delta_color="blue", delta_arrow="off",
            border=True, icon=":material/cheer:")
            
        #teams shots conceded vs goals conceded scatter chart
        with st.container(border=True):
            st.subheader("Shots conceded vs Goals conceded")
            st.scatter_chart(
                teams_defensive,
                x="shots_per90_against",
                y="goals_per90_against",
                x_label="Shots per 90 Conceded",
                y_label="Goals per 90 Conceded",
                color="team",
                size="minutes")
        
        #teams interceptions vs tackles won scatter chart
        with st.container(border=True):
            st.subheader("Interceptions vs Tackles Won")
            st.scatter_chart(
                teams_defensive,
                x="interceptions",
                y="tackles_won",
                x_label="Interceptions",
                y_label="Tackles Won",
                color="team",
                size="minutes")

        #teams goalkeeper saves and clean sheets scatter chart
        with st.container(border=True):
            st.subheader("Goalkeeper Saves and Clean sheets")
            st.scatter_chart(
                teams_defensive,
                x="gk_save_pct",
                y="gk_clean_sheets_pct",
                x_label="Save %",
                y_label="Clean Sheets %",
                color="team",
                size="minutes")
        
#------------------------------------------possession--------------------------------------------------------
    with tab3:
        st.header(":material/percent: Team possesion")

        #df for team possession
        teams_possession=filtered_team[ ["team","minutes","possession","goals_per90","shots_per90","assists_per90","shots_on_target_per90"] ].copy()
        
        # goals_per90
        goals_90, goals_90_team  = get_team_with_the_most_or_least("goals_per90",0,teams_possession)
        # shots_per90
        shots_90, shots_90_team  = get_team_with_the_most_or_least("shots_per90",0,teams_possession)
        # assists_per90
        assists_90, assists_90_team = get_team_with_the_most_or_least("assists_per90",0,teams_possession)
        # shots_on_target_per90
        sot_90, sot_90_team = get_team_with_the_most_or_least("shots_on_target_per90",0,teams_possession)
        #Higest possession
        high_possession, high_possession_team = get_team_with_the_most_or_least("possession",0,teams_possession)

        #teams possession comparison metrics
        p1, p2=st.columns(2)
        with p1:
            st.metric("Higest possession", high_possession_team,
            delta= f"Possession: {high_possession:.2f} %", delta_color="blue", delta_arrow="off",
            border=True, icon=":material/percent:")

            st.metric("Goals per 90", goals_90_team,
            delta= f"Goals: {goals_90:.2f}", delta_color="blue", delta_arrow="off",
            border=True, icon=":material/sports_and_outdoors:")

            st.metric("Shots on target per 90", sot_90_team,
            delta= f"SoT: {sot_90:.2f}", delta_color="blue", delta_arrow="off",
            border=True, icon=":material/target:")
  
        with p2:
            st.metric("Most Assists per 90", assists_90_team,
            delta= f"Assists: {assists_90:.2f}", delta_color="blue", delta_arrow="off",
            border=True, icon=":material/cheer:")

            st.metric("Shots per 90", shots_90_team,
            delta= f"Shots: {shots_90:.2f}", delta_color="blue", delta_arrow="off",
            border=True, icon=":material/shoe_cleats:")
        
        #teams possession vs goals per 90 scatter chart
        with st.container(border=True):
            st.subheader("Possession vs Goals per 90")
            st.scatter_chart(
                teams_possession,
                x="possession",
                y="goals_per90",
                x_label="Possession %",
                y_label="Goals per 90",
                color="team",
                size="minutes")

        #teams possession vs shots per 90 scatter chart
        with st.container(border=True):
            st.subheader("Possession vs Shots per 90")
            st.scatter_chart(
                teams_possession,
                x="possession",
                y="shots_per90",
                x_label="Possession %",
                y_label="Shots per 90",
                color="team",
                size="minutes")

        #teams possesion bar chart
        with st.container(border=True):
            st.subheader("Team possesion")
            st.bar_chart(teams_possession,
            x="team",
            y="possession",
            x_label="Team",
            y_label="Possesion %",
            sort="-possession")

#-------------------------------------offensive vs defensive performance---------------------------------------
    with tab4:
        st.header(":material/balance: Offensive vs Defensive Performance")

        #df for team performance
        team_performance = filtered_team[ ["team", "goals_per90", "goals_per90_against", "shots_per90","shots_per90_against","shots_on_target_per90","shots_on_target_per90_against","points_per_game"] ].copy()
        team_performance["shots_per90_difference"]= team_performance["shots_per90"]-team_performance["shots_per90_against"]
        team_performance["goals_per90_difference"]= team_performance["goals_per90"]-team_performance["goals_per90_against"]
        team_performance["sot_per90_difference"]= team_performance["shots_on_target_per90"]-team_performance["shots_on_target_per90_against"]

        #Goal difference
        min_goal_difference, min_goal_difference_team = get_team_with_the_most_or_least("goals_per90_difference",0,team_performance)
        #shot difference
        min_shot_difference, min_shot_difference_team = get_team_with_the_most_or_least("shots_per90_difference",0,team_performance)
        #sot difference
        min_sot_difference, min_sot_difference_team = get_team_with_the_most_or_least("sot_per90_difference",0,team_performance)
        #points_per_game
        max_points_per_game, max_points_per_game_team = get_team_with_the_most_or_least("points_per_game",0,team_performance)

        #teams offensive vs defensive performance comparison metrics
        tp1,tp2=st.columns(2)
        with tp1:
            st.metric("Least Goal difference per 90", min_goal_difference_team,
            delta= f"Difference: {min_goal_difference:.2f}", delta_color="blue", delta_arrow="off",
            border=True, icon=":material/contrast_circle:")

            st.metric("Least Shot on target difference per 90", min_sot_difference_team,
            delta= f"SoT Difference: {min_sot_difference:.2f}", delta_color="blue", delta_arrow="off",
            border=True, icon=":material/contrast_circle:")

        with tp2:
            st.metric("Least Shot difference per 90", min_shot_difference_team,
            delta= f"Difference: {min_shot_difference:.2f}", delta_color="blue", delta_arrow="off",
            border=True, icon=":material/contrast_circle:")

            st.metric("Most points per game", max_points_per_game_team,
            delta= f"Points: {max_points_per_game:.2f}", delta_color="blue", delta_arrow="off",
            border=True, icon=":material/add:")

        #teams Shot Difference vs Goal Difference scatter chart
        with st.container(border=True):
            st.subheader("Shot Difference vs Goal Difference")
            st.scatter_chart(
                team_performance,
                x="shots_per90_difference",
                y="goals_per90_difference",
                color="team",
                x_label="Shot Differential per 90",
                y_label="Goal Difference per 90",
                size=100
            )

        #teams Goals vs Goals Against bar chart
        with st.container(border=True):            
            st.subheader("Goals scored and conceded")
            st.bar_chart(team_performance,
            x="team",
            y=["goals_per90", "goals_per90_against"],
            x_label="Team",
            y_label="GF and GA",
            stack=False)

        #teams Shot difference bar chart
        team_performance["shots_per90_against"]=-team_performance["shots_per90_against"]
        with st.container(border=True):            
            st.subheader("Shot Difference: Shots per 90 and Shots Conceded per 90")
            st.bar_chart(team_performance,
            x="team",
            y=["shots_per90", "shots_per90_against"],
            x_label="Team",
            y_label="Shots per 90")

#-----------------------------------------------discipline------------------------------
    with tab5:
        st.header(":material/sports: Team Discipline")
        #df for team discipline
        team_discipline=filtered_team[ ["team","minutes","cards_yellow","cards_red","fouls","fouled","offsides","pens_att_against"] ].copy()

        #most yellow cards
        max_ycards, max_ycards_team = get_team_with_the_most_or_least("cards_yellow", 0, team_discipline)
        #most red cards
        max_rcards, max_rcards_team = get_team_with_the_most_or_least("cards_red", 0, team_discipline)
        #most fouls
        max_fouls, max_fouls_team = get_team_with_the_most_or_least("fouls", 0, team_discipline)
        #least fouls
        min_fouls, min_fouls_team = get_team_with_the_most_or_least("fouls", 1, team_discipline)
        #least offsides
        min_offsides, min_offsides_team = get_team_with_the_most_or_least("offsides", 1, team_discipline)
        #Most penalties
        max_pens, max_pens_team = get_team_with_the_most_or_least("pens_att_against", 0, team_discipline)

        #teams discipline comparison
        dis1, dis2=st.columns(2)
        with dis1:
            st.metric("Most yellow cards", max_ycards_team,
            delta= f"Cards: {max_ycards:.0f}", delta_color="blue", delta_arrow="off",
            border=True, icon=":material/crop_2_3:")

            st.metric("Fewer fouls", min_fouls_team,
            delta= f"Fouls: {min_fouls:.0f}", delta_color="blue", delta_arrow="off",
            border=True, icon=":material/sports:")

            st.metric("Least Offsides", min_offsides_team,
            delta= f"Offsides: {min_offsides:.0f}", delta_color="blue", delta_arrow="off",
            border=True, icon=":material/flag_2:")

        with dis2:
            st.metric("Most red cards", max_rcards_team,
            delta= f"Cards: {max_rcards:.0f}", delta_color="blue", delta_arrow="off",
            border=True, icon=":material/crop_2_3:")

            st.metric("Most fouls", max_fouls_team,
            delta= f"Fouls: {max_fouls:.0f}", delta_color="blue", delta_arrow="off",
            border=True, icon=":material/sports:")

            st.metric("Most Penalaties Conceded", max_pens_team,
            delta= f"Penalaties Conceded: {max_pens:.0f}", delta_color="blue", delta_arrow="off",
            border=True, icon=":material/flag_2:")

        #teams Fouls vs Fouled scatter chart
        with st.container(border=True):
            st.subheader("Fouls vs Fouled")
            st.scatter_chart(team_discipline,
            x="fouled",
            y="fouls",
            x_label="Fouled",
            y_label="Fouls",
            color="team")

        #teams Fouls vs Yellow Cards scatter chart
        with st.container(border=True):
            st.subheader("Fouls vs Yellow Cards")
            st.scatter_chart(team_discipline,
            x="fouls",
            y="cards_yellow",
            x_label="Fouls",
            y_label="Yellow Cards",
            color="team",
            size="minutes")

        #teams red cards, yellow cards bar chart
        with st.container(border=True):
            st.subheader("Red Cards and Yellow Cards")
            st.bar_chart(team_discipline,
            x="team",
            y=["cards_red","cards_yellow"],
            x_label="Team",
            y_label="Cards",
            color=["red", "yellow"])
