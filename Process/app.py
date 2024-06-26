import connexion 

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from base import Base
from stats import Stats

import yaml 
import logging
import logging.config
import requests
import datetime

from apscheduler.schedulers.background import BackgroundScheduler


with open('app_conf.yml', 'r') as f: 
    app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f: 
    log_config = yaml.safe_load(f.read()) 
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

# Connect to the database (db name: stats.sqlite)
DB_ENGINE = create_engine("sqlite:///%s" % app_config["datastore"]["filename"])

# DB_ENGINE = create_engine(f'mysql+pymysql://{app_config["datastore"]["user"]}:{app_config["datastore"]["password"]}@{app_config["datastore"]["hostname"]}:{app_config["datastore"]["port"]}/{app_config["datastore"]["db"]}')

Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

def get_stats():
    """ Gets Hotel Room and Hotel Activity processsed statistics """

    # Log an INFO message indicating request has started
    logger.info("Request Started")

    # Read in the current statistics from the SQLite database (i.e., the row with the most recent last_update datetime stamp.
    session = DB_SESSION() 

    stats = session.query(Stats).order_by(Stats.last_updated.desc()).first() 

    # If no stats exist, log an ERROR message and return 404 and the message “Statistics do not exist” OR return empty/default statistics
    if stats is None:
        logger.error("Statistics do not exist")
        return "Statistics do not exist", 404

    # Convert them as necessary into a new Python dictionary such that the structure matches that of your response defined in the openapi.yaml file.
    statistics = {
        "num_hotel_room_reservations": stats.num_hotel_room_reservations,
        "max_hotel_room_ppl": stats.max_hotel_room_ppl,
        "num_hotel_activity_reservations": stats.num_hotel_activity_reservations,
        "max_hotel_activity_ppl": stats.max_hotel_activity_ppl,
    }

    # Log a DEBUG message with the contents of the Python Dictionary
    logger.debug(statistics)

    # Log an INFO message indicating request has completed
    logger.info("Request Completed!")

    session.close() 

    # Return the Python dictionary as the context and 200 as the response code
    return statistics, 200 

