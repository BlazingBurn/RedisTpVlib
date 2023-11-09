from flask import Flask
from flask_redis import FlaskRedis


app = Flask(__name__)
app.config['SECRET_KEY'] = '323b22caac41acbf'
app.config['REDIS_URL'] = "redis://localhost:6379/0"

redis_client = FlaskRedis(app)

from flaskvlib import routes

