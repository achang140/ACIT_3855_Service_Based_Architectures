import connexion 
from connexion import NoContent 
import requests
import yaml 
import logging
import logging.config
import uuid

with open('app_conf.yml', 'r') as f: 
    app_config = yaml.safe_load(f.read())

# event_one_url = app_config["eventstore1"] 
# event_two_url = app_config["eventstore2"] 

with open('log_conf.yml', 'r') as f: 
    log_config = yaml.safe_load(f.read()) 
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

def book_hotel_room(body):
    """ Receives a hotel room booking event """

    trace_id = uuid.uuid4()
    body["trace_id"] = str(trace_id)

    logger.info("Received event Hotel Room Booking request with a trace id of %s", body["trace_id"])

    headers = { "content-type": "application/json" }
    response = requests.post(app_config["eventstore1"]["url"], json=body, headers=headers) # requests.post(url=event_one_url, json=body, headers=headers)
    
    logger.info(f"Returned event Hotel Room Booking response (Id: ${body['trace_id']}) with status ${response.status_code}")

    return NoContent, response.status_code

def book_hotel_activity(body):
    """ Receives a hotel activity reservation event """

    trace_id = uuid.uuid4()
    body["trace_id"] = str(trace_id)


    logger.info("Received event Hotel Activity Booking request with a trace id of %s", body["trace_id"])

    headers = { "content-type": "application/json" }
    response = requests.post(app_config["eventstore2"]["url"], json=body, headers=headers) # requests.post(url=event_two_url, json=body, headers=headers)

    logger.info("Returned event Hotel Activity Booking response (Id: %s) with status %d", body["trace_id"], response.status_code)

    return NoContent, response.status_code


app = connexion.FlaskApp(__name__, specification_dir="")
app.add_api("openapi.yaml", 
            strict_validation=True, 
            validate_responses=True) 

if __name__ == "__main__":
    app.run(port=8080)

