import logging
from datetime import datetime, timedelta
from functools import wraps
from urllib import parse as urlparser

import jwt
import oauth2
from flask import current_app, jsonify, request, Blueprint, session

from .models import JwtBlacklist, db, Tweet, to_dict
from .models import User
from .twitter_credentials import app_access_token


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
        except jwt.InvalidTokenError as e:
            print(e)
            return jsonify(invalid_msg), 401
        except Exception as e:
            logging.exception("message")
            return jsonify({
                'message': 'An error occured !',
                'authenticated': True
            }), 500

    return _verify

consumer = oauth2.Consumer(app_access_token['key'], app_access_token['secret'])
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


import dateutil.parser

def get_datetime_from_iso8601_string(s):
    d = dateutil.parser.parse(s)
    return d

tweets_blueprint = Blueprint('tweets', __name__, url_prefix='/tweets')

@tweets_blueprint.route('', methods=['POST'])
@token_required
def create_tweet(**kwargs):
    current_user = kwargs.get('current_user')
    send_date = get_datetime_from_iso8601_string(request.json['date'])
    tweet = Tweet(text=request.json['text'], send_date=send_date, status='DRAFT')
    current_user.tweets.append(tweet)
    db.session.flush()
    db.session.commit()
    return jsonify({'id': tweet.id})

@tweets_blueprint.route('/<int:id>', methods=['PUT'])
@token_required
def update_tweet(**kwargs):
    tweet = Tweet.query.filter(Tweet.id == request.view_args['id']).first()
    tweet.text = request.json['text']
    db.session.commit()
    return jsonify({'id': tweet.id})

@tweets_blueprint.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_tweet(**kwargs):
    Tweet.query.filter(Tweet.id == request.view_args['id']).delete()
    db.session.commit()
    return jsonify({'status': 'ok'})

@tweets_blueprint.route('', methods=['GET'])
@token_required
def get_user_tweets(**kwargs):
    tweets = Tweet.query.filter(User.id == kwargs.get('current_user').id).all()
    return jsonify([to_dict(tweet) for tweet in tweets])


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

    access_token = dict(urlparser.parse_qs(content.decode('utf-8')))

    expire_date = datetime.utcnow() + timedelta(days=4000)

    username = access_token['screen_name'][0]

    user = User.query.filter_by(username=username).first()
    if user is None:
        new_user = User(username=username, twitter_id=access_token['user_id'][0], oauth_token=access_token['oauth_token'][0], oauth_secret=access_token['oauth_token_secret'][0])
        db.session.add(new_user)
        db.session.commit()

    token = jwt.encode({
        'sub': username,
        'iat': datetime.utcnow(),
        'exp': expire_date},
        current_app.config['SECRET_KEY'])

    response = jsonify()
    response.set_cookie('Authorization', token.decode('UTF-8'))
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
    return jsonify({'username': kwargs.get('current_user').username})

####################
###### Tweet Scheduler
####################

def send_planned_tweets():
    print(datetime.utcnow())

    # TODO:
    # - retrieve matching tweets for current date
    # - Send the found tweets using specific user oauth tokens

# schedule.every(10).minutes.do(job)
# schedule.every(1).seconds.do(send_planned_tweets)

# while True:
#     schedule.run_pending()
#     time.sleep(1)