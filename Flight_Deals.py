import requests
from twilio.rest import Client


class FlightDeals:
    def __init__(self):
        self.account_sid = "ACd4a57246f080e3ae542c65ffeaf7a514"
        self.auth_token = "f9c0541d5e30766dff114fd1861ae02b"
        self.client = Client(self.account_sid, self.auth_token)

    def get_data_from_sheets(self):
        API_Sheety_Get = "https://api.sheety.co/ba75963e38b670a666f64c92359f350b/copyOfFlightDeals/prices"
        get_response = requests.get(url=API_Sheety_Get)
        data = get_response.json()
        google_sheet_data = data['prices']

        # Placing Sheety data of city iataCode and lowestPrice into dictionary
        self.data_dictionary = {}
        for row in google_sheet_data:
            self.data_dictionary[row["iataCode"]] = row["lowestPrice"]

    def check_deals(self):
        # Connecting to Tequila API and looping through Sheety data_dictionary to check if there is any deals on any of the
        # cities that is listed in Google Sheet
        for key in self.data_dictionary:
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
                "price_to": self.data_dictionary[key],
                "date_from": "21/01/2023",
                "date_to": "21/07/2023",
                "curr": "USD",
                "limit": 1,
            }

            response_flights = requests.get(url=Get_API_Endpoint, params=query, headers=HEADER)
            flights_data = response_flights.json()
            # If there is a deal  send an SMS with city, departure date and time, price
            if flights_data["_results"] > 0:
                self.send_sms(flights_data)

