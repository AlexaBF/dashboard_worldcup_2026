import streamlit as st
import pandas as pd

st.title("PLAYERS")

@st.cache_data
def load_data():
    df=pd.read_csv("datasets/players.csv")
    df['club'] = df['club'].fillna('No Club')
    df = df.fillna(0)
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
    delta=f"Goals: {top_scorers["goals"].iloc[1]:.0f}",
    border=True,
    icon=":material/trophy:",
    delta_arrow="off")
with s_place2:
    st.metric(label="1st Place",
    value=top_scorers["player"].iloc[0],
    delta=f"Goals: {top_scorers["goals"].iloc[0]:.0f}",
    border=True,
    icon=":material/trophy:",
    delta_arrow="off")
    
with s_place3:
    st.metric(label="3rd Place",
    value=top_scorers["player"].iloc[2],
    delta=f"Goals: {top_scorers["goals"].iloc[2]:.0f}",
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
    delta=f"Assists: {top_assists["assists"].iloc[1]:.0f}",
    border=True,
    icon=":material/trophy:",
    delta_arrow="off")
with a_place2:
    st.metric(label="1st Place",
    value=top_assists["player"].iloc[0],
    delta=f"Assists: {top_assists["assists"].iloc[0]:.0f}",
    border=True,
    icon=":material/trophy:",
    delta_arrow="off")
    
with a_place3:
    st.metric(label="3rd Place",
    value=top_assists["player"].iloc[2],
    delta=f"Assists: {top_assists["assists"].iloc[2]:.0f}",
    border=True,
    icon=":material/trophy:",
    delta_arrow="off")


#----------------------------------------------------max goal_contributions------------------------------------
goal_contributions=df[["player","goals","assists","goals_assists"]].copy()

max_gc=int(goal_contributions["goals_assists"].max())
top_gc_player=goal_contributions.loc[ goal_contributions["goals_assists"] == max_gc, "player" ].iloc[0]

col1,col2=st.columns(2)
with col1:
    st.metric(label="Most goal contributions ",
    value=top_gc_player, 
    border=True,
    delta=f"G+A: {max_gc}",
    icon=":material/workspace_premium:",
    delta_arrow="off")


##---------------------------golden boot---------

gold_boot=df[["player","goals_assists","minutes"]].copy()

gold_boot_player = (gold_boot.sort_values( ["goals_assists", "minutes"], ascending=[False, True]).iloc[0]["player"])
gold_boot_minutes = (gold_boot.sort_values( ["goals_assists", "minutes"], ascending=[False, True]).iloc[0]["minutes"])

with col2:
    st.metric(label="Golden Boot Player",
    value=gold_boot_player,
    border=True,
    delta=f"G+A: {max_gc} , Minutes: {gold_boot_minutes:.0f}",
    icon=":material/workspace_premium:",
    delta_arrow="off")

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


ps1,ps2,ps3,ps4 = st.tabs(["Attack", "Efficiency", "Activity", "Discipline"])

#-----------attack
with ps1:

    attack_df=filtered_players[["player","goals","assists","goals_assists","shots","shots_on_target","minutes"]].copy()

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


    col1,col2=st.columns(2)
    with col1:
        st.metric(label="Most goals ",
        value=ps_max_goals_player,
        border=True,
        delta= f"Goals: {ps_max_goals}", delta_color="blue", delta_arrow="off")

        st.metric(label="Most shots ",
        value=ps_max_shots_player,
        border=True,
        delta= f"Shots: {ps_max_shots}", delta_color="blue", delta_arrow="off")
        
        
    with col2:
        st.metric(label="Most assists",
        value=ps_max_assists_player,
        border=True,
        delta= f"Assists: {ps_max_assists}", delta_color="blue", delta_arrow="off")

        st.metric(label="Most shots on target",
        value=ps_max_sot_player,
        border=True,
        delta= f" SOT: {ps_max_sot}", delta_color="blue", delta_arrow="off")

    

    with st.container(border=True):
        st.header("Goal Contributions")
        
        #most goals contributions goals + assits
        values = st.slider("Select a range of values", 0, max_gc, (6,max_gc))
        filtered_attack_df = attack_df[(attack_df["goals_assists"] >= values[0]) & (df["goals_assists"] <= values[1])]
        
        st.bar_chart(filtered_attack_df,
        x="player",
        y=["goals","assists"],
        sort="goals_assists",
        x_label="Player",
        y_label="Goal Contributions")

    with st.container(border=True):
        st.header("Goal Contributions vs Minutes")
        st.scatter_chart(
            attack_df,
            x="minutes",
            y="goals_assists",
            x_label="Minutes",
            y_label="Goal Contributions",
            size=100,
            color="player")
    

    

