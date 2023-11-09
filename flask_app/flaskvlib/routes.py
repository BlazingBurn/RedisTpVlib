from flaskvlib import redis_client, app

@app.route('/')
def index():
    return redis_client.hgetall('vlibid:8035')