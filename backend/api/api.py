from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask import Blueprint
from flask import current_app, jsonify, request
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

class PlayerAPI(MethodView):
    @token_required
    def get(self, **kwargs):
        return jsonify([to_dict(player) for player in PlayerModel.query.all()])

users_blueprint = Blueprint('users', __name__, url_prefix='/users')

@users_blueprint.route('/login', methods=['POST'])
def login():
    if request.json is None:
        return 'WRONG PARAMS'

    user = User.query.filter_by(username=request.json['username']).first()
    if user is None or not user.check_password(request.json['password']):
        return 'Invalid username or password'

    token = jwt.encode({
        'sub': user.username,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=30)},
        current_app.config['SECRET_KEY'])
    return jsonify({ 'token': token.decode('UTF-8') })

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