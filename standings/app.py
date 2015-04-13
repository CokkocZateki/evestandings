from flask import Flask, jsonify
from flask.ext.redis import Redis
from standings import Standings
from standings.cache import EVEAPIRedisCache


app = Flask(__name__)
app.config['REDIS_URL'] = os.environ.get('REDIS_URL')
app.config['API_KEY_ID'] = os.environ.get('STANDINGS_API_KEY_ID')
app.config['API_KEY_VCODE'] = os.environ.get('STANDINGS_API_KEY_VCODE')
redis = Redis(app)
cache = EVEAPIRedisCache(redis)
standings = Standings(app.config['API_KEY_ID'], app.config['API_KEY_VCODE'], cache_handler=cache)


@app.route('/')
@app.route('/standings.html')
def index_html():
  return standings.html()

@app.route('/standings.txt')
def index_txt():
  return standings.text()
 
@app.route('/standings.json')
def index_json():
    return jsonify(standings._get_standings())

@app.route('/<string:template>')
def index_template(template):
    return standings.render_template(template)

if __name__ == '__main__':
    app.debug = True
    app.run()
