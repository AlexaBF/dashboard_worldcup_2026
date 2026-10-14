import streamlit as st
import pandas as pd

st.title(":material/groups_3: TEAMS") 

@st.cache_data
def load_data():
    df=pd.read_csv("datasets/teams.csv")
    return df

df=load_data()

#------------------------------------basic info-----------------------------------
#most goals scored
max_gf=df["goals"].max() 
max_gf_teams=df.loc[ df["goals"] == max_gf, "team" ].tolist() 
max_gf_team = ", ".join(max_gf_teams)

#most goals conceded
max_ga=df["goals_against"].max() 
max_ga_teams=df.loc[ df["goals_against"] == max_ga, "team" ].tolist() 
max_ga_team = ", ".join(max_ga_teams)


##least goals scored
min_gf=df["goals"].min()
min_gf_teams=df.loc[ df["goals"] == min_gf, "team" ].tolist() 
min_gf_team = ", ".join(min_gf_teams)

#least goals conceded
min_ga=df["goals_against"].min() 
min_ga_teams=df.loc[ df["goals_against"] == min_ga, "team" ].tolist() 
min_ga_team = ", ".join(min_ga_teams)

col1, col2=st.columns(2)
with col1:
    st.metric("Most goals scored", 
    max_gf_team,
    delta= f"Goals: {max_gf:.0f}",
    border=True, 
    icon=":material/sentiment_excited:", delta_color="blue", delta_arrow="off")

    st.metric("Least goals scored", 
    min_gf_team,
    delta= f"Goals: {min_gf:.0f}",
    border=True, 
    icon=":material/sentiment_stressed:", delta_color="blue", delta_arrow="off")

with col2:
    st.metric("Most goals conceded", 
    max_ga_team,
    delta= f"Goals: {max_ga:.0f}",
    border=True, 
    icon=":material/sentiment_neutral:", delta_color="blue", delta_arrow="off")

    st.metric("Least goals conceded", 
    min_ga_team,
    delta= f"Goals: {min_ga:.0f}",
    border=True, 
    icon=":material/sentiment_content:", delta_color="blue", delta_arrow="off")
#---------------------------------------------------------------------------------
tab1,tab2= st.tabs([":material/groups_2: Multi-Team Stats", ":material/group_search: Team Profile"])


#------------------------------------------team profile-------------------------------------

with tab2: 
    with st.container(border=True):
        st.header(":material/group_search: Team Profile")

        team_profile = st.selectbox(":material/filter_alt: Select a team",sorted(df["team"].unique()))
        filtered_team_profile = df[df["team"] == team_profile]
        
        df_team_selected=filtered_team_profile.copy()
        team_metric = df_team_selected.iloc[0]

        #team profile metric
        tp1,tp2,tp3=st.columns(3)

        #group stage, round of 32 round of 16, Quarter finals, semi finals, third place match, final

        with tp1:
            st.metric("Age Average", team_metric["avg_age"],border=True,
            icon=":material/date_range:")
            st.metric("Goals", team_metric["goals"], border=True,
            icon=":material/sports_and_outdoors:")
            st.metric("Possession", f"{team_metric["possession"]:.2f} %", border=True,
            icon=":material/percent:")
            st.metric("Fouls", team_metric["fouls"], border=True,
            icon=":material/sports:")
        with tp2:
            st.metric("Number of Players", team_metric["players_used"], border=True,
            icon=":material/groups_2:")
            st.metric("Goals Conceded", team_metric["goals_against"], border=True,
            icon=":material/sports_soccer:")
            st.metric("Shots", team_metric["shots"], border=True,
            icon=":material/shoe_cleats:")
            st.metric("Yellow Cards", team_metric["cards_yellow"],border=True,
            icon=":material/crop_2_3:")

        with tp3:
            st.metric("Games played", team_metric["games"], border=True,
            icon=":material/scoreboard:")
            st.metric("Own Goals", team_metric["own_goals"], border=True,
            icon=":material/sports_soccer:")
            st.metric("Shot Accuracy", f"{team_metric["shots_on_target_pct"]:.2f} %", border=True,
            icon=":material/percent:")
            st.metric("Red Cards", team_metric["cards_red"],border=True,
            icon=":material/crop_2_3:")

    c1,c2=st.columns(2)
    with c1:
        with st.container(border=True):
            st.subheader("Goals Comparison")

            st.bar_chart(
                df_team_selected,
                x="team",
                y=["goals","goals_against"],
                stack=False,
                color=["orange","blue"]
                )
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
        with st.container(border=True):
            st.subheader("Shooting Statistics")
            st.bar_chart(
                df_team_selected,
                x="team",
                y=["shots","shots_on_target"],
                stack=False
                )

        with st.container(border=True):
            st.subheader("Defensive")

            st.bar_chart(
                df_team_selected,
                x="team",
                y=["fouls","tackles_won"],
                stack=False
            )