#--efficiency
with ps2:
    efficiency_df=filtered_players[["player","goals_per90","assists_per90","goals_assists_per90","shots_per90","shots_on_target_per90","minutes"]].copy()
    efficiency_df["shot_conversion_per90"]= (efficiency_df["goals_per90"] / efficiency_df["shots_per90"] ) *100

    #goals/90
    ps_goals90=efficiency_df["goals_per90"].max()
    ps_goals90_player=efficiency_df.loc[ efficiency_df["goals_per90"] == ps_goals90, "player" ].iloc[0]

    #assists/90
    ps_assists90=efficiency_df["assists_per90"].max()
    ps_assists90_player=efficiency_df.loc[ efficiency_df["assists_per90"] == ps_assists90, "player" ].iloc[0]

    #goasl+assists/90
    ps_goals_assists90=efficiency_df["goals_assists_per90"].max()
    ps_goals_assists90_player=efficiency_df.loc[ efficiency_df["goals_assists_per90"] == ps_goals_assists90, "player" ].iloc[0]

    #shots on target/90
    ps_shots_on_target90=efficiency_df["shots_on_target_per90"].max()
    ps_shots_on_target90_player=efficiency_df.loc[ efficiency_df["shots_on_target_per90"] == ps_shots_on_target90, "player" ].iloc[0]


    col1,col2=st.columns(2)
    with col1:
        st.metric(label="Goals per 90",
        value=ps_goals90_player,
        border=True,
        delta= f"Goals/90: {ps_goals90:.1f}", delta_color="blue", delta_arrow="off")

        st.metric(label="Assits per 90",
        value=ps_assists90_player,
        border=True,
        delta= f"Assits/90: {ps_assists90:.1f}", delta_color="blue", delta_arrow="off")


    with col2:
        st.metric(label="Goal contributions per 90",
        value=ps_goals_assists90_player,
        border=True,
        delta= f"G+A/90: {ps_goals_assists90:.1f}", delta_color="blue", delta_arrow="off")

        st.metric(label="Shots on target per 90",
        value=ps_shots_on_target90_player,
        border=True,
        delta= f"SOT/90: {ps_shots_on_target90:.1f}", delta_color="blue", delta_arrow="off")
    
    with st.container(border=True):
        st.header("Goals vs Shots per 90")
        st.scatter_chart(
            efficiency_df,
            x="goals_per90",
            y="shots_per90",
            x_label="Goals per 90",
            y_label="Shots per 90",
            color="player",
            size="minutes")

    #Shot conversion rate
    with st.container(border=True):
        st.header("Shot Conversion vs Shots per 90")
        st.scatter_chart(
            efficiency_df,
            x="shot_conversion_per90",
            y="shots_per90",
            x_label="Shot Conversion per 90 %",
            y_label="Shots per 90",
            color="player",
            size="minutes")


#--activity
with ps3:
    activity_df=filtered_players[["player","tackles_won","interceptions", "offsides", "crosses","minutes"]].copy()
    
    #tackles_won
    ps_tackles_won=activity_df["tackles_won"].max()
    ps_tackles_won_player=activity_df.loc[ activity_df["tackles_won"] == ps_tackles_won, "player" ].iloc[0]

    #interceptions
    ps_interceptions=activity_df["interceptions"].max()
    ps_interceptions_player=activity_df.loc[ activity_df["interceptions"] == ps_interceptions, "player" ].iloc[0]

    #offsides
    ps_offsides=activity_df["offsides"].max()
    ps_offsides_player=activity_df.loc[ activity_df["offsides"] == ps_offsides, "player" ].iloc[0]

    #crosses
    ps_crosses=activity_df["crosses"].max()
    ps_crosses_player=activity_df.loc[ activity_df["crosses"] == ps_crosses, "player" ].iloc[0]
    
    col1,col2=st.columns(2)
    with col1:
        st.metric(label="Most Tackles Won",
        value=ps_tackles_won_player,
        border=True,
        delta= f"Tackles Won: {ps_tackles_won:.0f}", delta_color="blue", delta_arrow="off")

        st.metric(label="Most Interceptions",
        value=ps_interceptions_player,
        border=True,
        delta= f"Interceptions: {ps_interceptions:.0f}", delta_color="blue", delta_arrow="off")


    with col2:
        st.metric(label="Most offsides",
        value=ps_offsides_player,
        border=True,
        delta= f"Offsides: {ps_offsides:.0f}", delta_color="blue", delta_arrow="off")

        st.metric(label="Most Crosses",
        value=ps_crosses_player,
        border=True,
        delta= f"Crosses: {ps_crosses:.0f}", delta_color="blue", delta_arrow="off")

    #tackles vs interceptions
    with st.container(border=True):
        st.header("Tackles Won vs Interceptions")
        st.scatter_chart(
            activity_df,
            x="tackles_won",
            y="interceptions",
            x_label="Tackles Won",
            y_label="Interceptions",
            color="player",
            size="minutes")

    #minutes vs tackles
    with st.container(border=True):
        st.header("Minutes vs Tackles Won")
        st.scatter_chart(
            activity_df,
            x="minutes",
            y="tackles_won",
            x_label="minutes",
            y_label="Tackles Won",
            color="player",
            size=100)
    
    #tackles won players top 10
    with st.container(border=True):
        sort_act_tackles = activity_df.sort_values(by='tackles_won', ascending=False)
        st.header("Top 10 tacklers")
        st.bar_chart(sort_act_tackles.head(10),
        x="player",
        y="tackles_won",
        x_label="Player",
        y_label="Tackles Won",
        sort="-tackles_won")

    #crossers players top 10
    with st.container(border=True):
        sort_act_tackles = activity_df.sort_values(by='crosses', ascending=False)
        st.header("Top 10 crossers")
        st.bar_chart(sort_act_tackles.head(10),
        x="player",
        y="crosses",
        x_label="Player",
        y_label="Crosses",
        sort="-crosses")
    

