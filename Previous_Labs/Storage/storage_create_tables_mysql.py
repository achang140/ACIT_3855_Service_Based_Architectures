import mysql.connector
import yaml 

with open('app_conf.yml', 'r') as f: 
    app_config = yaml.safe_load(f.read())

db_conn = mysql.connector.connect(host=app_config["datastore"]["hostname"], 
                                  user=app_config["datastore"]["user"],
                                  password=app_config["datastore"]["password"], 
                                  database=app_config["datastore"]["db"])

db_cursor = db_conn.cursor()

db_cursor.execute('''
        CREATE TABLE hotel_room
        (id INT NOT NULL AUTO_INCREMENT,
        hotel_id VARCHAR(250) NOT NULL,
        customer_id VARCHAR(250) NOT NULL,
        room_id VARCHAR(250) NOT NULL,
        room_type VARCHAR(250) NOT NULL,
        num_of_people INTEGER NOT NULL,
        check_in_date VARCHAR(100) NOT NULL,
        check_out_date VARCHAR(100) NOT NULL,
        timestamp VARCHAR(100) NOT NULL,
        date_created VARCHAR(100) NOT NULL,
        trace_id VARCHAR(250) NOT NULL,
        CONSTRAINT hotel_room_pk PRIMARY KEY (id))
        ''')

db_cursor.execute('''
        CREATE TABLE hotel_activity
        (id INT NOT NULL AUTO_INCREMENT,
        hotel_id VARCHAR(250) NOT NULL,
        customer_id VARCHAR(250) NOT NULL,
        activity_id VARCHAR(250) NOT NULL,
        activity_name VARCHAR(250) NOT NULL,
        num_of_people INTEGER NOT NULL,
        reservation_date VARCHAR(100) NOT NULL,
        timestamp VARCHAR(100) NOT NULL,
        date_created VARCHAR(100) NOT NULL,
        trace_id VARCHAR(250) NOT NULL,
        CONSTRAINT hotel_activity_pk PRIMARY KEY (id))
        ''')

db_conn.commit()
db_conn.close() 