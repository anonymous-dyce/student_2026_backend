from flask import Blueprint, jsonify
from flask_restful import Api, Resource
from __init__ import app, db, login_manager  # Key Flask objects
leaderboard_api = Blueprint('leaderboard_api', __name__, url_prefix='/api')
api = Api(leaderboard_api)
class LeaderboardAPI:
    @staticmethod
    def get_score(name):
        score = {
            "Four": {
                "rank": 4,
                "player": "Player4",
                "wins": 9,
            },
            "Five": {
                "name": 5,
                "player": "Player5",
                "wins": 8,
            },
            "Six": {
                "name": 6,
                "player": "Player6",
                "wins": 7,
            },
            "Seven": {
                "name": 7,
                "player": "Player7",
                "wins": 6,
            },
            "Eight": {
                "name": 8,
                "player": "Player8",
                "wins": 5,
            },
            "Nine": {
                "name": 9,
                "player": "Player9",
                "wins": 4,
            },
             "Ten": {
                "name": 10,
                "player": "Player10",
                "wins": 3,
            },
        }
        return score.get(name)
    class _Four(Resource):
        def get(self):
            # Use the helper method to get John's details
            four_details = LeaderboardAPI.get_score("Four")
            return jsonify(four_details)
    class _Five(Resource):
        def get(self):
            # Use the helper method to get John's details
            five_details = LeaderboardAPI.get_score("Five")
            return jsonify(five_details)
    class _Six(Resource):
        def get(self):
            # Use the helper method to get John's details
            six_details = LeaderboardAPI.get_score("Six")
            return jsonify(six_details)
    class _Seven(Resource):
        def get(self):
            # Use the helper method to get John's details
            seven_details = LeaderboardAPI.get_score("Seven")
            return jsonify(seven_details)
    class _Eight(Resource):
        def get(self):
            # Use the helper method to get John's details
            eight_details = LeaderboardAPI.get_score("Eight")
            return jsonify(eight_details)
    class _Nine(Resource):
        def get(self):
            # Use the helper method to get John's details
            nine_details = LeaderboardAPI.get_score("Nine")
            return jsonify(nine_details)
    class _Ten(Resource):
        def get(self):
            # Use the helper method to get John's details
            ten_details = LeaderboardAPI.get_score("Ten")
            return jsonify(ten_details)
    class _Bulk(Resource):
        def get(self):
            # Use the helper method to get both John's and Jeff's details
            four_details = LeaderboardAPI.get_score("four")
            five_details = LeaderboardAPI.get_score("five")
            six_details = LeaderboardAPI.get_score("six")
            seven_details = LeaderboardAPI.get_score("seven")
            eight_details = LeaderboardAPI.get_score("eight")
            nine_details = LeaderboardAPI.get_score("nine")
            ten_details = LeaderboardAPI.get_score("ten")
            return jsonify({"score": [four_details, five_details, six_details, seven_details, eight_details, nine_details, ten_details]})
    # Building REST API endpoints
    api.add_resource(_Four, '/score/four')
    api.add_resource(_Five, '/score/five')
    api.add_resource(_Six, '/score/six')
    api.add_resource(_Seven, '/score/seven')
    api.add_resource(_Eight, '/score/eight')
    api.add_resource(_Nine, '/score/nine')
    api.add_resource(_Ten, '/score/ten')
    api.add_resource(_Bulk, '/score')
# Instantiate the StudentAPI to register the endpoints
leaderboard_api_instance = LeaderboardAPI()