def populate_stats():
    """ Periodically update stats """
    
    # Log an INFO message indicating periodic processing has started
    logger.info("Start Periodic Processing")

    # Read in the current statistics from the SQLite database (filename defined in your configuration)
    session = DB_SESSION() 
    
    print("Pass One!")
    
    # Query to get all the Stats objects from the database in descending order (from newest to oldest) 
    # Note that the first would be the most recent in this case 
    stats = session.query(Stats).order_by(Stats.last_updated.desc()).first() 

    print("Pass Two!")

    # - If no stats yet exist, use default values for the stats
    if stats is None:
        stats = Stats(
            num_hotel_room_reservations = 0,
            max_hotel_room_ppl = 0,
            num_hotel_activity_reservations = 0,
            max_hotel_activity_ppl = 0,
            last_updated=datetime.datetime.now()
        )
    

    session.add(stats)
    session.commit()

    print("Pass Three!")

    last_updated = stats.last_updated
    
    # Get the current datetime
    current_datetime = datetime.datetime.now()

    # print(current_datetime)
    # print(stats.last_updated)
    print("Pass Four!")

    curren_dateime_formatted = current_datetime.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    last_updated_formatted = last_updated.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    # Query the two GET endpoints from your Data Store Service (using requests.get) to get all new events 
    # from the last datetime you requested them (from your statistics) to the current datetime
    hotel_rooms_url = f"{app_config['eventstore']['url']}/booking/hotel-rooms?start_timestamp={last_updated_formatted}&end_timestamp={curren_dateime_formatted}"
    hotel_activities_url = f"{app_config['eventstore']['url']}/booking/hotel-activities?start_timestamp={last_updated_formatted}&end_timestamp={curren_dateime_formatted}"

    # print(hotel_rooms_url)

    print("Pass Five!")

    event_1_response = requests.get(hotel_rooms_url)
    event_2_response = requests.get(hotel_activities_url)

    # print(event_1_response)
    # print(event_2_response)

    print("Pass Six!")

    event_1_res_json = event_1_response.json()
    event_2_res_json = event_2_response.json()

    # print("Event 1:", len(event_1_res_json))
    # print(event_1_res_json)
    # print("Event 2:", len(event_2_res_json))
    # print(event_2_res_json)

    # - Log an INFO message with the number of events received
    if event_1_response.status_code == 200 and event_2_response.status_code == 200:
        logger.info(f"Received {len(event_1_res_json)} Hotel Room Reservation events and {len(event_2_res_json)} Hotel Activity Reservation events")

    # - Log an ERROR message if you did not get a 200 response code
    else:
        logger.error(f'''Failed to retrieve events from Hotel Room and Hotel Activity Reservations:
                      
                        Hotel Rooms Error: {event_1_response.text},

                        Hotel Activities Error: {event_2_response.text}''')
        return 

    print("Pass Seven!")

    # Based on the new events from the Data Store Service:
    # Calculate your updated statistics

    max_hotel_room_ppl_sql = stats.max_hotel_room_ppl

    max_hotel_activity_ppl_sql = stats.max_hotel_activity_ppl


    if len(event_1_res_json):
        max_hotel_room_ppl_json = max(event_1_res_json, key=lambda event1: event1["num_of_people"])["num_of_people"]
        # print(type(max_hotel_room_ppl_json))
        # print(max_hotel_room_ppl_json)

        if max_hotel_room_ppl_json > max_hotel_room_ppl_sql:
            new_max_hotel_room_ppl = max_hotel_room_ppl_json
        else:
            new_max_hotel_room_ppl = max_hotel_room_ppl_sql
    else:
        new_max_hotel_room_ppl = max_hotel_room_ppl_sql


    if len(event_2_res_json):
        max_hotel_activity_ppl_json = max(event_2_res_json, key=lambda event2: event2["num_of_people"])["num_of_people"]
        # print(type(max_hotel_activity_ppl_json))
        # print(max_hotel_activity_ppl_json)

        if max_hotel_activity_ppl_json > max_hotel_activity_ppl_sql:
            new_max_hotel_activity_ppl = max_hotel_activity_ppl_json
        else:
            new_max_hotel_activity_ppl = max_hotel_activity_ppl_sql
    else:
        new_max_hotel_activity_ppl = max_hotel_activity_ppl_sql
    
    print("Pass Eight!")

    new_num_hotel_room_reservations = stats.num_hotel_room_reservations + len(event_1_res_json)
    new_num_hotel_activity_reservations = stats.num_hotel_activity_reservations + len(event_2_res_json)

    print("Pass Nine!")

    new_stats = Stats(
        num_hotel_room_reservations=new_num_hotel_room_reservations,
        max_hotel_room_ppl=new_max_hotel_room_ppl,
        num_hotel_activity_reservations=new_num_hotel_activity_reservations,
        max_hotel_activity_ppl=new_max_hotel_activity_ppl,
        last_updated=current_datetime
    )

    # Write the updated statistics to the SQLite database file (filename defined in your configuration)
    session.add(new_stats)

    print("Pass Ten!")

    # # Log a DEBUG message for each event processed that includes the trace_id
    if len(event_1_res_json):
        trace_ids = [event_1["trace_id"] for event_1 in event_1_res_json]
        logger.debug(f"Processed Hotel Room Reservation Event Trace IDs: {', '.join(trace_ids)}")
    
    if len(event_2_res_json):
        trace_ids = [event_2["trace_id"] for event_2 in event_2_res_json]
        logger.debug(f"Processed Hotel Activity Reservation Event Trace IDs: {', '.join(trace_ids)}")

    print("Pass Eleven!")

    # Log a DEBUG message with your updated statistics values
    logger.debug(f"Num Hotel Room Reservations: {new_stats.num_hotel_room_reservations} \n"
                 f"Max Hotel Room People: {new_stats.max_hotel_room_ppl} \n" 
                 f"Num Hotel Activity Reservations: {new_stats.num_hotel_activity_reservations} \n"
                 f"Max Hotel Activity People: {new_stats.max_hotel_activity_ppl}\n"
                 f"Last Updated: {new_stats.last_updated.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'}")

    # Log an INFO message indicating period processing has ended
    logger.info("End Periodic Processing")

    session.commit() 
    session.close() 


def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats, 
                  'interval',
                   seconds=app_config['scheduler']['period_sec'])
    sched.start()


app = connexion.FlaskApp(__name__, specification_dir="")
app.add_api("openapi.yaml", strict_validation=True, validate_responses=True) 

if __name__ == "__main__":
    init_scheduler()
    app.run(port=8100)