#-------------------------------------Teams-------------
with tab1:
    with st.container(border=True):
        st.header(":material/groups_2: Multi-Team Stats")

        teams_selected = st.multiselect(":material/filter_alt: Select Teams", df["team"].unique(), default=df["team"].unique())
        filtered_team=df[ df["team"].isin(teams_selected) ]


        tab1,tab2,tab3,tab4,tab5 = st.tabs([":material/shoe_cleats: Offensive",":material/shield: Defensive", ":material/percent: Possesion", ":material/balance: Offensive vs Defensive",":material/sports: Discipline"])


    #---------------------------------------
    #----------------------------------------------------offensive performance--------------------------------------
    with tab1:
        st.header(":material/shoe_cleats: Offensive performance")

        #best scoring team
        best_scoring=filtered_team["goals_per90"].max() 
        best_scoring_teams=filtered_team.loc[ filtered_team["goals_per90"] == best_scoring, "team" ].tolist() 
        best_scoring_team = ", ".join(best_scoring_teams)

        #Most Attacking Volume
        most_attack=filtered_team["shots_per90"].max() 
        most_attack_teams=filtered_team.loc[ filtered_team["shots_per90"] == most_attack, "team" ].tolist() 
        most_attack_team = ", ".join(most_attack_teams)

        #best finishing
        best_finish=filtered_team["goals_per_shot_on_target"].max() 
        best_finish_teams=filtered_team.loc[ filtered_team["goals_per_shot_on_target"] == best_finish, "team" ].tolist() 
        best_finish_team = ", ".join(best_finish_teams)


        #Most shots on target
        most_sot = filtered_team["shots_on_target_per90"].max()
        most_sot_teams = filtered_team.loc[filtered_team["shots_on_target_per90"] == most_sot, "team" ].tolist()
        most_sot_team = ", ".join(most_sot_teams)

        #best  assist
        most_assist = filtered_team["assists_per90"].max()
        most_assist_teams = filtered_team.loc[filtered_team["assists_per90"] == most_assist, "team" ].tolist()
        most_assist_team = ", ".join(most_assist_teams)

        # Shot accuracy
        most_shot_accuracy = filtered_team["shots_on_target_pct"].max()
        most_shot_accuracy_teams = filtered_team.loc[filtered_team["shots_on_target_pct"] == most_shot_accuracy, "team" ].tolist()
        most_shot_accuracy_team = ", ".join(most_shot_accuracy_teams)

        # Goals per shot
        most_goal_sper_shot = filtered_team["goals_per_shot"].max()
        goals_per_shot_teams = filtered_team.loc[filtered_team["goals_per_shot"] == most_goal_sper_shot, "team" ].tolist()
        goals_per_shot_team = ", ".join(goals_per_shot_teams)
        # Possession 
        most_possession = filtered_team["possession"].max()
        most_possession_teams = filtered_team.loc[filtered_team["possession"] == most_possession, "team" ].tolist()
        most_possession_team = ", ".join(most_possession_teams)

        o1, o2=st.columns(2)
        with o1:
            st.metric("Best Scoring Team", 
            best_scoring_team,
            delta= f"Goals per 90: {best_scoring:.1f}",
            border=True,
            delta_color="blue", delta_arrow="off",
            icon=":material/sports_soccer:")

            st.metric("Best Shot Conversion", 
            best_finish_team,
            delta= f"SoT scored: {best_finish:.1%}",
            border=True,
            delta_color="blue", delta_arrow="off",
            icon=":material/target:")

            st.metric("Most Assists per 90", 
            most_assist_team,
            delta= f"Assists: {most_assist:.2f}",
            border=True,
            delta_color="blue", delta_arrow="off",
            icon=":material/partner_exchange:")

            st.metric("Most Goals per shot", 
            goals_per_shot_team,
            delta= f"Goals: {most_goal_sper_shot:.2f}",
            border=True,
            delta_color="blue", delta_arrow="off",
            icon=":material/sports_and_outdoors:")
        
        with o2:
            st.metric("Most Shots per 90", 
            most_attack_team,
            delta= f"Shots per 90: {most_attack:.1f}",
            border=True, 
            delta_color="blue", delta_arrow="off",
            icon=":material/shoe_cleats:")

            st.metric("Most shots on target", 
            most_sot_team,
            delta= f"SoT per 90: {most_sot:.1f}",
            border=True, 
            delta_color="blue", delta_arrow="off",
            icon=":material/target:")

            st.metric("Best shot accuracy", 
            most_shot_accuracy_team,
            delta= f"Accuracy: {most_shot_accuracy:.2f}%",
            border=True, 
            delta_color="blue", delta_arrow="off",
            icon=":material/percent:")
            
            st.metric("Possesion", 
            most_possession_team,
            delta= f"Possesion: {most_possession:.2f}%",
            border=True, 
            delta_color="blue", delta_arrow="off",
            icon=":material/percent:")
    
        teams_offensive=filtered_team[ ["team","minutes", "goals_per90", "shots_on_target_pct","goals_per_shot_on_target","shots_per90","shots_on_target_per90"] ].copy()

        #Shots per 90 vs Goals per 90
        with st.container(border=True):
            st.subheader("Shots per 90 vs Goals per 90")
            st.scatter_chart(teams_offensive,
                x="shots_per90",
                y="goals_per90",
                x_label="Shots per 90",
                y_label="Goals per 90",
                color="team",
                size="minutes")

        #shot accuracy
        with st.container(border=True):
            st.subheader("Shot per 90 vs SoT per 90")
            st.scatter_chart(teams_offensive,
                x="shots_per90",
                y="shots_on_target_per90",
                x_label="Shots per 90",
                y_label="Shots on Target per 90",
                color="team",
                size="minutes")
        
        #shot accuracy 
        with st.container(border=True):
            st.subheader("Shot Accuracy (%) Ranking")
            st.bar_chart(teams_offensive,
            x="team",
            y="shots_on_target_pct",
            x_label="Team",
            y_label="shots on target %",
            sort="-shots_on_target_pct")

        #goals pershot on target
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

        teams_defensive=filtered_team[ ["team","minutes", "goals_per90_against", "shots_per90_against","goals_per_shot_against","shots_on_target_per90_against","gk_save_pct","gk_clean_sheets_pct", "interceptions","tackles_won"] ].copy()

        #best defense
        best_defense=teams_defensive["goals_per90_against"].min() 
        best_defense_teams=teams_defensive.loc[ teams_defensive["goals_per90_against"] == best_defense, "team" ].tolist() 
        best_defense_team = ", ".join(best_defense_teams)

        #best shot blocking
        shot_block=teams_defensive["shots_per90_against"].min() 
        shot_block_teams=teams_defensive.loc[ teams_defensive["shots_per90_against"] == shot_block, "team" ].tolist() 
        shot_block_team = ", ".join(shot_block_teams)

        #best defensive efficiency
        defense_efficiency = teams_defensive["goals_per_shot_against"].min()
        defense_efficiency_teams = teams_defensive.loc[teams_defensive["goals_per_shot_against"] == defense_efficiency, "team" ].tolist()
        defense_efficiency_team = ", ".join(defense_efficiency_teams)

        #best SOT blocking
        sot_block=teams_defensive["shots_on_target_per90_against"].min() 
        sot_block_teams=teams_defensive.loc[ teams_defensive["shots_on_target_per90_against"] == sot_block, "team" ].tolist() 
        sot_block_team = ", ".join(sot_block_teams)
        
        #most saves   
        most_saves=teams_defensive["gk_save_pct"].max() 
        most_saves_teams=teams_defensive.loc[ teams_defensive["gk_save_pct"] == most_saves, "team" ].tolist() 
        most_saves_team = ", ".join(most_saves_teams)

        #clean sheets 
        most_clean=teams_defensive["gk_clean_sheets_pct"].max() 
        most_clean_teams=teams_defensive.loc[ teams_defensive["gk_clean_sheets_pct"] == most_clean, "team" ].tolist() 
        most_clean_team = ", ".join(most_clean_teams)

        # Interceptions
        most_interceptions=teams_defensive["interceptions"].max() 
        most_interceptions_teams=teams_defensive.loc[ teams_defensive["interceptions"] == most_interceptions, "team" ].tolist() 
        most_interceptions_team = ", ".join(most_interceptions_teams)

        # Tackles won
        most_tackles_won=teams_defensive["tackles_won"].max() 
        most_tackles_won_teams=teams_defensive.loc[ teams_defensive["tackles_won"] == most_tackles_won, "team" ].tolist() 
        most_tackles_won_team = ", ".join(most_tackles_won_teams)


        d1, d2=st.columns(2)
        with d1:
            st.metric("Best Defense", 
            best_defense_team,
            delta= f"Goals conceded per 90: {best_defense:.2f}",
            border=True,
            delta_color="blue", delta_arrow="off",
            icon=":material/shield_person:")

            st.metric("Best Shot Blocking", 
            shot_block_team,
            delta= f"Shots conceded per 90: {shot_block:.2f}",
            border=True,
            delta_color="blue", delta_arrow="off",
            icon=":material/guardian:")

            st.metric("Most Saves by Gk", 
            most_saves_team,
            delta= f"Saves: {most_saves:.2f}%",
            border=True,
            delta_color="blue", delta_arrow="off",
            icon=":material/percent:")

            st.metric("Most Interceptions", 
            most_interceptions_team,
            delta=f"Interceptions: {most_interceptions:.0f}",
            border=True,
            delta_color="blue", delta_arrow="off",
            icon=":material/cheer:")

        
        with d2:
            st.metric("Best Defensive Efficiency", 
            defense_efficiency_team,
            delta= f"Goals per shots conceded: {defense_efficiency:.2f}",
            border=True, 
            delta_color="blue", delta_arrow="off",
            icon=":material/speed_2:")

            st.metric("Best SOT Blocking", 
            sot_block_team,
            delta= f"SoT conceded per 90: {sot_block:.2f}",
            border=True, 
            delta_color="blue", delta_arrow="off",
            icon=":material/crisis_alert:")

            st.metric("Most Clean Sheets", 
            most_clean_team,
            delta= f"Clean Sheets: {most_clean:.2f}%",
            border=True, 
            delta_color="blue", delta_arrow="off",
            icon=":material/percent:")

            st.metric("Most Tackles Won", 
            most_tackles_won_team,
            delta= f"Tackles: {most_tackles_won:.0f}",
            border=True, 
            delta_color="blue", delta_arrow="off",
            icon=":material/cheer:")
            

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
        

    # ------------------------------------------possession--------------------------------------------------------
    with tab3:
        st.header(":material/percent: Team possesion")

        teams_possession=filtered_team[ ["team","minutes","possession","goals_per90","shots_per90","assists_per90","shots_on_target_per90"] ].copy()

        #Crosses?
        #Offsides??
        
        # goals_per90
        goals_90=teams_possession["goals_per90"].max() 
        goals_90_teams=teams_possession.loc[ teams_possession["goals_per90"] == goals_90, "team" ].tolist() 
        goals_90_team = ", ".join(goals_90_teams)

        # shots_per90
        shots_90=teams_possession["shots_per90"].max() 
        shots_90_teams=teams_possession.loc[ teams_possession["shots_per90"] == shots_90, "team" ].tolist() 
        shots_90_team = ", ".join(shots_90_teams)

        # assists_per90
        assists_90=teams_possession["assists_per90"].max() 
        assists_90_teams=teams_possession.loc[ teams_possession["assists_per90"] == assists_90, "team" ].tolist() 
        assists_90_team = ", ".join(assists_90_teams)

        # shots_on_target_per90
        sot_90=teams_possession["shots_on_target_per90"].max() 
        sot_90_teams=teams_possession.loc[ teams_possession["shots_on_target_per90"] == sot_90, "team" ].tolist() 
        sot_90_team = ", ".join(sot_90_teams)

        #Higest possession
        high_possession=teams_possession["possession"].max() 
        high_possession_teams=teams_possession.loc[ teams_possession["possession"] == high_possession, "team" ].tolist() 
        high_possession_team = ", ".join(high_possession_teams)

        p1, p2=st.columns(2)
        with p1:
            st.metric("Higest possession", 
            high_possession_team,
            delta= f"Possession: {high_possession:.2f} %",
            border=True,
            delta_color="blue", delta_arrow="off",
            icon=":material/percent:")

            st.metric("Goals per 90", 
            goals_90_team,
            delta= f"Goals: {goals_90:.2f}",
            border=True,
            delta_color="blue", delta_arrow="off",
            icon=":material/sports_and_outdoors:")

            st.metric("Shots on target per 90", 
            sot_90_team,
            delta= f"SoT: {sot_90:.2f}",
            border=True,
            delta_color="blue", delta_arrow="off",
            icon=":material/target:")

            
        with p2:
            st.metric("Most Assists per 90", 
            assists_90_team,
            delta= f"Assists: {assists_90:.2f}",
            border=True,
            delta_color="blue", delta_arrow="off",
            icon=":material/cheer:")

            st.metric("Shots per 90", 
            shots_90_team,
            delta= f"Shots: {shots_90:.2f}",
            border=True,
            delta_color="blue", delta_arrow="off",
            icon=":material/shoe_cleats:")
        
        with st.container(border=True):
            st.subheader("Possession vs Goals per90")
            st.scatter_chart(
                teams_possession,
                x="possession",
                y="goals_per90",
                x_label="Possession %",
                y_label="Goals per 90",
                color="team",
                size="minutes")

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

        #team possesion
        with st.container(border=True):
            st.subheader("Team possesion")
            st.bar_chart(teams_possession,
            x="team",
            y="possession",
            x_label="Team",
            y_label="Possesion %",
            sort="-possession")


    #-------------------------------------offensive vs defensive performance---------
    with tab4:
        st.header(":material/balance: Offensive vs Defensive Performance")

        team_performance = df[ ["team", "goals_per90", "goals_per90_against", "shots_per90","shots_per90_against","shots_on_target_per90","shots_on_target_per90_against","points_per_game"] ].copy()
        team_performance["shots_per90_difference"]= team_performance["shots_per90"]-team_performance["shots_per90_against"]
        team_performance["goals_per90_difference"]= team_performance["goals_per90"]-team_performance["goals_per90_against"]
        team_performance["sot_per90_difference"]= team_performance["shots_on_target_per90"]-team_performance["shots_on_target_per90_against"]
        
        #Goal difference
        min_goal_difference=team_performance["goals_per90_difference"].max()
        min_goal_difference_teams=team_performance.loc[ team_performance["goals_per90_difference"] == min_goal_difference, "team" ].tolist() 
        min_goal_difference_team = ", ".join(min_goal_difference_teams)

        #shot difference
        min_shot_difference=team_performance["shots_per90_difference"].max()
        min_shot_difference_teams=team_performance.loc[ team_performance["shots_per90_difference"] == min_shot_difference, "team" ].tolist() 
        min_shot_difference_team = ", ".join(min_shot_difference_teams)

        #sot difference
        min_sot_difference=team_performance["sot_per90_difference"].max()
        min_sot_difference_teams=team_performance.loc[ team_performance["sot_per90_difference"] == min_sot_difference, "team" ].tolist() 
        min_sot_difference_team = ", ".join(min_sot_difference_teams)

        #points_per_game
        max_points_per_game=team_performance["points_per_game"].max()
        max_points_per_game_teams=team_performance.loc[ team_performance["points_per_game"] == max_points_per_game, "team" ].tolist() 
        max_points_per_game_team = ", ".join(max_points_per_game_teams)
        

        tp1,tp2=st.columns(2)
        with tp1:
            st.metric("Least Goal difference per 90", 
            min_goal_difference_team,
            delta= f"Difference: {min_goal_difference:.2f}",
            border=True,
            delta_color="blue", delta_arrow="off",
            icon=":material/contrast_circle:")

            st.metric("Least Shot on target difference per 90", 
            min_sot_difference_team,
            delta= f"SoT Difference: {min_sot_difference:.2f}",
            border=True,
            delta_color="blue", delta_arrow="off",
            icon=":material/contrast_circle:")

        with tp2:
            st.metric("Least Shot difference per 90", 
            min_shot_difference_team,
            delta= f"Difference: {min_shot_difference:.2f}",
            border=True,
            delta_color="blue", delta_arrow="off",
            icon=":material/contrast_circle:")

            st.metric("Most points per game", 
            max_points_per_game_team,
            delta= f"Points: {max_points_per_game:.2f}",
            border=True,
            delta_color="blue", delta_arrow="off",
            icon=":material/add:")



        #Shot Difference vs Goal Difference
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

        #Goals vs Goals Against
        with st.container(border=True):            
            st.subheader("Goals scored and conceded")
            st.bar_chart(team_performance,
            x="team",
            y=["goals_per90", "goals_per90_against"],
            x_label="Team",
            y_label="GF and GA",
            stack=False)


        #Shot difference
        team_performance["shots_per90_against"]=-team_performance["shots_per90_against"]
        with st.container(border=True):            
            st.subheader("Shot Difference: Shots per 90 and Shots Conceded per 90")
            st.bar_chart(team_performance,
            x="team",
            y=["shots_per90", "shots_per90_against"],
            x_label="Team",
            y_label="Shots per 90")

    #-----------------------------------------------------------------------------------------------
    #-----------------------------------------------discipline------------------------------
    with tab5:
        st.header(":material/sports: Team Discipline")

        team_discipline=filtered_team[ ["team","minutes","cards_yellow","cards_red","fouls","fouled","offsides","pens_att_against"] ].copy()

        #mosrt yellow cards
        max_ycards=team_discipline["cards_yellow"].max() 
        max_ycards_teams=team_discipline.loc[ team_discipline["cards_yellow"] == max_ycards, "team" ].tolist() 
        max_ycards_team = ", ".join(max_ycards_teams)

        #most red cards
        max_rcards=team_discipline["cards_red"].max() 
        max_rcards_teams=team_discipline.loc[ team_discipline["cards_red"] == max_rcards, "team" ].tolist() 
        max_rcards_team = ", ".join(max_rcards_teams)

        #most fouls
        max_fouls=team_discipline["fouls"].max() 
        max_fouls_teams=team_discipline.loc[ team_discipline["fouls"] == max_fouls, "team" ].tolist() 
        max_fouls_team = ", ".join(max_fouls_teams)

        #least fouls
        min_fouls=team_discipline["fouls"].min()
        min_fouls_teams=team_discipline.loc[ team_discipline["fouls"] == min_fouls, "team" ].tolist() 
        min_fouls_team = ", ".join(min_fouls_teams)

        #least offsides
        min_offsides=team_discipline["offsides"].min()
        min_offsides_teams=team_discipline.loc[ team_discipline["offsides"] == min_offsides, "team" ].tolist() 
        min_offsides_team = ", ".join(min_offsides_teams)

        #Most penalties
        max_pens=team_discipline["pens_att_against"].max()
        max_pens_teams=team_discipline.loc[ team_discipline["pens_att_against"] == max_pens, "team" ].tolist() 
        max_pens_team = ", ".join(max_pens_teams)


        dis1, dis2=st.columns(2)
        with dis1:
            st.metric("Most yellow cards", 
            max_ycards_team,
            delta= f"Cards: {max_ycards:.0f}",
            border=True, 
            icon=":material/crop_2_3:", 
            delta_color="blue", delta_arrow="off")

            st.metric("Fewer fouls", 
            min_fouls_team,
            delta= f"Fouls: {min_fouls:.0f}",
            border=True, 
            icon=":material/sports:",
            delta_color="blue", delta_arrow="off")

            st.metric("Least Offsides", 
            min_offsides_team,
            delta= f"Offsides: {min_offsides:.0f}",
            border=True, 
            icon=":material/flag_2:",
            delta_color="blue", delta_arrow="off")

        with dis2:
            st.metric("Most red cards", 
            max_rcards_team,
            delta= f"Cards: {max_rcards:.0f}",
            border=True, 
            icon=":material/crop_2_3:",
            delta_color="blue", delta_arrow="off")

            st.metric("Most fouls", 
            max_fouls_team,
            delta= f"Fouls: {max_fouls:.0f}",
            border=True, 
            icon=":material/sports:",
            delta_color="blue", delta_arrow="off")

            st.metric("Most Penalaties Conceded", 
            max_pens_team,
            delta= f"Penalaties Conceded: {max_pens:.0f}",
            border=True, 
            icon=":material/flag_2:",
            delta_color="blue", delta_arrow="off")
            
        with st.container(border=True):
            st.subheader("Fouls vs Fouled")
            st.scatter_chart(team_discipline,
            x="fouled",
            y="fouls",
            x_label="Fouled",
            y_label="Fouls",
            color="team")

        with st.container(border=True):
            st.subheader("Fouls vs Yellow Cards")
            st.scatter_chart(team_discipline,
            x="fouls",
            y="cards_yellow",
            x_label="Fouls",
            y_label="Yellow Cards",
            color="team",
            size="minutes")

        #red cards, yellow cards
        with st.container(border=True):
            st.subheader("Red Cards and Yellow Cards")
            st.bar_chart(team_discipline,
            x="team",
            y=["cards_red","cards_yellow"],
            x_label="Team",
            y_label="Cards",
            color=["red", "yellow"])

