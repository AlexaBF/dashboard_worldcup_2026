import streamlit as st
import pandas as pd

st.title("PLAYERS")

@st.cache_data
def load_data():
    df=pd.read_csv("datasets/players.csv")
    df['club'] = df['club'].fillna('No Club')
    df = df[df["position"] != "GK"]
    return df

df=load_data()
st.dataframe(df)

st.header("Players Performance and Statistics")
#------------------------------------------Top scorers------------------------------------------
st.subheader(":material/social_leaderboard: Top Scorers")
top_scorers=df.sort_values(by=["goals","assists"], ascending=False).head(3)

s_place1,s_place2,s_place3 = st.columns(3)
with s_place1:
    st.metric(label="2nd Place",
    value=top_scorers["player"].iloc[1],
    delta=f"GOALS: {top_scorers["goals"].iloc[1]:.0f}",
    border=True,
    icon=":material/trophy:",
    delta_arrow="off")
with s_place2:
    st.metric(label="1st Place",
    value=top_scorers["player"].iloc[0],
    delta=f"GOALS: {top_scorers["goals"].iloc[0]:.0f}",
    border=True,
    icon=":material/trophy:",
    delta_arrow="off")
    
with s_place3:
    st.metric(label="3rd Place",
    value=top_scorers["player"].iloc[2],
    delta=f"GOALS: {top_scorers["goals"].iloc[2]:.0f}",
    border=True,
    icon=":material/trophy:",
    delta_arrow="off")
# ---------------------------------------
# ------------------------------Top assists------------------------------------------

st.subheader(":material/social_leaderboard: Top Assists")
top_assists=df.sort_values(by=["assists","goals"], ascending=False).head(3)

a_place1,a_place2,a_place3 = st.columns(3)
with a_place1:
    st.metric(label="2nd Place",
    value=top_assists["player"].iloc[1],
    delta=f"ASSISTS: {top_assists["assists"].iloc[1]:.0f}",
    border=True,
    icon=":material/trophy:",
    delta_arrow="off")
with a_place2:
    st.metric(label="1st Place",
    value=top_assists["player"].iloc[0],
    delta=f"ASSISTS: {top_assists["assists"].iloc[0]:.0f}",
    border=True,
    icon=":material/trophy:",
    delta_arrow="off")
    
with a_place3:
    st.metric(label="3rd Place",
    value=top_assists["player"].iloc[2],
    delta=f"ASSISTS: {top_assists["assists"].iloc[2]:.0f}",
    border=True,
    icon=":material/trophy:",
    delta_arrow="off")


#----------------------------------------------------max goal_contributions------------------------------------
goal_contributions=df[["player","goals","assists","goals_assists"]].copy()

max_gc=int(goal_contributions["goals_assists"].max())
top_gc_player=goal_contributions.loc[ goal_contributions["goals_assists"] == max_gc, "player" ].iloc[0]

st.metric(label="Most goal contributions ",value=top_gc_player, border=True)

##---------------------------golden boot---------

gold_boot=df[["player","goals_assists","minutes"]].copy()

gold_boot_player = (gold_boot.sort_values( ["goals_assists", "minutes"], ascending=[False, True]).iloc[0]["player"])
st.metric(label="Gold boot Player ",value=gold_boot_player, border=True)

#------------------------------------------------players------------------------------------------
st.divider()
st.header("Filter players")

#team filter
teams_selected = st.multiselect("Select Teams", df["team"].unique(), default=df["team"].unique())
filtered_players = df[df["team"].isin(teams_selected)]

#position filter
position_selected = st.multiselect("Select Position", ["FW", "MF", "DF"] ,default=["FW", "MF", "DF"])
filtered_players = filtered_players[ filtered_players["position"].str.contains( "|".join(position_selected),na=False)]

st.dataframe(filtered_players)


ps1,ps2,ps3,ps4 = st.tabs(["Attack", "Efficiency", "Defense", "Discipline"])

#-----------attack
with ps1:

    attack_df=filtered_players[["player","goals","assists","goals_assists","shots","shots_on_target"]].copy()
    attack_df["shot_conversion"]= (attack_df["goals"] / attack_df["shots"] ) *100

    #goal contributions
    ps_max_goal_contributions=int(attack_df["goals_assists"].max())
    ps_gc_player=attack_df.loc[ attack_df["goals_assists"] == ps_max_goal_contributions, "player" ].iloc[0]

    #goals
    ps_max_goals=int(attack_df["goals"].max())
    ps_max_goals_player=attack_df.loc[ attack_df["goals"] == ps_max_goals, "player" ].iloc[0]

    #assists
    ps_max_assists=int(attack_df["assists"].max())
    ps_max_assists_player=attack_df.loc[ attack_df["assists"] == ps_max_assists, "player" ].iloc[0]

    #shots
    ps_max_shots=int(attack_df["shots"].max())
    ps_max_shots_player=attack_df.loc[ attack_df["shots"] == ps_max_shots, "player" ].iloc[0]
    
    #shots on target
    ps_max_sot=int(attack_df["shots_on_target"].max())
    ps_max_sot_player=attack_df.loc[ attack_df["shots_on_target"] == ps_max_sot, "player" ].iloc[0]

    #shot conversion rate%(total goals/totalshots) *100
    ps_max_shot_conversion=int(attack_df["shot_conversion"].max())
    ps_max_shot_conversion_player=attack_df.loc[ attack_df["shot_conversion"] == ps_max_shot_conversion, "player" ].iloc[0]

    col1,col2,col3=st.columns(3)
    with col1:
        st.metric(label="Most goals ",value=ps_max_goals_player, border=True)
        st.metric(label="Most shots ",value=ps_max_shots_player, border=True)
        
    with col2:
        st.metric(label="Most assists",value=ps_max_assists_player, border=True)
        st.metric(label="Most shots on targets ",value=ps_max_sot_player, border=True)
        
    with col3:
        st.metric(label="Most goal contributions ",value=ps_gc_player, border=True)
        st.metric(label="best shot conversion rate",value=ps_max_shot_conversion_player, border=True)



    with st.container(border=True):
        st.header(":material/person_celebrate: Goal Contributions")
        #most goals contributions goals + assits
        
        values = st.slider("Select a range of values", 0, max_gc, (6,max_gc))
        filtered_df = goal_contributions[(goal_contributions["goals_assists"] >= values[0]) & (df["goals_assists"] <= values[1])]
        
        st.bar_chart(filtered_df,
        x="player",
        y=["goals","assists"],
        sort="goals_assists",
        x_label="Player",
        y_label="Goal Contributions")


    

#--efficiency
with ps2:
    st.header("efficiency")
    #goals/90
    #assists/90
    #goasl+assists/90
    #shots on target%




#--defense
with ps3:
    st.header("defense")
    #tackles_won
    #interceptions
    #offsides
    #crosses
    

#--discipline 
with ps4:
    st.header("discipline")
    #fouls
    #fouled
    #cards_yellow
    #cards_red
