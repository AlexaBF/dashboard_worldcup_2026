import streamlit as st
import pandas as pd
import plotly.express as px

st.title(":material/recent_actors: PLAYERS")

@st.cache_data
def load_data():
    df=pd.read_csv("datasets/players.csv")
    df["club"] = df["club"].fillna("No Club")
    df = df.fillna(0)
    df = df[df["position"] != "GK"]
    return df

df=load_data()

#------------------------------------------Top scorers------------------------------------------
st.subheader(":material/social_leaderboard: Top Scorers")
#df for top scorers
top_scorers=df.sort_values(by=["goals","assists"], ascending=False).head(3)
#podium of top scorers
s_place1,s_place2,s_place3 = st.columns(3)
with s_place1:
    st.metric( label="1st Place", value=top_scorers["player"].iloc[0],
    delta=f"Goals: {top_scorers["goals"].iloc[0]:.0f}", delta_arrow="off",
    border=True, icon=":material/trophy:")

with s_place2:
    st.metric( label="2nd Place", value=top_scorers["player"].iloc[1],
    delta=f"Goals: {top_scorers["goals"].iloc[1]:.0f}", delta_arrow="off",
    border=True, icon=":material/trophy:")
    
with s_place3:
    st.metric( label="3rd Place", value=top_scorers["player"].iloc[2],
    delta=f"Goals: {top_scorers["goals"].iloc[2]:.0f}", delta_arrow="off",
    border=True, icon=":material/trophy:")

# ------------------------------Top assists------------------------------------------
st.subheader(":material/social_leaderboard: Top Assists")
#df for top assists
top_assists=df.sort_values(by=["assists","goals"], ascending=False).head(3)
#podium of top assists
a_place1,a_place2,a_place3 = st.columns(3)
with a_place1:
    st.metric( label="1st Place", value=top_assists["player"].iloc[0],
    delta=f"Assists: {top_assists["assists"].iloc[0]:.0f}", delta_arrow="off",
    border=True, icon=":material/trophy:")
    
with a_place2:
    st.metric( label="2nd Place", value=top_assists["player"].iloc[1],
    delta=f"Assists: {top_assists["assists"].iloc[1]:.0f}", delta_arrow="off",
    border=True, icon=":material/trophy:")

with a_place3:
    st.metric( label="3rd Place", value=top_assists["player"].iloc[2],
    delta=f"Assists: {top_assists["assists"].iloc[2]:.0f}", delta_arrow="off",
    border=True, icon=":material/trophy:")
#------------------------------------function------------------------------------------------------------------
def get_player_with_the_most(the_most,dataframe):
    best_num=dataframe[the_most].max()
    best_players=dataframe.loc[ dataframe[the_most] == best_num, "player" ].tolist() 
    best_player = ", ".join(best_players)

    return best_num, best_player

#df for goal contributions
goal_contributions=df[["player","goals","assists","goals_assists"]].copy()
#max goal contributions and player that made it
max_gc, top_gc_player = get_player_with_the_most("goals_assists",goal_contributions)
max_gc=int(max_gc)

#df for gold boot
gold_boot=df[["player","goals_assists","minutes"]].copy()

gold_boot_player = (gold_boot.sort_values( ["goals_assists", "minutes"], ascending=[False, True]).iloc[0]["player"])
gold_boot_minutes = (gold_boot.sort_values( ["goals_assists", "minutes"], ascending=[False, True]).iloc[0]["minutes"])

st.subheader(":material/workspace_premium: Individual Recognition")
#metrics for individual recogniiton
col1,col2=st.columns(2)
with col1:
    st.metric( label="Most goal contributions ", value=top_gc_player, 
    border=True, icon=":material/workspace_premium:",
    delta=f"G+A: {max_gc}", delta_arrow="off")

with col2:
    st.metric( label="Golden Boot Player", value=gold_boot_player,
    border=True, icon=":material/workspace_premium:",
    delta=f"G+A: {max_gc} , Minutes: {gold_boot_minutes:.0f}", delta_arrow="off" )

