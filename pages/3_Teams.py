import streamlit as st
import pandas as pd

st.title(":material/display_group: TEAMS") 

@st.cache_data
def load_data():
    df=pd.read_csv("datasets/teams.csv")
    return df

df=load_data()
st.dataframe(df)

#Team Analysis?
# Team ranking????

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
    delta= f"{max_gf:.0f} goals",
    border=True, 
    icon=":material/sentiment_excited:", delta_color="blue", delta_arrow="off")

    st.metric("Least goals scored", 
    min_gf_team,
    delta= f"{min_gf:.0f} goals",
    border=True, 
    icon=":material/sentiment_stressed:", delta_color="blue", delta_arrow="off")

with col2:
    st.metric("Most goals conceded", 
    max_ga_team,
    delta= f"{max_ga:.0f} goals",
    border=True, 
    icon=":material/sentiment_neutral:", delta_color="blue", delta_arrow="off")

    st.metric("Least goals conceded", 
    min_ga_team,
    delta= f"{min_ga:.0f} goals",
    border=True, 
    icon=":material/sentiment_content:", delta_color="blue", delta_arrow="off")

#------------------------------------------team profile-------------------------------------
st.divider()
st.header(":material/group_search: Team Profile")

team_profile = st.selectbox("Select a team",sorted(df["team"].unique()))
filtered_team_profile = df[df["team"] == team_profile]
#st.dataframe(filtered_team_profile)

#team profile metric
tp1,tp2,tp3=st.columns(3)

#group stage, round of 32 round of 16, Quarter finals, semi finals, third place match, final

with tp1:
    st.metric("Age Average", filtered_team_profile.iloc[0]['avg_age'], border=True)
    st.metric("Goals", filtered_team_profile.iloc[0]['goals'], border=True)
    st.metric("Possession", f"{filtered_team_profile.iloc[0]['possession']} %", border=True)
    st.metric("Fouls", filtered_team_profile.iloc[0]['fouls'], border=True)
with tp2:
    st.metric("Number of Players", filtered_team_profile.iloc[0]['players_used'], border=True)
    st.metric("Goals Conceded", filtered_team_profile.iloc[0]['goals_against'], border=True)
    st.metric("Shots", filtered_team_profile.iloc[0]['shots'], border=True)
    st.metric("Yellow Cards", filtered_team_profile.iloc[0]['cards_yellow'],border=True)

with tp3:
    st.metric("Games played", filtered_team_profile.iloc[0]['games'], border=True)
    st.metric("Own Goals", filtered_team_profile.iloc[0]['own_goals'], border=True)
    st.metric("Shot Accuracy", f"{filtered_team_profile.iloc[0]['shots_on_target_pct']} %", border=True)
    st.metric("Red Cards", filtered_team_profile.iloc[0]['cards_red'],border=True)
    



#-------------------------------------Teams-------------
st.divider()
st.header("Team Stats")

teams_selected = st.multiselect("Select Teams", df["team"].unique(), default=df["team"].unique())
filtered_team=df[ df["team"].isin(teams_selected) ]


tab1,tab2,tab3,tab4,tab5 = st.tabs(["Offensive", "Defensive", "Possesion", "Offensive vs Defensive","Discipline"])