#--discipline 
with ps4:
    discipline_df=filtered_players[["player","fouls","fouled", "cards_yellow", "cards_red","minutes"]].copy()
    
    #fouls
    ps_max_fouls=discipline_df["fouls"].max()
    ps_max_fouls_player=discipline_df.loc[ discipline_df["fouls"] == ps_max_fouls, "player" ].iloc[0]

    #fouled
    ps_max_fouled=discipline_df["fouled"].max()
    ps_max_fouled_player=discipline_df.loc[ discipline_df["fouled"] == ps_max_fouled, "player" ].iloc[0]

    #cards_yellow
    ps_max_yellow=discipline_df["cards_yellow"].max()
    ps_min_yellow=discipline_df["cards_yellow"].min()
    ps_max_yellow_player=discipline_df.loc[ discipline_df["cards_yellow"] == ps_max_yellow, "player" ].iloc[0]
    ps_min_yellow_player=discipline_df.loc[ discipline_df["cards_yellow"] == ps_min_yellow, "player" ].iloc[0]

    #cards_red
    ps_max_red=discipline_df["cards_red"].max()
    ps_min_red=discipline_df["cards_red"].min()
    ps_max_red_player=discipline_df.loc[ discipline_df["cards_red"] == ps_max_red, "player" ].iloc[0]
    ps_min_red_player=discipline_df.loc[ discipline_df["cards_red"] == ps_min_red, "player" ].iloc[0]
    
    col1,col2,col3=st.columns(3)
    with col1:
        st.metric(label="Most Fouls",
        value=ps_max_fouls_player,
        border=True,
        delta= f"Fouls: {ps_max_fouls:.0f}", delta_color="blue", delta_arrow="off")

        st.metric(label="Most Fouled",
        value=ps_max_fouled_player,
        border=True,
        delta= f"Fouls: {ps_max_fouled:.0f}", delta_color="blue", delta_arrow="off") 


    with col2:
        st.metric(label="Least Yellow Cards",
        value=ps_min_yellow_player,
        border=True,
        delta= f"Cards: {ps_max_yellow:.0f}", delta_color="blue", delta_arrow="off")

        st.metric(label="Most Yellow Cards",
        value=ps_max_yellow_player,
        border=True,
        delta= f"Cards: {ps_max_yellow:.0f}", delta_color="blue", delta_arrow="off")

    with col3:
        st.metric(label="Least Red Cards",
        value=ps_min_red_player,
        border=True,
        delta= f"Cards: {ps_max_red:.0f}", delta_color="blue", delta_arrow="off")

        st.metric(label="Most Red Cards",
        value=ps_max_red_player,
        border=True,
        delta= f"Cards: {ps_max_red:.0f}", delta_color="blue", delta_arrow="off")


    #minutes vs fouls
    with st.container(border=True):
        st.header("Minutes vs Fouls")
        st.scatter_chart(
            discipline_df,
            x="minutes",
            y="fouls",
            x_label="Minutes",
            y_label="Fouls",
            color="player",
            size=100)

    #minutes vs yellow
    with st.container(border=True):
        st.header("Minutes vs Yellow Cards")
        st.scatter_chart(
            discipline_df,
            x="minutes",
            y="cards_yellow",
            x_label="Minutes",
            y_label="Yellow Cards",
            color="player",
            size=150)

    #minutes vs red
    with st.container(border=True):
        st.header("Minutes vs Red Cards")
        st.scatter_chart(
            discipline_df,
            x="minutes",
            y="cards_red",
            x_label="Minutes",
            y_label="Red Cards",
            color="player",
            size=150)


    #most fouled
    with st.container(border=True):
        sort_fouled= discipline_df.sort_values(by='fouled', ascending=False)
        st.header("Top 10 most fouled players")
        st.bar_chart(sort_fouled.head(10),
        x="player",
        y="fouled",
        x_label="Player",
        y_label="Fouls",   
        sort="-fouled")

    #most fouls
    with st.container(border=True):
        sort_fouls= discipline_df.sort_values(by='fouls', ascending=False)
        st.header("Top 10 players with the most fouls")
        st.bar_chart(sort_fouled.head(10),
        x="player",
        y="fouls",
        x_label="Player",
        y_label="Fouls",   
        sort="-fouls")
    