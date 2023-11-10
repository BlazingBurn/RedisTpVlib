from flask import Flask, render_template, request, redirect, url_for
from flask_redis import FlaskRedis
from datetime import datetime

app = Flask(__name__)
app.config['REDIS_URL'] = "redis://localhost:6379/0"
app.config['REDIS_URL_SLAVE'] = "redis://localhost:6380/1"
app.config['SECRET_KEY'] = '2178976565787'
redis_client = FlaskRedis(app, config_prefix='REDIS_URL')
redis_slave = FlaskRedis(app, config_prefix='REDIS_URL_SLAVE')

from flaskvlib import routes
