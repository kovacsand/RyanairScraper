# This is my python application to scrape Ryanair's website for prices
import json
import time

from datetime import datetime
from datetime import timedelta

from ryanair import Ryanair

BILLUND_AIRPORT_CODE = "BLL"
BUDAPEST_AIRPORT_CODE = "BUD"
DENMARK_COUNTRY_CODE = "DK"
HUNGARY_COUNTRY_CODE = "HU"

ryanair = Ryanair("DKK")


# True, if going to BUD (Hungary), false if going to BLL (Denmark)
def request_flights(to_bud):
    # I am not sure, how many days ahead can I see flights to Budapest, so I decided that it is going to be 180 days,
    # because that is close to my observations
    # Another method would be checking for consecutive emtpy results from the
    # queries, but again, after hwo many days should I conclude that the flights are not planned yet for those period
    today = datetime.today()
    searched_day = today
    last_day = today + timedelta(days=180)

    if to_bud:
        origin_airport_code = BILLUND_AIRPORT_CODE
        destination_country_code = HUNGARY_COUNTRY_CODE
    else:
        origin_airport_code = BUDAPEST_AIRPORT_CODE
        destination_country_code = DENMARK_COUNTRY_CODE

    flights_info = []

    while searched_day < last_day:
        flight = ryanair.get_flights(
            origin_airport_code, f"{searched_day.year}-{searched_day.month:02d}-{searched_day.day:02d}",
            f"{searched_day.year}-{searched_day.month:02d}-{searched_day.day:02d}", destination_country_code)
        if flight:
            flight_info = {"date": str(flight[0].departureTime), "price": str(flight[0].price)}
            flights_info.append(flight_info)
        searched_day += timedelta(days=1)

    print(f"Searched flights until {last_day.year}-{last_day.month:02d}-{last_day.day:02d}")

    return flights_info


def write_flights(to_bud, flights):
    today = datetime.today()
    json_object = json.dumps(flights, indent=2)
    with open(f"C:/Users/kandr/PycharmProjects/RyanairScraper/flights_data/{today.year}-"
              f"{today.month:02d}-{today.day:02d}-{'BUD' if to_bud else 'BLL'}.json", "w") as outfile:
        outfile.write(json_object)


def scrape_flights(to_bud):
    print("Starting scraping")
    start_time = time.perf_counter()
    flights = request_flights(to_bud)
    finish_time = time.perf_counter()
    print(f"Scraping took {finish_time - start_time:.2f} seconds")

    print(f"Writing to file now")
    write_flights(to_bud, flights)
    print(f"Writing to file done")


scrape_flights(True)
scrape_flights(False)
