from flask import Flask
from flask_cors import CORS
from api.config import Config
from api.api import users_blueprint, tweets_blueprint
from api.models import db


def create_app(config):
    app = Flask(__name__)
    app.secret_key = Config.SECRET_KEY
    CORS(app, expose_headers=['Authorization'], supports_credentials=True)
    app.config.from_object(config)
    register_extensions(app)
    return app


def register_api(app):
    app.register_blueprint(tweets_blueprint)
    app.register_blueprint(users_blueprint)

def register_extensions(app):
    db.init_app(app)
    register_api(app)

app = create_app(Config)

# Run the application
if __name__ == '__main__':
    app = create_app(Config)
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
