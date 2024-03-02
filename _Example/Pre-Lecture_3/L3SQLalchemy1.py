""" SQLAlchemy Declaratives """

from sqlalchemy import Column, Integer, String, DateTime 
# from base import Base 
from L3base import Base 
import datetime

class HeartRate(Base): # HeartRate extends a SQLAlchemy Base class # Heart Rate inherits from Base class 
    """ Heart Rate """ 

    # Table Mapping - Mapping to the heart_rate table 
    __tablename__ = "heart_rate"

    # Column Mapping - Mapping to the columns in the heart_rate table 
    id = Column(Integer, primary_key=True)
    patient_id = Column(String(250), nullable=False)
    device_id = Column(String(250), nullable=False)
    heart_rate = Column(Integer, nullable=False)
    timestamp = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)

    # Constructor 
    def __init__(self, patient_id, device_id, timestamp, heart_rate):
        """ Initializes a heart rate reading """
        self.patient_id = patient_id
        self.device_id = device_id
        self.timestamp = timestamp
        self.date_created = datetime.datetime.now() # Sets the date/time the record is created 
        self.heart_rate = heart_rate

    # Custom Method - Helper method to put the object's attributes into a Python dictionary. 
    # This Python dictionary can later be serialized into JSON. 
    def to_dict(self):
        """ Dictionary Representation of a heart rate reading """
        dict = {}

        dict["id"] = self.id
        dict["patient_id"] = self.patient_id
        dict["device_id"] = self.device_id
        dict["heart_rate"] = self.heart_rate
        dict["timestamp"] = self.timestamp
        dict["date_created"] = self.date_created

        return dict 
