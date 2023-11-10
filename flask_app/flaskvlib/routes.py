from flask import Flask, render_template, request, redirect, url_for
from flask_redis import FlaskRedis
from datetime import datetime
from flaskvlib import app, redis_client, redis_slave
import logging
import random

# Configurer les logs
logging.basicConfig(level=logging.DEBUG)

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


@app.route('/', methods=['GET', 'POST'])
def search_data():
    data = []

    if request.method == 'POST':
        data = []
        commune = request.form.get('commune')
        station_name = request.form.get('station')

        if commune or station_name:
            keys = redis_client.keys("vlibid:*")
            for key in keys:
                station_data = redis_client.hgetall(key)
                station_commune = station_data.get(b'commune').decode('utf-8')
                station_station = station_data.get(b'station').decode('utf-8')

                if (not commune or commune.lower() in station_commune.lower()) and \
                   (not station_name or station_name.lower() in station_station.lower()):
                    data.append({
                        "id": station_data.get(b'id').decode('utf-8'),
                        "station": station_station,
                        "status": station_data.get(b'status').decode('utf-8'),
                        # Ajoutez d'autres champs ici
                    })
    
    # Si aucune recherche n'a été effectuée, affichez les données aléatoires
    else:
        data = random_stations_data


    return render_template('data.html', data=data)

@app.route('/modify/<int:id>', methods=['GET', 'POST'])
def modify(id):
    station_key = f'vlibid:{id}'
    station_data = redis_client.hgetall(station_key)
    current_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")

    station_name = station_data.get(b'station').decode('utf-8')
    
    decoded_station_data = {}
    for key, value in station_data.items():
        decoded_station_data[key.decode('utf-8')] = value.decode('utf-8')


    if request.method == 'POST':
        # Recuperation data
        new_station_name = request.form.get('new_station_name')
        new_status = request.form.get('new_status')
        new_capacity = request.form.get('new_capacity')
        new_nbbornettesLibre = request.form.get('new_nbbornettesLibre')
        new_nbtotalvelodispo = request.form.get('new_nbtotalvelodispo')
        new_velomecadispo = request.form.get('new_velomecadispo')
        new_veloelecdispo = request.form.get('new_veloelecdispo')
        new_bornedispo = request.form.get('new_bornedispo')
        new_retourvelip = request.form.get('new_retourvelip')
        new_actualisation = request.form.get('new_actualisation')
        new_commune = request.form.get('new_commune')

        # Mise a jour redis
        redis_client.hset(station_key, 'station', new_station_name)
        redis_client.hset(station_key, 'status', new_status)
        redis_client.hset(station_key, 'capacity', new_capacity)
        redis_client.hset(station_key, 'nbbornettesLibre', new_nbbornettesLibre)
        redis_client.hset(station_key, 'nbtotalvelodispo', new_nbtotalvelodispo)
        redis_client.hset(station_key, 'velomecadispo', new_velomecadispo)
        redis_client.hset(station_key, 'veloelecdispo', new_veloelecdispo)
        redis_client.hset(station_key, 'bornedispo', new_bornedispo)
        redis_client.hset(station_key, 'retourvelip', new_retourvelip)
        redis_client.hset(station_key, 'actualisation', new_actualisation)
        redis_client.hset(station_key, 'commune', new_commune)

        return redirect('/')

    return render_template('modify.html', id=id, station_data=decoded_station_data, current_date=current_date)


@app.route('/add', methods=['GET', 'POST'])
def add_data():
    
    current_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")
    
    if request.method == 'POST':
        new_id = request.form.get('new_id')
        new_station_name = request.form.get('new_station_name')
        new_status = request.form.get('new_status')
        new_capacity = request.form.get('new_capacity')
        new_nbbornettesLibre = request.form.get('new_nbbornettesLibre')
        new_nbtotalvelodispo = request.form.get('new_nbtotalvelodispo')
        new_velomecadispo = request.form.get('new_velomecadispo')
        new_veloelecdispo = request.form.get('new_veloelecdispo')
        new_bornedispo = request.form.get('new_bornedispo')
        new_retourvelip = request.form.get('new_retourvelip')
        new_actualisation = request.form.get('new_actualisation')
        new_commune = request.form.get('new_commune')

        # S'assurer que le nouvel ID est unique avant d'ajouter la station

        if not redis_client.exists(f'vlibid:{new_id}'):

            data = {
                'id': new_id,
                'station': new_station_name,
                'status': request.form.get('new_status'),
                'capacity': request.form.get('new_capacity'),
                'nbbornettesLibre': request.form.get('new_nbbornettesLibre'),
                'nbtotalvelodispo': request.form.get('new_nbtotalvelodispo'),
                'velomecadispo': request.form.get('new_velomecadispo'),
                'veloelecdispo': request.form.get('new_veloelecdispo'),
                'bornedispo': request.form.get('new_bornedispo'),
                'retourvelip': request.form.get('new_retourvelip'),
                'actualisation': request.form.get('new_actualisation'),
                'commune': request.form.get('new_commune')
            }

            redis_client.hset(f'vlibid:{new_id}', mapping=data)

            return redirect('/')

    return render_template('add.html', current_date=current_date)


@app.route('/delete/<int:id>', methods=['GET'])
def delete_data(id):
    station_key = f'vlibid:{id}'
    
    if redis_client.exists(station_key):
        redis_client.delete(station_key)
        return redirect('/')
    else:
        # Gérer le cas où la station n'existe pas ou a déjà été supprimée
        return "La station n'existe pas ou a déjà été supprimée."