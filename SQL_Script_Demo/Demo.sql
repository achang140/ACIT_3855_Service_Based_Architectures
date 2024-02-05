CREATE DATABASE events; 
USE events; 

SELECT * FROM hotel_room; 
SELECT * FROM hotel_activity; 

SELECT count(*) from hotel_room;
SELECT count(*) from hotel_activity;

SELECT * FROM hotel_activity WHERE trace_id = "28daa495-7f62-4996-ab1b-03031bb22d61"