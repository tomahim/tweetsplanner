from flask import jsonify, request
from flask.views import MethodView
from flask_login import login_required, login_user, logout_user, current_user

from .models import Player as PlayerModel, to_dict, User
from flask import Blueprint

class PlayerAPI(MethodView):
    @login_required
    def get(self):
        return jsonify([to_dict(player) for player in PlayerModel.query.all()])

users_blueprint = Blueprint('users', __name__, url_prefix='/users')

@users_blueprint.route('/login', methods=['POST'])
def login():
    if request.json is None:
        return 'WRONG PARAMS'

    user = User.query.filter_by(username=request.json['username']).first()
    if user is None or not user.check_password(request.json['password']):
        return 'Invalid username or password'

    login_user(user)
    return 'Connected'

@users_blueprint.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return 'User disconnected'

@users_blueprint.route('/me', methods=['GET'])
def me():
    if not current_user.is_authenticated:
        return 'Unauthorized'
    return jsonify({'username': current_user.username})