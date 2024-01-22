import connexion 
from connexion import NoContent 

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from hotel_room import HotelRoom
from hotel_activity import HotelActivity
import datetime

DB_ENGINE = create_engine("sqlite:///bookings.sqlite") # Connect to the database (name of the database)
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
                           body["timestamp"])

    session.add(hotel_room)

    session.commit()
    session.close()

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
                           body["timestamp"])

    session.add(hotel_activity)

    session.commit()
    session.close()

    return NoContent, 201

app = connexion.FlaskApp(__name__, specification_dir="")
app.add_api("openapi.yaml", strict_validation=True, validate_responses=True) 

if __name__ == "__main__":
    app.run(port=8090)

