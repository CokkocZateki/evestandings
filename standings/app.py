import os
from flask import Flask, jsonify, current_app
from flask.ext.redis import Redis
from standings import Standings
from standings.cache import EVEAPIRedisCache


app = Flask(__name__)
app.config['REDIS_URL'] = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
app.config['API_KEY_ID'] = os.environ.get('STANDINGS_API_KEY_ID')
app.config['API_KEY_VCODE'] = os.environ.get('STANDINGS_API_KEY_VCODE')
redis = Redis(app)
cache = EVEAPIRedisCache(redis)
standings = Standings(app.config['API_KEY_ID'], app.config['API_KEY_VCODE'], cache_handler=cache)


def check_config():
    if not current_app.config['API_KEY_ID'] or current_app.config['API_KEY_VCODE']:
        return 'Invalid API details specified, please check your configuration.'

@app.route('/')
@app.route('/standings.html')
def index_html():
    check_config()
    return standings.html()

@app.route('/standings.txt')
def index_txt():
    check_config()
    return standings.text()
 
@app.route('/standings.json')
def index_json():
    check_config()
    return jsonify(standings._get_standings())

@app.route('/<template>')
def index_template(template):
    check_config()
    return standings.render_template(template)

if __name__ == '__main__':
    app.debug = True
    app.run()
