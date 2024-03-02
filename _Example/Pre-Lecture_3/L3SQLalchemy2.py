""" SQLAlchemy Sessions """

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from heart_rate import HeartRate 
from L3SQLalchemy1 import HeartRate

### Example Add a Heart Rate Reading ### 

# Create a database session
session = DB_SESSION()

# Create a new HeartRate objective (calls the Constructor)
hr = HeartRate(patient_id,
               device_id,
               timestamp,
               heart_rate)

# Adds the HeartRate object to the database session 
session.add(hr) 

# Commits the HeartRate objective to the database and closes the session 
session.commit()
session.close() 



### Example Query for All Heart Rate Readings ### 

# Create a database session
session = DB_SESSION() 

# Queries for all HeartRate objects from the database 
all_readings = session.query(HeartRate).all() # Returns query results as a list 
one_reading = session.query(HeartRate).filter(HeartRate.id == query_id).first() # Returns a single result (not list)

session.close() 



### Can now access public attributes and methods on the HeartRate objects ### 

# Mapped columns are public instance variables 
print("Heart Rate is %d from device" % (one_reading.heart_rate, one_reading.device_id))

# Create a list of Python dictionaries for all readings 
all_readings_list = []

# Useful to convert to Python objects when returned as a response message from a connexion endpoint 
for reading in all_readings:
     all_readings_list.append(reading.to_dict())