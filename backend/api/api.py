from flask import jsonify
from flask.views import MethodView

from .models import Player as PlayerModel, to_dict

class PlayerAPI(MethodView):
    def get(self):
        return jsonify([to_dict(player) for player in PlayerModel.query.all()])
