#Formula 1 Race Telemetry Viewer

#Will be utilizing the FastF1 API to fetch and display race info.

#Objective for now: Initialize and develop the app's GUI to display intended features and information.

#Possible starting features to implement could include simply fetching and displaying next session times, and possibly a countdown until said times.

import pandas as pd
import fastf1 #Starting by importing the fastf1 API.
import time
from datetime import date #Importing date for fetching the current year's schedules and session times.
import streamlit as st


current_year = date.today().year #Fetch current year
schedule = fastf1.get_event_schedule(current_year) #Fetch current year's schedule
current_date = date.today()

current_round = 1


while schedule.get_event_by_round(current_round)['EventDate'] < pd.Timestamp(current_date):
    current_round +=1

current_event = schedule.get_event_by_round(current_round)  #Fetch current round's information by incrementing round number until event date is greater than or equal to the current date.

  

st.set_page_config(layout="wide")

st.title("Formula 1 Race Monitor", text_alignment="center")

st.header(

current_event['EventName'], text_alignment="left"
    
)

st.subheader(
    "Race Date: " + str(current_event['EventDate'].date()) , text_alignment="left"
)
