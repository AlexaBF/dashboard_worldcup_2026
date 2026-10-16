import streamlit as st
import pandas as pd
import plotly.express as px

st.title(":material/front_hand: GOALKEEPERS")

@st.cache_data
def load_data():
    df=pd.read_csv("datasets/players.csv")
    df = df[df["position"] == "GK"]
    return df
#df only with goalkeepers
df=load_data()

def get_gk_with_most(the_most,dataframe):
    best_num=dataframe[the_most].max()
    best_players=dataframe.loc[ dataframe[the_most] == best_num, "player" ].tolist() 
    best_player = ", ".join(best_players)

    return best_num, best_player

#most saves
max_gk_saves, max_gk_saves_player= get_gk_with_most("gk_saves",df)
#most clean sheets
max_gk_clean_sheets, max_gk_clean_sheets_player = get_gk_with_most("gk_clean_sheets",df)
#total saves on tournament
total_saves=int (df["gk_saves"].sum() )
total_gk=int( len(df) )

#overview gk metrics 
col1,col2=st.columns(2)
with col1:
    st.metric(label="Total saves on tournament",value=total_saves, border=True, icon=":material/back_hand:")   
    
    st.metric(label="Most clean sheets",value=max_gk_clean_sheets_player,
    delta=f"Count: {max_gk_clean_sheets:.0f}",
    delta_arrow="off", delta_color="green",
    border=True, icon=":material/person_check:")

with col2: 
    st.metric(label="Amount of Goalkeepers",value=total_gk, border=True, icon=":material/person:")

    st.metric(label="Most saves",value=max_gk_saves_player,
    delta= f"Saves: {max_gk_saves:.0f}",
    delta_arrow="off", delta_color="green",
    border=True, icon=":material/person_shield:")
st.divider()

st.header(":material/group_search: Goalkeeper overview")

#team filter
teams_selected = st.multiselect(":material/filter_alt: Select Teams", df["team"].unique(), default=df["team"].unique())
filtered_gks = df[df["team"].isin(teams_selected)]
#choose at least 1
if len(teams_selected)<1:
    st.warning("Select at least one team")
    st.stop()

#tabs for all goalkeepers or just one
p1,p2 = st.tabs([":material/groups: Players",":material/person: Player"])
#--------------------------------------------players---------------------------------
with p1:
    with st.container(border=True):
        st.subheader(":material/groups: Tournament Goalkeepers Info")
        
        #select only the gks with playing minutes
        gk_with_minutes=filtered_gks[filtered_gks["minutes"]>0].copy()

        #plot bar chart with save %
        with st.container(border=True):
            st.subheader("Save %")
            st.bar_chart(
                gk_with_minutes,
                x="player",
                y="gk_save_pct",
                x_label="Goalkeeper",
                y_label="Save %",
                sort="-gk_save_pct")

        #scatter chart for saves vs goals conceded
        fig_save_goals_conceded=px.scatter(
            gk_with_minutes,
            x="gk_goals_against",
            y="gk_saves",
            labels={
                "gk_goals_against":"Goals Conceded",
                "gk_saves":"Saves",
                "player":"Goalkeeper",
                "minutes":"Minutes"
            },hover_data={
                "gk_goals_against":True,
                "gk_saves":True,
                "player":True,
                "minutes":True
            },size="minutes",
            color="player"
        )
        #plot chart for saves vs goals conceded
        with st.container(border=True):
            st.subheader("Saves vs Goals Conceded")
            st.plotly_chart(fig_save_goals_conceded)

        #scatter chart for saves vs goals conceded
        fig_clean_sheets =px.scatter(
            gk_with_minutes,
            x="minutes",
            y="gk_clean_sheets",
            labels={
                "minutes":"Minutes",
                "gk_clean_sheets":"Clean Sheets",
                "player":"Goalkeeper"
            },
            color="player" 
        )
        #resize the scatter dots
        fig_clean_sheets.update_traces(marker_size=15)
        #plot chart for saves vs goals conceded
        with st.container(border=True):
            st.subheader("Clean Sheets")
            st.plotly_chart(fig_clean_sheets)
            
        #scatter chart for saves vs goals conceded
        fig_clean_sheets_percent =px.scatter(
            gk_with_minutes,
            x="minutes",
            y="gk_clean_sheets_pct",
            labels={
                "minutes":"Minutes",
                "gk_clean_sheets_pct":"Clean Sheets %",
                "player":"Goalkeeper"
            },
            size="minutes",
            color="player" 
        )
        #plot chart for saves vs goals conceded
        with st.container(border=True):
            st.subheader("Clean Sheets %")
            st.plotly_chart(fig_clean_sheets_percent) 

