import connexion 
from connexion import NoContent 
import json 
import os 
from datetime import datetime 

EVENT_FILE = "events.json"
MAX_EVENTS = 5 

def book_hotel_room(body):
    """ Receives a hotel room booking event """

    event_count = "hotel_room_count"
    event_type = "recent_hotel_room_reservation"

    customer_id = body["customer_id"]
    room_type = body["room_type"]

    new_event = {
        'received_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
        'msg_data': f"Customer ID:{customer_id}, Room Type: {room_type}"
    }

    if os.path.isfile(EVENT_FILE):
        with open(EVENT_FILE, "r") as file:
            events = json.load(file)
        
        events[event_count] += 1 

        events[event_type] = [new_event] + events[event_type][:MAX_EVENTS-1]

        with open(EVENT_FILE, "w") as file:
            json.dump(events, file, indent=2)

    else:
        data = {
            event_count: 1, 
            event_type: [new_event],
            "hotel_activity_count": 0,
            "recent_hotel_activity_reservation": []
        }

        with open(EVENT_FILE, "w") as file:
            json.dump(data, file, indent=2)

    return NoContent, 201


def book_hotel_activity(body):
    """ Receives a hotel activity reservation event """
    
    event_count = "hotel_activity_count"
    event_type = "recent_hotel_activity_reservation"

    customer_id = body["customer_id"]
    activity_name = body["activity_name"]

    new_event = {
        'received_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
        'msg_data': f"Customer ID:{customer_id}, Activity Name: {activity_name}"
    }

    if os.path.isfile(EVENT_FILE):
        with open(EVENT_FILE, "r") as file:
            events = json.load(file)

            events[event_count] += 1 

            events[event_type] = [new_event] + events[event_type][:MAX_EVENTS-1]

            with open(EVENT_FILE, "w") as file:
                json.dump(events, file, indent=2)

    else: 
        data = {
            "hotel_room_count": 0, 
            "recent_hotel_room_reservation": [],
            event_count: 1, 
            event_type: [new_event]
        }

        with open(EVENT_FILE, "w") as file:
            json.dump(data, file, indent=2)


    return NoContent, 201


app = connexion.FlaskApp(__name__, specification_dir="")
app.add_api("openapi.yaml", 
            strict_validation=True, 
            validate_responses=True) 

if __name__ == "__main__":
    app.run(port=8080)