#------------------------------------------------------------------------------------------------------------------------
st.divider()
st.header(":material/user_attributes: Players Performance and Statistics")

#team filter
teams_selected = st.multiselect(":material/filter_alt: Select Teams", df["team"].unique(), default=df["team"].unique())
filtered_players = df[df["team"].isin(teams_selected)]

#position filter
position_selected = st.multiselect(":material/filter_alt: Select Position", ["FW", "MF", "DF"] ,default=["FW", "MF", "DF"])
filtered_players = filtered_players[ filtered_players["position"].str.contains( "|".join(position_selected),na=False)]

#------------------------------------------------------------------------------------------------------------------------
tab_all_players, tab_single_player = st.tabs([":material/groups: Players",":material/person: Player"])
#------------------------------------------------players---------------------------------------------------------------------------
with tab_all_players:
    with st.container(border=True):
        st.subheader(":material/groups: Tournament Players' Info")

        #tabs for all players
        ps1,ps2,ps3,ps4 = st.tabs([":material/sprint: Attack",":material/arrow_shape_up_stack_2: Efficiency",":material/directions_walk: Activity",":material/sports: Discipline"])
    
    #-----------------------------------attack------------------------------------------------
    with ps1:
        st.subheader(":material/sprint: Attack")
        #df for attack metrics
        attack_df=filtered_players[["player","goals","assists","goals_assists","shots","shots_on_target","minutes"]].copy()

        #goals
        ps_max_goals, ps_max_goals_player = get_player_with_the_most("goals",attack_df)
        #assists
        ps_max_assists, ps_max_assists_player = get_player_with_the_most("assists",attack_df)
        #shots
        ps_max_shots, ps_max_shots_player = get_player_with_the_most("shots",attack_df)
        #shots on target
        ps_max_sot, ps_max_sot_player = get_player_with_the_most("shots_on_target",attack_df)

        #attack metrics 
        col1,col2=st.columns(2)
        with col1:
            st.metric( label="Most goals", value=ps_max_goals_player,
            border=True, icon=":material/sports_soccer:",
            delta= f"Goals: {ps_max_goals:.0f}", delta_color="blue", delta_arrow="off" )

            st.metric( label="Most shots", value=ps_max_shots_player,
            border=True, icon=":material/shoe_cleats:",
            delta= f"Shots: {ps_max_shots:.0f}", delta_color="blue", delta_arrow="off")
            
        with col2:
            st.metric( label="Most assists", value=ps_max_assists_player,
            border=True, icon=":material/group:",
            delta= f"Assists: {ps_max_assists:.0f}", delta_color="blue", delta_arrow="off")

            st.metric( label="Most shots on target", value=ps_max_sot_player,
            border=True, icon=":material/target:",
            delta= f" SOT: {ps_max_sot:.0f}", delta_color="blue", delta_arrow="off")

        #goal contributions
        with st.container(border=True):
            st.header("Goal Contributions")
            #most goal contributions filter 
            values = st.slider("Select a range of values", 0, max_gc, (6, max_gc ))
            filtered_attack_df = attack_df[(attack_df["goals_assists"] >= values[0]) & (attack_df["goals_assists"] <= values[1])]
            #plot goal contributions bar chart
            st.bar_chart(
                filtered_attack_df,
                x="player",
                y=["goals","assists"],
                sort="goals_assists",
                x_label="Player",
                y_label="Goal Contributions")

        #scatter chart goal contributions vs minutes 
        fig_goal_contributions = px.scatter(
            attack_df,
            x="minutes",
            y="goals_assists",
            color="player",
            size="goals_assists",
            size_max=30,
            labels={
                "minutes":"Minutes",
                "goals_assists": "Goal Contributions"
            }
        )
        fig_goal_contributions.update_layout(showlegend = False)
        #plot goal contributions vs minutes scatter chart
        with st.container(border=True):
            st.header("Goal Contributions vs Minutes")
            st.plotly_chart(fig_goal_contributions)

    #--------------------------------------------------------efficiency------------------------------------------------------
    with ps2:
        st.subheader(":material/arrow_shape_up_stack_2: Efficiency")

        #df for efficiency metrics
        efficiency_df=filtered_players[["player","goals_per90","assists_per90","goals_assists_per90","shots_per90","shots_on_target_per90","minutes"]].copy()
        efficiency_df["shot_conversion_per90"]= (efficiency_df["goals_per90"] / efficiency_df["shots_per90"] ) *100

        #goals/90
        ps_goals90, ps_goals90_player = get_player_with_the_most("goals_per90",efficiency_df )
        #assists/90
        ps_assists90, ps_assists90_player = get_player_with_the_most("assists_per90",efficiency_df)
        #goasl+assists/90
        ps_goals_assists90, ps_goals_assists90_player = get_player_with_the_most("goals_assists_per90",efficiency_df)
        #shots on target/90
        ps_shots_on_target90, ps_shots_on_target90_player = get_player_with_the_most("shots_on_target_per90",efficiency_df)

        #show efficency metrics
        col1,col2=st.columns(2)
        with col1:
            st.metric( label="Goals per 90", value=ps_goals90_player,
            border=True, icon=":material/sports_soccer:",
            delta= f"Goals/90: {ps_goals90:.1f}", delta_color="blue", delta_arrow="off")

            st.metric(label="Assits per 90", value=ps_assists90_player,
            border=True, icon=":material/group:",
            delta= f"Assits/90: {ps_assists90:.1f}", delta_color="blue", delta_arrow="off")

        with col2:
            st.metric( label="Goal contributions per 90", value=ps_goals_assists90_player,
            border=True, icon=":material/sports_and_outdoors:",
            delta= f"G+A/90: {ps_goals_assists90:.1f}", delta_color="blue", delta_arrow="off")

            st.metric(label="Shots on target per 90", value=ps_shots_on_target90_player,
            border=True, icon=":material/target:",
            delta= f"SOT/90: {ps_shots_on_target90:.1f}", delta_color="blue", delta_arrow="off")
        
        #scatter chart goals vs shots per 90
        fig_goals_shots_90 = px.scatter(
            efficiency_df,
            y="goals_per90",
            x="shots_per90",
            labels={
                "goals_per90":"Goals per 90",
                "shots_per90":"Shots per 90"
            },
            color="player",
            size="shots_per90"
        )
        fig_goals_shots_90.update_layout(showlegend = False)

        #scatter Shot conversion %
        fig_shot_conversion = px.scatter(
            efficiency_df,
            y="shot_conversion_per90",
            x="shots_per90",
            labels={
                "shot_conversion_per90":"Shot Conversion per 90 %",
                "shots_per90":"Shots per 90"
            },
            color="player"
        )
        fig_shot_conversion.update_layout(showlegend = False)

        #plot scatter goals vs shots per 90
        with st.container(border=True):
            st.header("Goals vs Shots per 90")
            st.plotly_chart(fig_goals_shots_90)

        #plot scatter Shot conversion rate
        with st.container(border=True):
            st.header("Shot Conversion vs Shots per 90")
            st.plotly_chart(fig_shot_conversion)
            
    #----------------------------------------------------------activity----------------------------------------------------------------------
    with ps3:
        st.subheader(":material/directions_walk: Activity")
        #df for activity metrics
        activity_df=filtered_players[["player","tackles_won","interceptions", "offsides", "crosses","minutes"]].copy()
        
        #tackles_won
        ps_tackles_won, ps_tackles_won_player = get_player_with_the_most("tackles_won",activity_df)
        #interceptions
        ps_interceptions,ps_interceptions_player = get_player_with_the_most("interceptions",activity_df)
        #offsides
        ps_offsides, ps_offsides_player= get_player_with_the_most("offsides",activity_df)
        #crosses
        ps_crosses,ps_crosses_player = get_player_with_the_most("crosses",activity_df)
        
        #metrics for activity
        col1,col2=st.columns(2)
        with col1:
            st.metric( label="Most Tackles Won", value=ps_tackles_won_player,
            border=True, icon=":material/cheer:",
            delta= f"Tackles Won: {ps_tackles_won:.0f}", delta_color="blue", delta_arrow="off")

            st.metric(label="Most Interceptions", value=ps_interceptions_player,
            border=True, icon=":material/cheer:",
            delta= f"Interceptions: {ps_interceptions:.0f}", delta_color="blue", delta_arrow="off")

        with col2:
            st.metric( label="Most offsides", value=ps_offsides_player,
            border=True, icon=":material/flag_2:",
            delta= f"Offsides: {ps_offsides:.0f}", delta_color="blue", delta_arrow="off")

            st.metric( label="Most Crosses", value=ps_crosses_player,
            border=True, icon=":material/step_over:",
            delta= f"Crosses: {ps_crosses:.0f}", delta_color="blue", delta_arrow="off")

        #plot scatter tackles vs interceptions
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

        #plot scatter minutes vs tackles
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
        
        #plot bar chart tackles won players top 10
        with st.container(border=True):
            sort_act_tackles = activity_df.sort_values(by="tackles_won", ascending=False)
            st.header("Top 10 tacklers")
            st.bar_chart(sort_act_tackles.head(10),
            x="player",
            y="tackles_won",
            x_label="Player",
            y_label="Tackles Won",
            sort="-tackles_won")

        #plot bar chart crossers players top 10
        with st.container(border=True):
            sort_act_tackles = activity_df.sort_values(by="crosses", ascending=False)
            st.header("Top 10 crossers")
            st.bar_chart(sort_act_tackles.head(10),
            x="player",
            y="crosses",
            x_label="Player",
            y_label="Crosses",
            sort="-crosses")
        

    #---------------------------------------------discipline------------------------------------------------------
    with ps4:
        st.subheader(":material/sports: Discipline")
        #df for discipline metrics
        discipline_df=filtered_players[["player","fouls","fouled", "cards_yellow", "cards_red","minutes"]].copy()
        
        #fouls
        ps_max_fouls, ps_max_fouls_player = get_player_with_the_most("fouls",discipline_df)
        #fouled
        ps_max_fouled, ps_max_fouled_player= get_player_with_the_most("fouled",discipline_df)
        #cards_yellow
        ps_max_yellow, ps_max_yellow_player= get_player_with_the_most("cards_yellow",discipline_df)
        #cards_red
        ps_max_red, ps_max_red_player= get_player_with_the_most("cards_red",discipline_df)

        #metrics of discipline
        col1,col2=st.columns(2)
        with col1:
            st.metric( label="Most Fouls", value=ps_max_fouls_player,
            border=True, icon=":material/sports:",
            delta= f"Fouls: {ps_max_fouls:.0f}", delta_color="blue", delta_arrow="off")

            st.metric( label="Most Fouled", value=ps_max_fouled_player,
            border=True, icon=":material/sports:",
            delta= f"Fouls: {ps_max_fouled:.0f}", delta_color="blue", delta_arrow="off") 

        with col2:
            st.metric( label="Most Yellow Cards", value=ps_max_yellow_player,
            border=True, icon=":material/crop_2_3:",
            delta= f"Cards: {ps_max_yellow:.0f}", delta_color="blue", delta_arrow="off")

            st.metric( label="Most Red Cards", value=ps_max_red_player,
            border=True, icon=":material/crop_2_3:",
            delta= f"Cards: {ps_max_red:.0f}", delta_color="blue", delta_arrow="off")

        #plot scatter minutes vs fouls
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

        #plot scatter minutes vs yellow
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

        #plot scatter minutes vs red
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

        #plot bar chart most fouled
        with st.container(border=True):
            sort_fouled= discipline_df.sort_values(by="fouled", ascending=False)
            st.header("Top 10 most fouled players")
            st.bar_chart(sort_fouled.head(10),
            x="player",
            y="fouled",
            x_label="Player",
            y_label="Fouls",   
            sort="-fouled")

        #plot bar chart most fouls
        with st.container(border=True):
            sort_fouls= discipline_df.sort_values(by="fouls", ascending=False)
            st.header("Top 10 players with the most fouls")
            st.bar_chart(sort_fouls.head(10),
            x="player",
            y="fouls",
            x_label="Player",
            y_label="Fouls",   
            sort="-fouls")
    
