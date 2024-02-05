import connexion 
from connexion import NoContent 

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from hotel_room import HotelRoom
from hotel_activity import HotelActivity

import yaml 
import logging
import logging.config

with open('app_conf.yml', 'r') as f: 
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f: 
    log_config = yaml.safe_load(f.read()) 
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

# DB_ENGINE = create_engine("sqlite:///bookings.sqlite") # Connect to the database (db name: bookings.sqlite)
DB_ENGINE = create_engine(f'mysql+pymysql://{app_config["datastore"]["user"]}:{app_config["datastore"]["password"]}@{app_config["datastore"]["hostname"]}:{app_config["datastore"]["port"]}/{app_config["datastore"]["db"]}')

Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

def book_hotel_room(body):
    """ Receives a hotel room booking event """

    session = DB_SESSION() 

    hotel_room = HotelRoom(body["hotel_id"],
                           body["customer_id"],
                           body["room_id"],
                           body["room_type"],
                           body["num_of_people"],
                           body["check_in_date"],
                           body["check_out_date"],
                           body["timestamp"],
                           body["trace_id"])

    session.add(hotel_room)

    session.commit()
    session.close()

    logger.debug(f"Stored event Hotel Room Booking request with a trace id of {body['trace_id']}")

    return NoContent, 201


def book_hotel_activity(body):
    """ Receives a hotel activity reservation event """
    session = DB_SESSION() 

    hotel_activity = HotelActivity(body["hotel_id"],
                           body["customer_id"],
                           body["activity_id"],
                           body["activity_name"],
                           body["num_of_people"],
                           body["reservation_date"],
                           body["timestamp"],
                           body["trace_id"])

    session.add(hotel_activity)

    session.commit()
    session.close()

    logger.debug("Stored event Hotel Activity Booking request with a trace id of %s", body["trace_id"])

    return NoContent, 201

app = connexion.FlaskApp(__name__, specification_dir="")
app.add_api("openapi.yaml", strict_validation=True, validate_responses=True) 

if __name__ == "__main__":
    app.run(port=8090)