#--------------------------------------------player---------------------------------
with p2:
    with st.container(border=True):
        st.subheader(":material/person: Tournament Goalkeeper's Info")
        
        #list of gks
        gk_list = filtered_gks["player"].unique().tolist()
        selected_gk = st.selectbox(":material/filter_alt: Select player", gk_list)

        #df of selected gk
        filtered_gk_data = filtered_gks[filtered_gks["player"] == selected_gk]

        #player/gk info
        col1,col2=st.columns(2)
        with col1:
            st.metric( label="Player", value=filtered_gk_data.iloc[0]["player"],
            border=True, icon=":material/person:")

            st.metric( label="Age", value=filtered_gk_data.iloc[0]["age"],
            border=True, icon=":material/calendar_today:")
        
        with col2:
            st.metric(label="Team", value=filtered_gk_data.iloc[0]["team"],
            border=True, icon=":material/flag:")

            st.metric(label="Club", value=filtered_gk_data.iloc[0]["club"],
            border=True, icon=":material/groups:")

            
        tab1,tab2,tab3=st.tabs([":material/sports_and_outdoors: Games", ":material/sports_handball: Saves",":material/sports: Disclipline"])
        #games tab
        with tab1:
            col1,col2=st.columns(2)
            with col1:
                st.metric(label="Games Played", value=filtered_gk_data.iloc[0]["games"],
                border=True, icon=":material/groups:")

                st.metric(label="Games as a starter", value=filtered_gk_data.iloc[0]["games_starts"],
                border=True, icon=":material/groups:")
            with col2:
                st.metric(label="Clean sheets", value=int( filtered_gk_data.iloc[0]["gk_clean_sheets"] ),
                border=True, icon=":material/groups:")
                
                st.metric(label="Clean sheet %", value=filtered_gk_data.iloc[0]["gk_clean_sheets_pct"],
                border=True, icon=":material/groups:")
            
            #plot bar chartgames played and clean sheets
            with st.container(border=True):
                st.subheader("Games played and Clean sheets")
                st.bar_chart(
                    filtered_gk_data,
                    x="player",
                    x_label="Goalkeeper",
                    y=["gk_clean_sheets","games"],
                    stack=False,
                    color=["orange","blue"])

        #saves tab
        with tab2:
            col1,col2,col3=st.columns(3)
            with col1:
                st.metric(label="Total Saves", value=int( filtered_gk_data.iloc[0]["gk_saves"] ),
                border=True, icon=":material/groups:")

                st.metric(label="Save %", value=filtered_gk_data.iloc[0]["gk_save_pct"],
                border=True, icon=":material/groups:")

            with col2:   
                st.metric(label="Goals against per 90", value=filtered_gk_data.iloc[0]["gk_goals_against_per90"],
                border=True, icon=":material/groups:")

                st.metric(label="Goals conceded", value=int( filtered_gk_data.iloc[0]["gk_goals_against"] ),
                border=True, icon=":material/groups:")

            with col3:
                st.metric(label="Penalties faced", value=int( filtered_gk_data.iloc[0]["gk_pens_att"]),
                border=True, icon=":material/groups:")

                st.metric(label="Penalty save %", value=filtered_gk_data.iloc[0]["gk_pens_save_pct"],
                border=True, icon=":material/groups:")
        
            #plot bar chart saves and goals
            with st.container(border=True):
                st.subheader("Saves vs Goals conceded")
                st.bar_chart(
                    filtered_gk_data,
                    x="player",
                    x_label="Goalkeeper",
                    y=["gk_saves","gk_goals_against"],
                    stack=False,
                    color=["orange","grey"])

            #plot bar chart penalty saved and conceded
            with st.container(border=True):
                st.subheader("Penalty saved vs conceded")
                st.bar_chart(
                    filtered_gk_data,
                    x="player",
                    x_label="Goalkeeper",
                    y=["gk_pens_saved","gk_pens_allowed"],
                    stack=False,
                    color=["violet","blue"])
            
            #plot bar chart for Save % vs Peanlty save %
            with st.container(border=True):
                st.subheader("Save % vs Peanlty save %")
                st.bar_chart(
                    filtered_gk_data,
                    x="player",
                    x_label="Goalkeeper",
                    y=["gk_save_pct","gk_pens_save_pct"],
                    y_label="%",
                    stack=False,
                    color=["#FF4B4B", "#1F77B4"])

        #discipline tab
        with tab3:
            col1,col2=st.columns(2)
            with col1:
                st.metric( label="Red Cards", value=int( filtered_gk_data.iloc[0]["cards_red"] ),
                border=True, icon=":material/crop_2_3:")

                st.metric( label="Yellow Cards", value=int( filtered_gk_data.iloc[0]["cards_yellow"] ),
                border=True, icon=":material/crop_2_3:")

            with col2:
                st.metric( label="Fouls committed", value=int( filtered_gk_data.iloc[0]["fouls"] ),
                border=True, icon=":material/sports:")

                st.metric( label="Fouls suffered", value=int( filtered_gk_data.iloc[0]["fouled"] ),
                border=True, icon=":material/sports:")

            #plot bar chart fouls committed  vs suffered
            with st.container(border=True):
                st.subheader("Fouls committed  vs suffered")
                st.bar_chart(
                    filtered_gk_data,
                    x="player",
                    x_label="Goalkeeper",
                    y=["fouls","fouled"],
                    stack=False,
                    color=["#b36966","#66b387"])
            
            #plot bar chart cards
            with st.container(border=True):
                st.subheader("Red cards vs Yellow cards")
                st.bar_chart(
                    filtered_gk_data,
                    x="player",
                    x_label="Goalkeeper",
                    y=["cards_red","cards_yellow"],
                    stack=False,
                    color=["red","yellow"])
