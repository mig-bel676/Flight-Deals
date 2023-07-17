import requests

# Importing Twilio for SMS integration
from twilio.rest import Client
account_sid = "ACd4a57246f080e3ae542c65ffeaf7a514"
auth_token = "f9c0541d5e30766dff114fd1861ae02b"

# Getting data from sheets
API_Sheety_Get = "https://api.sheety.co/ba75963e38b670a666f64c92359f350b/copyOfFlightDeals/prices"
get_response = requests.get(url=API_Sheety_Get)
data = get_response.json()
google_sheet_data = data['prices']

# Placing Sheety data of city iataCode and lowestPrice into dictionary
data_dictionary = {}
for row in google_sheet_data:
    data_dictionary[row["iataCode"]] = row["lowestPrice"]

# Connecting to Tequila API and looping through Sheety data_dictionary to check if there is any deals on any of the
# cities that is listed in Google Sheet
for key in data_dictionary:
    Get_API_Endpoint = "https://api.tequila.kiwi.com/v2/search"
    API_KEY = "tBAwt_rfWWtKZwIZnhG_jaKFSX1c_bgG"
    HEADER = {
        "apikey": API_KEY,
    }
    # Query determines how I get the specific flight deals I am looking for
    query = {
        "fly_from": "LAX",
        "fly_to": key,
        "price_from": 0,
        "price_to": data_dictionary[key],
        "date_from": "17/07/2023", # UPDATE DATE DD/MM/YYYY
        "date_to": "17/07/2024", # UPDATE DATE DD/MM/YYYY
        "curr": "USD",
        "limit": 1,
    }

    response_flights = requests.get(url=Get_API_Endpoint, params=query, headers=HEADER)
    flights_data = response_flights.json()
    print(flights_data)
    # If there is a deal  send an SMS with city, departure date and time, price
    if flights_data["_results"] > 0:
        client = Client(account_sid, auth_token)
        destination_from = flights_data["data"][0]["cityFrom"]
        destination_to = flights_data["data"][0]["cityTo"]
        date_of_departure = flights_data["data"][0]["local_departure"]
        date_of_departure = date_of_departure[:10]
        deal_price = flights_data["data"][0]["price"]
        message = client.messages.create(
            body=f'\nFlight Deal! \n{destination_from} to {destination_to} '
                 f'\nPrice: ${deal_price} \nDeparts: {date_of_departure} '
                 f'\nBook It:https://tequila.kiwi.com/portal/docs/user_guides/booking_api__general_information_',
            from_='+15737314325',
            to='+15624450411'  # Recipients Phone Number
        )
