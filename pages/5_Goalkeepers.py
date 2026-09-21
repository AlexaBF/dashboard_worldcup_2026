import streamlit as st
import pandas as pd

st.title(":material/front_hand: GOALKEEPERS")

@st.cache_data
def load_data():
    df=pd.read_csv("datasets/players.csv")
    df = df[df["position"] == "GK"]
    return df

df=load_data()
#st.dataframe(df)
#print(df.info())


col1,col2=st.columns(2)

#total saves on tournament
total_saves=int (df["gk_saves"].sum() )
total_gk=int( len(df) )

#most saves
#max_gk_saves=int(df["gk_saves"].max())
#max_gk_saves_player=df.loc[ df["gk_saves"] == max_gc, "player" ].iloc[0]
max_gk_saves=df["gk_saves"].max()
max_gk_saves_players=df.loc[ df["gk_saves"] == max_gk_saves, "player" ].tolist() 
max_gk_saves_player = ", ".join(max_gk_saves_players)

#most clean sheets
max_gk_clean_sheets=df["gk_clean_sheets"].max()
max_gk_clean_sheets_players=df.loc[ df["gk_clean_sheets"] == max_gk_clean_sheets, "player" ].tolist() 
max_gk_clean_sheets_player = ", ".join(max_gk_clean_sheets_players)

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

#st.dataframe(filtered_gks)


p1,p2 = st.tabs([":material/groups: Players",":material/person: Player"])
#--------------------------------------------players---------------------------------
with p1:
    with st.container(border=True):
        st.subheader(":material/groups: Tournament Goalkeepers Info")

        bar=filtered_gks[filtered_gks["minutes"]>0].copy()
        with st.container(border=True):
            st.subheader("Save %")
            st.bar_chart(
                bar,
                x="player",
                y="gk_save_pct",
                x_label="Player",
                y_label="Save %",
                sort="-gk_save_pct")

        with st.container(border=True):
            st.subheader("Saves vs Goals Conceded")
            st.scatter_chart(
                filtered_gks,
                x="gk_goals_against",
                y="gk_saves",
                x_label="Goals Conceded",
                y_label="Saves",
                size="minutes",
                color="player")


        with st.container(border=True):
            st.subheader("Clean Sheets")
            st.scatter_chart(
                filtered_gks,
                x="minutes",
                y="gk_clean_sheets",
                x_label="Minutes Played",
                y_label="Clean Sheets",
                size=100,
                color="player")
        
        with st.container(border=True):
            st.subheader("Clean Sheets %")
            st.scatter_chart(
                filtered_gks,
                x="minutes",
                y="gk_clean_sheets_pct",
                x_label="Minutes Played",
                y_label="Clean Sheets %",
                size=100,
                color="player")

        

#--------------------------------------------player---------------------------------
with p2:
    with st.container(border=True):
        st.subheader(":material/person: Tournament Goalkeeper's Info")

        gk_list = filtered_gks["player"].unique().tolist()
        selected_gk = st.selectbox("Select player", gk_list)
        filtered_gk_data = filtered_gks[filtered_gks["player"] == selected_gk]

        st.dataframe(filtered_gk_data)

        col1,col2=st.columns(2)
        with col1:
            st.metric(label="Player",
            value=filtered_gk_data.iloc[0]["player"],
            border=True,
            icon=":material/person:")


            st.metric(label="Age",
            value=filtered_gk_data.iloc[0]["age"],
            border=True,
            icon=":material/calendar_today:")
        

        with col2:
            st.metric(label="Team",
            value=filtered_gk_data.iloc[0]["team"],
            border=True,
            icon=":material/flag:")

            st.metric(label="Club",
            value=filtered_gk_data.iloc[0]["club"],
            border=True,
            icon=":material/groups:")

            
        tab1,tab2,tab3=st.tabs([":material/sports_and_outdoors: Games", ":material/sports_handball: Saves",":material/sports: Disclipline"])
        with tab1:
            col1,col2=st.columns(2)
            with col1:
                st.metric(label="Games Played",
                value=filtered_gk_data.iloc[0]["games"],
                border=True,
                icon=":material/groups:")

                st.metric(label="Games as a starter",
                value=filtered_gk_data.iloc[0]["games_starts"],
                border=True,
                icon=":material/groups:")
            with col2:
                st.metric(label="Clean sheets",
                value=int( filtered_gk_data.iloc[0]["gk_clean_sheets"] ),
                border=True,
                icon=":material/groups:")
                
                st.metric(label="Clean sheet %",
                value=filtered_gk_data.iloc[0]["gk_clean_sheets_pct"],
                border=True,
                icon=":material/groups:")


        with tab2:
            col1,col2,col3=st.columns(3)
            with col1:
                st.metric(label="Total Saves",
                value=int( filtered_gk_data.iloc[0]["gk_saves"] ),
                border=True,
                icon=":material/groups:")

                st.metric(label="Save %",
                value=filtered_gk_data.iloc[0]["gk_save_pct"],
                border=True,
                icon=":material/groups:")

            with col2:   
                st.metric(label="Goals against per 90",
                value=filtered_gk_data.iloc[0]["gk_goals_against_per90"],
                border=True,
                icon=":material/groups:")

                st.metric(label="Goals against",
                value=int( filtered_gk_data.iloc[0]["gk_goals_against"] ),
                border=True,
                icon=":material/groups:")

            with col3:
                st.metric(label="Penalties faced",
                value=int( filtered_gk_data.iloc[0]["gk_pens_att"]),
                border=True,
                icon=":material/groups:")

                st.metric(label="Penalty save %",
                value=filtered_gk_data.iloc[0]["gk_pens_save_pct"],
                border=True,
                icon=":material/groups:")


        with tab3:
            col1,col2=st.columns(2)
            with col1:
                st.metric(label="Red Cards",
                value=int( filtered_gk_data.iloc[0]["cards_red"] ),
                border=True,
                icon=":material/crop_2_3:")

                st.metric(label="Yellow Cards",
                value=int( filtered_gk_data.iloc[0]["cards_yellow"] ),
                border=True,
                icon=":material/crop_2_3:")

            with col2:
                st.metric(label="Fouls committed",
                value=int( filtered_gk_data.iloc[0]["fouls"] ),
                border=True,
                icon=":material/sports:")

                st.metric(label="Fouls suffered",
                value=int( filtered_gk_data.iloc[0]["fouled"] ),
                border=True,
                icon=":material/sports:")


        
