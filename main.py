#Formula 1 Race Telemetry Viewer

#Will be utilizing the FastF1 API to fetch and display race info.

#Objective for now: Improve the app's UI; add more features.

#Possible starting features to implement could include simply fetching and displaying next session times, and possibly a countdown until said times.

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
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

st.header(current_event['EventName'], text_alignment="left")

st.subheader(
    "Race Date: " + str(current_event['EventDate'].date()) , text_alignment="left"
)

gp = current_event['EventName']
event = 'Race'

last_session_year = current_year - 1

print(fastf1.get_event_schedule(last_session_year).get_event_by_name(gp)['EventName'])

while True: #Until a match is found, check previous season schedules for the GP's event name.
    if gp in fastf1.get_event_schedule(last_session_year)['EventName'].values:
        break
    else:
        last_session_year -= 1

st.subheader("Last Time Around", text_alignment="right")

session_event = fastf1.get_session((last_session_year), gp, event)
session_event.load(
    laps=True,
    telemetry=True,
    weather=False,
    messages=False,
    ) #Avoid heavy session loading and load only needed data for plotting track layout and driver positions.

circuit_info = session_event.get_circuit_info()
lap = session_event.laps.pick_fastest()
pos = lap.get_pos_data()

fig, ax = plt.subplots(figsize=(10,5))

def rotate(xy, *, angle):
    rot_mat = np.array([[np.cos(angle), np.sin(angle)],
                        [-np.sin(angle), np.cos(angle)]])
    return np.matmul(xy, rot_mat)

track = pos.loc[:, ('X', 'Y')].to_numpy()

track_angle = circuit_info.rotation / 180 * np.pi

offset_vector = [500, 0]  

rotated_track = rotate(track, angle=track_angle)
plt.plot(rotated_track[:, 0], rotated_track[:, 1], color ='tab:red')
fig.patch.set_alpha(0.0)
ax.patch.set_alpha(0.0)
#plot_title = f"{year} | {gp} | {session_event.event['Location']} "

#plt.title(plot_title, fontsize = 10, color ='white')
plt.xticks([])
plt.yticks([])
plt.axis('equal')
for spine in ax.spines.values():
    spine.set_alpha(0)

col1, col2, col3 = st.columns([1, 4, 0.8])

with col2:
    st.pyplot(plt) #Plot the track layout on the app's page


starting_position = [int(x) for x in session_event.results['GridPosition']]
final_position = [int(x) for x in session_event.results['Position']] #These two variables have to be declared and converted outside of the table since they return float by default.


with col3: #Plot last time's driver positions in a table
    st.table(
        data={
        "Driver": session_event.results['Abbreviation'],
        "Final Position": final_position,
        "Starting Position": starting_position
        }
    )