#---------------------------------------
#----------------------------------------------------offensive performance--------------------------------------
with tab1:
    st.header(":material/arrow_forward: Offensive performance")

    #best scoring team
    best_scoring=df["goals_per90"].max() 
    best_scoring_teams=df.loc[ df["goals_per90"] == best_scoring, "team" ].tolist() 
    best_scoring_team = ", ".join(best_scoring_teams)

    #Most Attacking Volume
    most_attack=df["shots_per90"].max() 
    most_attack_teams=df.loc[ df["shots_per90"] == most_attack, "team" ].tolist() 
    most_attack_team = ", ".join(most_attack_teams)

    #best finishing
    best_finish=df["goals_per_shot_on_target"].max() 
    best_finish_teams=df.loc[ df["goals_per_shot_on_target"] == best_finish, "team" ].tolist() 
    best_finish_team = ", ".join(best_finish_teams)


    #Most shots on target
    most_sot = df["shots_on_target_per90"].max()
    most_sot_teams = df.loc[df["shots_on_target_per90"] == most_sot, "team" ].tolist()
    most_sot_team = ", ".join(most_sot_teams)

    o1, o2=st.columns(2)
    with o1:
        st.metric("Best Scoring Team", 
        best_scoring_team,
        delta= f"{best_scoring:.1f} goals per 90",
        border=True,
        delta_color="blue", delta_arrow="off")

        st.metric("Best Shot Conversion", 
        best_finish_team,
        delta= f"{best_finish:.1%} of shots on target scored",
        border=True,
        delta_color="blue", delta_arrow="off")
    
    with o2:
        st.metric("Most Shots per 90", 
        most_attack_team,
        delta= f"{most_attack:.1f} shots per 90",
        border=True, 
        delta_color="blue", delta_arrow="off")

        st.metric("Most shots on target", 
        most_sot_team,
        delta= f"{most_sot:.1f} shots on target per 90",
        border=True, 
        delta_color="blue", delta_arrow="off")
   

    #goals per 90 ranking
    with st.container(border=True):
        g90_teams=filtered_team[ ["team", "goals_per90"] ].copy()  
        st.subheader("Goals per 90")
        st.bar_chart(g90_teams,
        x="team",
        y="goals_per90",
        x_label="Team",
        y_label="goals per90",
        sort="-goals_per90")

    #shot accuracy 
    with st.container(border=True):
        sot_team=filtered_team[ ["team", "shots_on_target_pct"] ].copy() 
        st.subheader("Shot Accuracy (%)")
        st.bar_chart(sot_team,
        x="team",
        y="shots_on_target_pct",
        x_label="Team",
        y_label="shots on target %",
        sort="-shots_on_target_pct")

    #goals pershot on target
    with st.container(border=True):
        gpsot_team=filtered_team[ ["team", "goals_per_shot_on_target"] ].copy() 
        st.subheader("goals pershot on target")
        st.bar_chart(gpsot_team,
        x="team",
        y="goals_per_shot_on_target",
        x_label="Team",
        y_label="goals per shot",
        sort="-goals_per_shot_on_target")

    #Shots per 90
    with st.container(border=True):
        s90_team=filtered_team[ ["team", "shots_per90"] ].copy() 
        st.subheader("Shots per 90")
        st.bar_chart(s90_team,
        x="team",
        y="shots_per90",
        x_label="Team",
        y_label="Shots",
        sort="-shots_per90")


#-----------------------------------------------defensive-------------------------------------------------
with tab2:
    st.header(":material/arrow_back: Defensive performance")

    #best defense
    best_defense=df["goals_per90_against"].min() 
    best_defense_teams=df.loc[ df["goals_per90_against"] == best_defense, "team" ].tolist() 
    best_defense_team = ", ".join(best_defense_teams)

    #best shot blocking
    shot_block=df["shots_per90_against"].min() 
    shot_block_teams=df.loc[ df["shots_per90_against"] == shot_block, "team" ].tolist() 
    shot_block_team = ", ".join(shot_block_teams)

    #best defensive efficiency
    defense_efficiency = df["goals_per_shot_against"].min()
    defense_efficiency_teams = df.loc[df["goals_per_shot_against"] == defense_efficiency, "team" ].tolist()
    defense_efficiency_team = ", ".join(defense_efficiency_teams)

    #best SOT blocking
    sot_block=df["shots_on_target_per90_against"].min() 
    sot_block_teams=df.loc[ df["shots_on_target_per90_against"] == sot_block, "team" ].tolist() 
    sot_block_team = ", ".join(sot_block_teams)


    d1, d2=st.columns(2)
    with d1:
        st.metric("Best Defense", 
        best_defense_team,
        delta= f"{best_defense:.1f} goals conceded per 90",
        border=True,
        delta_color="blue", delta_arrow="off")

        st.metric("Best Shot Blocking", 
        shot_block_team,
        delta= f"{shot_block:.1f} shots conceded per 90",
        border=True,
        delta_color="blue", delta_arrow="off")
    
    with d2:
        st.metric("Best Defensive Efficiency", 
        defense_efficiency_team,
        delta= f"{defense_efficiency:.1f} goals per shots conceded",
        border=True, 
        delta_color="blue", delta_arrow="off")

        st.metric("Best SOT Blocking", 
        sot_block_team,
        delta= f"{sot_block:.1f} shots on target conceded per 90",
        border=True, 
        delta_color="blue", delta_arrow="off")

    
    #goals Against per 90 /Shots against per 90 / Shots on target conceded per 90
    #tackles won 
    #interceptions 
    #defensive efficiency goals_per_shot_against
    

