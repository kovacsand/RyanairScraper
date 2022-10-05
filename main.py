# This is my python application to scrape Ryanair's website for prices
import json
import time

from datetime import datetime
from datetime import timedelta

from ryanair import Ryanair

BILLUND_AIRPORT_CODE = "BLL"
HUNGARY_COUNTRY_CODE = "HU"

ryanair = Ryanair("DKK")

today = datetime.today()
searched_day = today
# I am not sure, how many days ahead can I see flights to Budapest, so I decided that it is going to be 180 days,
# because that is close to my observations
# Another method would be checking for consecutive emtpy results from the
# queries, but again, after hwo many days should I conclude that the flights are not planned yet for those period
last_day = today + timedelta(days=180)

flights_info = []

print("Starting scraping")
start_time = time.perf_counter()

while searched_day < last_day:
    flight = ryanair.get_flights(
        BILLUND_AIRPORT_CODE, f"{searched_day.year}-{searched_day.month:02d}-{searched_day.day:02d}",
        f"{searched_day.year}-{searched_day.month:02d}-{searched_day.day:02d}", HUNGARY_COUNTRY_CODE)
    if flight:
        flight_info = {"date": str(flight[0].departureTime), "price": str(flight[0].price)}
        flights_info.append(flight_info)
    searched_day += timedelta(days=1)

finish_time = time.perf_counter()
print(f"Searched flights until {last_day.year}-{last_day.month:02d}-{last_day.day:02d}"
      f"\nScraping took {finish_time - start_time:.2f} seconds"
      f"\nWriting to file now")

json_object = json.dumps(flights_info, indent=2)
with open("C:/Users/kandr/PycharmProjects/RyanairScraper/flights_data/"
          f"{today.year}-{today.month:02d}-{today.day:02d}.json", "w") as outfile:
    outfile.write(json_object)
print(f"Writing to file done")
