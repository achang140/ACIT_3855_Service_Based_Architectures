# ACIT 3855 - Service Based Architectures LABS 

This is an application for resort hotels located in various countries, allowing customers to book hotel rooms and activities such as outdoor biking, yoga lessons, and rock climbing within the hotel.
The events consist of room booking requests and activity scheduling requests. Room booking requests are expected to peak on Friday evenings and weekends, with as many as 5000 requests per second. Activity scheduling requests are anticipated to be high on Friday nights, with as many as 1000 requests per second, as more customers typically arrive on Fridays and tend to book activities after checking in to the hotel.

The requests are stored to allow the following:
* Front counter staff to book hotel rooms for customers and assist with check-in and check-out.
* Staff in charge of activities to monitor and keep track of customers.
* Analysis of data to produce reports for management.

Users of the system include customers, resort hotel staff, including front counter staff responsible for customer check-in and check-out, staff responsible for monitoring activities, and management.

## Lab 1 
* Set up an account on [SwaggerHub](https://swagger.io/tools/swaggerhub/) 
* Created an OpenAPI 3.0 specification for the RESTful that receive 2 events  
* 2 POST endpoints in `openapi.yaml` file: 
    * `/booking/hotel-rooms`
    * `/booking/hotel-activities`

## Lab 2 
* Built an Edge Service (Receiver Service) that receives the 2 event types and stores them in a JSON file 
    * `Receiver` folder contains `app.py`, `openapi.yaml`, and `events.json`
    * Installed Packages in Virtual Environment (venv): 
        * `pip install connexion`
        * `pip install connexion[flask]`
        * `pip install connexion[swagger-ui]`
* Tested Edge Service with Apache JMeter and PostMan

### Installation: 
* [Apache JMeter](https://jmeter.apache.org/download_jmeter.cgi)
* [PostMan](https://www.postman.com/downloads/)