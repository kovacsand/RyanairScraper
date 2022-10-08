import json

from datetime import datetime
from datetime import timedelta

flights_data = []

start_day = datetime(2022, 10, 5)
today = datetime.today()
searched_day = start_day

while searched_day <= today:
    try:
        with open(f"C:/Users/kandr/PycharmProjects/RyanairScraper/flights_data/{searched_day.year}-"
                  f"{searched_day.month:02d}-{searched_day.day:02d}-BUD.json") as file:
            data = json.load(file)
        flights_data.append(data)
        searched_day += timedelta(days=1)
    except FileNotFoundError:
        searched_day += timedelta(days=1)
        continue


start_day = datetime(2022, 10, 5)
searched_day = start_day
last_day = datetime.today() + timedelta(days=180)

searched_flights = []
while searched_day <= last_day:
    searched_flight = []
    for index, data in enumerate(flights_data):
        for flight in data:
            found_day_strings = dict(flight).get("date").split(" ")[0].split("-")
            found_day = datetime(int(found_day_strings[0]), int(found_day_strings[1]), int(found_day_strings[2]))
            if found_day.date() == searched_day.date():
                searched_flight.append(dict(flight))
    if searched_flight:
        searched_flights.append(searched_flight)
    searched_day += timedelta(days=1)

print(searched_flights)

for day in searched_flights:
    print(day[0].get("date"))
    for flight in day:
        print(f"\t{flight.get('price')} - ")