#----------------------------------------------player basic info---------------------------------------------
with tab_single_player:
    with st.container(border=True):
        st.subheader(":material/person: Tournament Player's Info ")
        #player list to filter player 
        players_list = filtered_players["player"].unique().tolist()
        selected_player = st.selectbox("Select player", players_list)
        #df for player selected 
        filtered_player_df = filtered_players[filtered_players["player"] == selected_player]

        #player metrics
        col1,col2,col3=st.columns(3)
        with col1:
            st.metric( label="Player", value=filtered_player_df.iloc[0]["player"],
            border=True, icon=":material/person:")

            st.metric( label="Position", value=filtered_player_df.iloc[0]["position"],
            border=True, icon=":material/person_pin:")

        with col2:
            st.metric( label="Age", value=filtered_player_df.iloc[0]["age"],
            border=True, icon=":material/calendar_today:")

            st.metric( label="Team", value=filtered_player_df.iloc[0]["team"],
            border=True, icon=":material/flag:")
            
        with col3:
            st.metric( label="birth year", value=filtered_player_df.iloc[0]["birth_year"],
            border=True, icon=":material/perm_contact_calendar:")

            st.metric( label="Club", value=filtered_player_df.iloc[0]["club"],
            border=True, icon=":material/groups:")

        #player info tabs
        tab1,tab2,tab3,tab4,tab5,tab6,tab7 = st.tabs([":material/directions_run: Playing Time",":material/scoreboard: Scoring",":material/shoe_cleats: Shooting",":material/person_play: Creativity",":material/sports: Discipline",":material/diversity_3: Team",":material/shield: Defensive"])

    #---------------------------------------------------------playing time---------------------------------------------------
    with tab1:
        st.subheader(":material/directions_run: Player Playing Time")
        #df for player playing time
        play_time_df=filtered_player_df[["player","games","minutes_90s", "games_starts","minutes","minutes_pct","minutes_per_sub","minutes_per_start","games_complete"]].copy()

        #minutes per game
        games = play_time_df.iloc[0]["games"]
        minutes = play_time_df.iloc[0]["minutes"]
        minutes_pg = minutes / games if games > 0 else 0

        #player playing time metrics
        col1,col2,col3=st.columns(3)
        with col1:
            st.metric( label="Games played", value=play_time_df.iloc[0]["games"],
            border=True, icon=":material/date_range:")

            st.metric( label="Minutes per 90", value=play_time_df.iloc[0]["minutes_90s"],
            border=True, icon=":material/acute:")

        with col2:
            st.metric( label="Games started", value=play_time_df.iloc[0]["games_starts"],
            border=True, icon=":material/date_range:")

            st.metric(label="Minutes per game", value=f"{minutes_pg:.2f}",
            border=True, icon=":material/acute:")

        with col3:
            st.metric( label="Minutes played", value=play_time_df.iloc[0]["minutes"],
            border=True, icon=":material/acute:")
        
            st.metric( label="of Team Minutes Played",value=f"{play_time_df.iloc[0]["minutes_pct"]:.2f}%",
            border=True, icon=":material/percent:")

        #plot bar chart Starts vs substitute appearances
        with st.container(border=True):
            st.header("Starts vs substitute appearances")
            st.bar_chart(
                play_time_df,
                x="player",
                y=["minutes_per_start","minutes_per_sub"],
                y_label="Minutes as starter and as sub",
                color=["orange","blue"],
                stack=False)
        
        #plot bar chart games vs games_complete
        with st.container(border=True):
            st.header("Games played vs Games Completed")
            st.bar_chart(
                play_time_df,
                x="player",
                y=["games","games_complete"],
                y_label="Games played",
                color=["#298c8c","#a00000"],
                stack=False)

    #-------------------------------------------score--------------------------------------------------------
    with tab2:
        st.subheader(":material/scoreboard: Goal Scoring")
        #df for goal scoring metrics
        goal_scoring_df=filtered_player_df[["player","goals","goals_pens","goals_per90","goals_pens_per90","pens_made","pens_att"]].copy()

        #show goal scoring metrics
        col1,col2,col3 =st.columns(3)
        with col1:
            st.metric( label="Goals", value=int(goal_scoring_df.iloc[0]["goals"] ),
            border=True, icon=":material/sports_soccer:")
            
            st.metric( label="Non-penalty goals", value=int( goal_scoring_df.iloc[0]["goals_pens"] ),
            border=True, icon=":material/sports_and_outdoors:")

        with col2:
            st.metric( label="Goals per 90", value=goal_scoring_df.iloc[0]["goals_per90"],
            border=True, icon=":material/sports_soccer:")

            st.metric( label="Non-penalty goals per 90", value=goal_scoring_df.iloc[0]["goals_pens_per90"],
            border=True, icon=":material/sports_and_outdoors:")

        with col3:
            st.metric(label="Penalties made", value=int(goal_scoring_df.iloc[0]["pens_made"]),
            border=True, icon=":material/shoe_cleats:")

            st.metric(label="Penalties attempted", value=int( goal_scoring_df.iloc[0]["pens_att"] ),
            border=True, icon=":material/shoe_cleats:")

        #plot bar chart goals vs non penalties goals
        with st.container(border=True):
            st.header("Goals vs Non penalties goals")   
            st.bar_chart(
                goal_scoring_df,
                x="player",
                y=["goals","goals_pens"],
                y_label="Goals",
                color=["orange", "blue"], 
                stack=False)

        #plot bar chart penalties made vs attempt
        with st.container(border=True):
            st.header("Penalties made vs Penalties attempted")   
            st.bar_chart(
                goal_scoring_df,
                x="player",
                y=["pens_att","pens_made"],
                y_label="Penalties",
                color=["red", "green"], 
                stack=False)
        
    #------------------------------------------------------Shooting------------------------------------------------------
    with tab3:
        st.subheader(":material/shoe_cleats: Shooting")
        #df for shooting metrics
        shooting_df=filtered_player_df[["player","goals", "shots","shots_per90","shots_on_target","shots_on_target_pct","minutes"]].copy()
        #Goal conversion rate -measures how often a player scores from any shot attempt
        shooting_df["g_c_rate_pct"]=( shooting_df["goals"]/shooting_df["shots"] )*100
        #Goal conversion rate on target- measures how clinical a player is when they hit the target
        shooting_df["g_c_rate_target_pct"]=( shooting_df["goals"]/shooting_df["shots_on_target"] )*100

        #show metrics
        col1,col2,col3 =st.columns(3)
        with col1:
            st.metric( label="Shots", value=int(shooting_df.iloc[0]["shots"] ),
            border=True, icon=":material/shoe_cleats:")
            
            st.metric( label="Shots per 90", value=int( shooting_df.iloc[0]["shots_per90"] ),
            border=True, icon=":material/shoe_cleats:")

        with col2:
            st.metric( label="Shots on target", value=shooting_df.iloc[0]["shots_on_target"],
            border=True, icon=":material/target:")
            
            st.metric( label="Shot Accuracy %", value=f"{shooting_df.iloc[0]["shots_on_target_pct"]}%",
            border=True, icon=":material/target:")

        with col3: 
            st.metric( label="Goal conversion rate", value=f"{shooting_df.iloc[0]["g_c_rate_pct"]:.2f}%",
            border=True, icon=":material/percent:")

            st.metric( label="Goal conversion rate on target", value=f"{shooting_df.iloc[0]["g_c_rate_target_pct"]:.2f}%",
            border=True, icon=":material/percent:")

        #plot br chart shots vs goals
        with st.container(border=True):
            st.header("Shots vs Goals")   
            st.bar_chart(
                shooting_df,
                x="player",
                y=["shots","shots_on_target","goals"],
                y_label="Shots",
                color=["#298c8c","#a00000","#F54927"],
                stack=False)

        #plot bar chart conversion rate and converion rate on target
        with st.container(border=True):
            st.header("Goal conversion rate vs Goal conversion rate on target")   
            st.bar_chart(
                shooting_df,
                x="player",
                y=["g_c_rate_target_pct","g_c_rate_pct"],
                y_label="Conversion rate %",
                color="minutes",
                stack=False)

    #----------------------------------------------Creativity--------------------------------------------------------
    with tab4:
        st.subheader(":material/person_play: Player Creatvity")
        #df for creativity metrics
        creativity_df=filtered_player_df[["player","goals","goals_per90","assists","assists_per90","goals_assists", "goals_assists_per90"]].copy()

        #show metrics
        col1,col2 =st.columns(2)
        with col1:
            st.metric( label="Assists", value=int(creativity_df.iloc[0]["assists"] ),
            border=True, icon=":material/group:")

            st.metric( label="Goals + Assists", value=int( creativity_df.iloc[0]["goals_assists"] ),
            border=True, icon=":material/sports_soccer:")    

        with col2:
            st.metric( label="Assists per 90", value=creativity_df.iloc[0]["assists_per90"],
            border=True, icon=":material/group:")
            
            st.metric( label="Goals + Assists per 90", value=creativity_df.iloc[0]["goals_assists_per90"],
            border=True, icon=":material/sports_soccer:")

        #plot bar chart shots vs goals
        with st.container(border=True):
            st.header("Goals vs assists")   
            st.bar_chart(
                creativity_df,
                x="player",
                y=["goals","assists"],
                y_label="G+A",
                color=["#298c8c","#a00000"],
                stack=False)
        
        #plot bar chart Goals vs assists per 90
        with st.container(border=True):
            st.header("Goals vs assists per 90")   
            st.bar_chart(
                creativity_df,
                x="player",
                y=["goals_per90","assists_per90","goals_assists_per90"],
                y_label="G+A/90",
                color=["#298c8c","#a00000","orange"],
                stack=False)


    #--------------------------------------------Discipline-------------------------------------------------------
    with tab5:
        st.subheader(":material/sports: Player Discipline")
        #df for discipine metrics
        disciplie_df=filtered_player_df[["player","cards_yellow","cards_red","fouls","fouled"]].copy()
        #show metrics
        col1,col2 =st.columns(2)
        with col1:
            st.metric( label="Yellow cards", value=int(disciplie_df.iloc[0]["cards_yellow"] ),
            border=True, icon=":material/crop_2_3:")

            st.metric( label="Red cards", value=int( disciplie_df.iloc[0]["cards_red"] ),
            border=True, icon=":material/crop_2_3:")    

        with col2:
            st.metric( label="Fouls committed", value=int( disciplie_df.iloc[0]["fouls"] ),
            border=True, icon=":material/sports:")
            
            st.metric( label="Fouls suffered", value=int( disciplie_df.iloc[0]["fouled"]),
            border=True, icon=":material/sports:")
 
        #plot bar chart cards: yellow vs red
        with st.container(border=True):
            st.header("Yellow cards vs Red cards")   
            st.bar_chart(
                disciplie_df,
                x="player",
                y=["cards_yellow","cards_red"],
                y_label="Cards",
                color=["yellow","red"],
                stack=False)
        
        #plot bar chart Fouls vs. fouled
        with st.container(border=True):
            st.header("Fouls vs Fouled")   
            st.bar_chart(
                disciplie_df,
                x="player",
                y=["fouls","fouled"],
                y_label="Cards",
                color=["orange","blue"],
                stack=False)
        
    #-------------------------------------------------------Team Impact--------------------------------------------
    with tab6:
        st.subheader(":material/diversity_3: Player Team Impact")
        #df for team impact metrics
        team_impact_df=filtered_player_df[["player","points_per_game","plus_minus","plus_minus_per90","plus_minus_wowy","on_goals_for","on_goals_against"]].copy()
        #show metrics
        col1,col2,col3=st.columns(3)
        with col1:
            st.metric( label="Points per game", value=team_impact_df.iloc[0]["points_per_game"],
            border=True, icon=":material/spoke:")

            st.metric( label="Plus/Minus WOWY", value=team_impact_df.iloc[0]["plus_minus_wowy"],
            border=True, icon=":material/unknown_2:")   

        with col2:
            st.metric( label="Plus/Minus", value=team_impact_df.iloc[0]["plus_minus"],
            border=True, icon=":material/unknown_2:")
            
            st.metric( label="Plus/Minus per 90", value=team_impact_df.iloc[0]["plus_minus_per90"],
            border=True, icon=":material/unknown_2:")

        with col3:
            st.metric( label="Goals for while on field", value=int( team_impact_df.iloc[0]["on_goals_for"] ),
            border=True, icon=":material/grass:")  

            st.metric( label="Goals against while on field", value=int( team_impact_df.iloc[0]["on_goals_against"] ),
            border=True, icon=":material/grass:") 
 
        #plot bar chart plus/minus 
        with st.container(border=True):
            st.header("Plus/Minus vs Plus/Minus WOWY")   
            st.bar_chart(
                team_impact_df,
                x="player",
                y=["plus_minus","plus_minus_wowy"],
                y_label="Plus/Minus",
                color=["orange","blue"],stack=False)

        #plot bar chart goals
        with st.container(border=True):
            st.header("Goals for vs Goals against while on field")   
            st.bar_chart(
                team_impact_df,
                x="player",
                y=["on_goals_for","on_goals_against"],
                y_label="Goals",
                color=["blue","violet"], stack=False)

    #-------------------------------------------------------Defensive Metrics---------------------------------
    with tab7:
        st.subheader(":material/shield: Player Defensive Metrics")
        #df for defense metrics
        defense_df=filtered_player_df[["player","tackles_won", "interceptions","pens_won","pens_conceded", "own_goals"]].copy()
        #show metrics
        col1,col2,col3=st.columns(3)
        with col1:
            st.metric( label="Tackles won", value=int( defense_df.iloc[0]["tackles_won"] ),
            border=True, icon=":material/cheer:")

            st.metric( label="Interceptions", value=int( defense_df.iloc[0]["interceptions"] ),
            border=True, icon=":material/cheer:")   

        with col2:
            st.metric( label="Penalties won", value=int( defense_df.iloc[0]["pens_won"]),
            border=True, icon=":material/sentiment_content:")
            
            st.metric( label="Penalties conceded", value=int( defense_df.iloc[0]["pens_conceded"] ),
            border=True, icon=":material/sentiment_dissatisfied:")

        with col3:
            st.metric(  label="Own goals", value=int( defense_df.iloc[0]["own_goals"] ),
            border=True, icon=":material/sports_and_outdoors:")  


        #plot bar chart Interceptions tackles
        with st.container(border=True):
            st.header("Interceptions vs Tackles Won")   
            st.bar_chart(
                defense_df,
                x="player",
                y=["interceptions","tackles_won"],
                y_label="interceptions and tackles",
                color=["violet","blue"],stack=False)

        #plot bar chart Penalties
        with st.container(border=True):
            st.header("Penalties won vs Penalties conceded")   
            st.bar_chart(
                defense_df,
                x="player",
                y=["pens_won","pens_conceded"],
                y_label="Penaties",
                color=["orange","blue"],stack=False)
        