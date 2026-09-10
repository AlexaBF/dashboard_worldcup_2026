import streamlit as st

st.set_page_config(page_title="World Cup 2026 Analytics", layout="wide")

page_1 = st.Page( "pages/1_Overview.py", title="Overview", icon=":material/search_insights:" )
page_2 = st.Page( "pages/2_Matches.py", title="Matches", icon=":material/scoreboard:" )
page_3 = st.Page( "pages/3_Teams.py", title="Teams", icon=":material/groups:" )
page_4 = st.Page( "pages/4_Players.py", title="Players", icon=":material/person:" )
page_5 = st.Page( "pages/5_Goalkeepers.py", title="Goalkeepers", icon=":material/pan_tool:" )
page_6 = st.Page( "pages/6_Venues.py", title="Venues", icon=":material/stadium:" )

pg = st.navigation([page_1,page_2, page_3,page_4,page_5,page_6])

pg.run()