import streamlit as st
import pandas as pd

st.title(":material/map: VENUES")

@st.cache_data
def load_data():
    df = pd.read_csv("datasets/matches.csv")
    venues = df[["round", "attendance", "venue"]].copy()
    venues["attendance"] = (venues["attendance"].str.replace(",", "").astype(int))
    return venues

@st.cache_data
def load_locations():
    return pd.read_csv("datasets/venues_locations.csv")

#df for venues
df=load_data()
locations=load_locations()

#total venues
total_venues=df["venue"].value_counts().reset_index()
total_venues.columns=["Venue","Count"]
# Attendance
avg_attendance=df["attendance"].mean()
#max attendance and the venue
max_attendance=df["attendance"].max()
max_attendance_venues = df.loc[df["attendance"] == max_attendance, "venue"]
max_attendance_venues= max_attendance_venues.unique()
#min attendance and the venue
min_attendance=df["attendance"].min()
min_attendance_venues = df.loc[df["attendance"] == min_attendance, "venue"]
min_attendance_venues= min_attendance_venues.unique()
#the percentage change in attendance
max_change=(max_attendance-avg_attendance)/avg_attendance*100
min_change=(min_attendance-avg_attendance)/avg_attendance*100

#show metrics
t_venue1, t_venue2 = st.columns(2)
with t_venue1:
    st.metric( label="Total Venues",value=len(total_venues), border=True, icon=":material/stadium:")
with t_venue2:
    st.metric(label="Host Countries", value="CANADA , MÉXICO, USA", border=True, icon=":material/globe_location_pin:")

#attendance overview
st.divider()
st.header(":material/crowdsource: Attendance")
a_venue1, a_venue2,a_venue3 = st.columns(3)
with a_venue1:
    st.metric("Min Attendance", f"{min_attendance:,.0f}", 
    border=True, icon=":material/event_seat:", 
    delta=f"{min_change:.2f}%", delta_color="red", delta_arrow="down")

with a_venue2:
    st.metric("Average Attendance", f"{avg_attendance:,.0f}", 
    border=True, icon=":material/event_seat:", 
    delta="average",delta_color="off", delta_arrow="off")

with a_venue3:
    st.metric("Max Attendance", f"{max_attendance:,.0f}",
    border=True, icon=":material/event_seat:",
    delta=f"{max_change:.2f}%")

#popular venues
st.divider()
st.header(":material/star_shine: Standout Venues")
venues1, venues2 = st.columns(2)
with venues1:
    st.metric(label="Venue with Least matches",value=total_venues["Venue"].iloc[-1], 
    border=True, icon=":material/stadium:")

    st.metric(label="Venue with Least Attendance",value=min_attendance_venues[0],
    border=True, icon=":material/stadium:")

with venues2:
    st.metric(label="Venue with Most matches",value=total_venues["Venue"][0],
    border=True, icon=":material/stadium:")

    st.metric(label="Venue with Max Attendance",value=max_attendance_venues[0], 
    border=True, icon=":material/stadium:")

st.divider()
st.header(":material/location_on: Venue Locations")

with st.container(border=True):
    #filter country
    country = st.selectbox(":material/filter_alt: Select a country",["All"] + sorted(locations["country"].unique()))
    if country != "All":
        filtered_locations = locations[ locations["country"]==country ]
    else:
        filtered_locations = locations

    city = st.selectbox( ":material/filter_alt: Select a city", ["All"] + sorted(filtered_locations["city"].unique()))
    if city != "All":
        filtered_locations = filtered_locations[ filtered_locations["city"]==city ]

    map_venue = filtered_locations.rename( columns={ "lat": "latitude", "lon": "longitude"} )
    st.caption(f"Showing {len(filtered_locations)} venue locations")
    st.map(map_venue)