# ------------------------------------------possession--------------------------------------------------------
with tab3:
    st.header(":material/percent: Team possesion")
    #- Possession 
    #Possesion
    #Crosses?
    #Offsides??

    #Higest possession
    #most goals with high possesion??? goals_assists_pens_per90
    #Most shots with possession? shots_per90


    #team possesion
    with st.container(border=True):
        team_possession=filtered_team[ ["team", "possession"] ].copy()
        
        st.subheader("Team possesion")
        st.bar_chart(team_possession,
        x="team",
        y="possession",
        x_label="Team",
        y_label="Possesion %",
        sort="-possession")

    #possesion% vs goals??

    

#-------------------------------------offensive vs defensive performance---------
with tab4:
    st.header(":material/balance: Offensive vs Defensive Performance")

    #Goals vs Goals Against
    with st.container(border=True):
        
        goals_scored_conceded=filtered_team[ ["team", "goals", "goals_against"] ].copy()
        
        st.subheader("Goals scored and conceded")
        st.bar_chart(goals_scored_conceded,
        x="team",
        y=["goals", "goals_against"],
        x_label="Team",
        y_label="GF and GA",
        stack=False)

    #Offensive vs Defensive Scatter
    team_performance = df[ ["team", "goals_per90", "goals_per90_against", "shots_per90","shots_per90_against"] ].copy()
    team_performance["shots_per90_difference"]= team_performance["shots_per90"]-team_performance["shots_per90_against"]
    team_performance["goals_per90_difference"]= team_performance["goals_per90"]-team_performance["goals_per90_against"]
    
    with st.container(border=True):
        st.subheader("Offensive vs Defensive Scatter")

        st.scatter_chart(
            team_performance,
            x="shots_per90_difference",
            y="goals_per90_difference",
            color="team",
            x_label="Shot Differential per 90",
            y_label="Goal Difference per 90",
            size=100
        )



#-----------------------------------------------------------------------------------------------
#-----------------------------------------------discipline------------------------------
with tab5:
    st.header(":material/sports: Team Discipline")

    team_discipline=filtered_team[ ["team", "cards_yellow","cards_red","fouls"] ].copy()

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



    dis1, dis2=st.columns(2)
    with dis1:
        st.metric("Most yellow cards", 
        max_ycards_team,
        delta= f"{max_ycards:.0f} cards",
        border=True, 
        icon=":material/crop_2_3:", 
        delta_color="blue", delta_arrow="off")

        st.metric("Fewer fouls", 
        min_fouls_team,
        delta= f"{min_fouls:.0f} fouls",
        border=True, 
        icon=":material/sports:",
        delta_color="blue", delta_arrow="off")

    with dis2:
        st.metric("Most red cards", 
        max_rcards_team,
        delta= f"{max_rcards:.0f} cards",
        border=True, 
        icon=":material/crop_2_3:",
        delta_color="blue", delta_arrow="off")

        st.metric("Most fouls", 
        max_fouls_team,
        delta= f"{max_fouls:.0f} fouls",
        border=True, 
        icon=":material/sports:",
        delta_color="blue", delta_arrow="off")
        


    # graph red cards, yellow cards, fouls
    with st.container(border=True):
        st.subheader("Red Cards, Yellow Cards and Fouls")
        st.bar_chart(team_discipline,
        x="team",
        y=["cards_red","cards_yellow", "fouls"],
        x_label="Team",
        y_label="Cards and Fouls",
        color=["red", "yellow", "blue"],
        stack=False)

    
