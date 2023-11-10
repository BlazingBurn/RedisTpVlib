from flask import Flask, render_template, request, redirect, url_for
from flask_redis import FlaskRedis
from datetime import datetime

app = Flask(__name__)
app.config['REDIS_URL'] = "redis://localhost:6379/0"
app.config['REDIS_URL_SLAVE'] = "redis://localhost:6380/1"
redis_client = FlaskRedis(app, 'REDIS_URL')
redis_slave = FlaskRedis(app, 'REDIS_URL_SLAVE')

from flaskvlib import routes
