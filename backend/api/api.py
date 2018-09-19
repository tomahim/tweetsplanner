import cgi
from datetime import datetime, timedelta
from functools import wraps
from urllib import parse as urlparser

import jwt
import oauth2
from flask import current_app, jsonify, request, redirect, Blueprint, session
from flask.views import MethodView

from .models import Player as PlayerModel, to_dict, JwtBlacklist, db
from .models import User


def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        token = request.headers.get('Authorization')

        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

        if token is None:
            return jsonify(invalid_msg), 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'])

            blacklisted = JwtBlacklist.query.filter_by(token=token).first()
            if blacklisted:
                return jsonify(invalid_msg), 401

            user = User.query.filter_by(username=data['sub']).first()
            if not user:
                raise RuntimeError('User not found')
            return f(current_user=user, token=token, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401 # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401

    return _verify

# It's probably a good idea to put your consumer's OAuth token and
# OAuth secret into your project's settings.
consumer = oauth2.Consumer('cTRantOxOurOTbS7LvJhnKDc7', 'biw4IBJGogdUShAaDLTGeRD61138L7miIZcsw3MCflP90I6BQT')
client = oauth2.Client(consumer)

request_token_url = 'https://api.twitter.com/oauth/request_token'
access_token_url = 'https://api.twitter.com/oauth/access_token'

# This is the slightly different URL used to authenticate/authorize.
authenticate_url = 'https://api.twitter.com/oauth/authenticate'

def get_twitter_auth_url():
    # Step 1. Get a request token from Twitter.
    resp, content = client.request(request_token_url, "GET")
    if resp['status'] != '200':
        raise Exception("Invalid response from Twitter.")

    # Step 2. Store the request token in a session for later use.
    session['request_token'] = dict(urlparser.parse_qs(content.decode('utf-8')))

    # Step 3. Redirect the user to the authentication URL.
    url = "{}?oauth_token={}".format(authenticate_url, session['request_token']['oauth_token'][0])

    return url


class PlayerAPI(MethodView):
    @token_required
    def get(self, **kwargs):
        return jsonify([to_dict(player) for player in PlayerModel.query.all()])

users_blueprint = Blueprint('users', __name__, url_prefix='/users')

@users_blueprint.route('/login', methods=['POST'])
def login():
    return jsonify({'authenticate_url': get_twitter_auth_url()})

@users_blueprint.route('/confirm_authenticate', methods=['POST'])
def confirm_authenticate():
    # Step 1. Use the request token in the session to build a new client.

    token = oauth2.Token(session['request_token']['oauth_token'][0],
                        session['request_token']['oauth_token_secret'][0])
    token.set_verifier(request.json['oauth_verifier'])
    client = oauth2.Client(consumer, token)



    # Step 2. Request the authorized access token from Twitter.
    resp, content = client.request(access_token_url, "GET")
    if resp['status'] != '200':
        raise Exception("Invalid response from Twitter.")

    """
    This is what you'll get back from Twitter. Note that it includes the
    user's user_id and screen_name.
    {
        'oauth_token_secret': 'IcJXPiJh8be3BjDWW50uCY31chyhsMHEhqJVsphC3M',
        'user_id': '120889797', 
        'oauth_token': '120889797-H5zNnM3qE0iFoTTpNEHIz3noL9FKzXiOxwtnyVOD',
        'screen_name': 'heyismysiteup'
    }
    """
    access_token = dict(urlparser.parse_qs(content.decode('utf-8')))

    # invalid_msg = {
    #     'message': 'Username / password is invalid',
    #     'authenticated': False
    # }
    #
    # if request.json is None:
    #     return jsonify(invalid_msg), 401
    #
    # user = User.query.filter_by(username=request.json['username']).first()
    # if user is None or not user.check_password(request.json['password']):
    #     return jsonify(invalid_msg), 401

    expire_date = datetime.utcnow() + timedelta(days=4000)

    token = jwt.encode({
        'sub': 'tom',
        'iat': datetime.utcnow(),
        'exp': expire_date},
        current_app.config['SECRET_KEY'])

    response = jsonify()
    response.set_cookie('Authorization', token.decode('UTF-8'))
    response.set_cookie('oauth_token', access_token['oauth_token'][0])
    response.set_cookie('oauth_secret', access_token['oauth_token_secret'][0])
    session.pop('request_token')
    return response



@users_blueprint.route('/logout', methods=['POST'])
@token_required
def logout(**kwargs):
    blacklisted = JwtBlacklist(token=kwargs.get('token'))
    db.session.add(blacklisted)
    db.session.commit()
    return jsonify({'status': 'ok'}), 200

@users_blueprint.route('/me', methods=['GET'])
@token_required
def me(**kwargs):
    return jsonify({'username': kwargs.get('username')})