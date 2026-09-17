import streamlit as st
import pandas as pd

st.title(":material/front_hand: GOALKEEPERS")

@st.cache_data
def load_data():
    df=pd.read_csv("datasets/players.csv")
    df = df[df["position"] == "GK"]
    return df

df=load_data()
st.dataframe(df)
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

        

#--------------------------------------------player---------------------------------
with p2:
    with st.container(border=True):
        st.subheader(":material/person: Tournament Goalkeeper's Info")

        gk_list = filtered_gks["player"].unique().tolist()
        selected_gk = st.selectbox("Select player", gk_list)
        filtered_gk_data = filtered_gks[filtered_gks["player"] == selected_gk]

        st.dataframe(filtered_gk_data)


#total saves on tournament
#most Saves
#Save %
#Goals against
#Goals against per 90
#Clean sheets
#Clean sheet %
#Penalty save %
#Charts
#Save %
#Clean sheets
#Saves vs. goals conceded
