import streamlit as st
import pandas as pd

st.title("GOALKEEPERS")

@st.cache_data
def load_data():
    df=pd.read_csv("datasets/players.csv")
    return df

df=load_data()
st.dataframe(df)

#most Saves
# Save %
# most Clean sheets
# Goals conceded per 90
# Penalty saves


#KPIs
#Saves
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
