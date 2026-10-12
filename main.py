#Formula 1 Race Telemetry Viewer
#Some sample code for now before I can get an idea of what to put down here.
#Will be utilizing the FastF1 API to fetch and display race info.

#Objective for now: just get something to start it off. Probably a safe bet is to just get something basic for now and build off of it later.

#Possible starting features to implement could include simply fetching and displaying next session times, and possibly a countdown until said times.

import fastf1 #Starting by importing the fastf1 API.

from datetime import date #Importing date for fetching the current year's schedules and session times.

current_year = date.today().year #Fetch current year

schedule = fastf1.get_event_schedule(current_year) #Fetch current year's schedule

print(schedule) #Print fetched F1 race schedule

