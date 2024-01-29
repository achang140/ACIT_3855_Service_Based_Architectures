import connexion 
from connexion import NoContent 

import requests


def book_hotel_room(body):
    """ Receives a hotel room booking event """

    headers = { "content-type": "application/json" }
    response = requests.post(url="http://localhost:8090/booking/hotel-rooms", json=body, headers=headers)

    return NoContent, response.status_code


def book_hotel_activity(body):
    """ Receives a hotel activity reservation event """
    
    headers = { "content-type": "application/json" }
    response = requests.post(url="http://127.0.0.1:8090/booking/hotel-activities", json=body, headers=headers)

    return NoContent, response.status_code


app = connexion.FlaskApp(__name__, specification_dir="")
app.add_api("openapi.yaml", 
            strict_validation=True, 
            validate_responses=True) 

if __name__ == "__main__":
    app.run(port=8080)
