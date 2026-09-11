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

st.header(":material/group_search: Goalkeeper overview")

col1,col2,col3=st.columns(3)

with col1:
    #total saves on tournament
    st.text("total saves on tournament")
    
with col2: 
    #""""""
    st.text("goalkeeper with most saves")
with col3:
    #"""player with most clean sheets"""
    st.text("goalkeeper with most clean sheets")
    
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
