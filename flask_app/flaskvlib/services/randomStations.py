from flask import Flask, render_template, request, redirect, url_for
from flask_redis import FlaskRedis
from datetime import datetime
from flaskvlib import app, redis_client, redis_slave
import random

def randomStation():
    existing_station_ids = redis_client.keys("vlibid:*")
    random.shuffle(existing_station_ids)
    num_random_stations = 100
    random_station_ids = existing_station_ids[:num_random_stations]

    random_stations_data = []

    for station_id in random_station_ids:
        station_data = redis_client.hgetall(station_id)
        station_info = {
            "id": station_data.get(b'id').decode('utf-8'),
            "station": station_data.get(b'station').decode('utf-8'),
            "status": station_data.get(b'status').decode('utf-8'),
            # Ajoutez d'autres champs ici
        }
        random_stations_data.append(station_info)
    
    return random_stations_data