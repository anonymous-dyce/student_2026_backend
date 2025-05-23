from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # Used for REST API building
from __init__ import app  # Ensure __init__.py initializes your Flask app
from model.leaderboard import Leaderboard
from api.jwt_authorize import token_required
# Blueprint for the API
leaderboard_api = Blueprint('leaderboard_api', __name__, url_prefix='/api')
api = Api(leaderboard_api)  # Attach Flask-RESTful API to the Blueprint


class CoolFactsAPI:


    class _CRUD(Resource):

        def post(self):
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()
            # Create a new post object using the data from the request
            post = Leaderboard(content=data['_content'], name=data['_title'])
            # Save the post object using the Object Relational Mapper (ORM) method defined in the model
            post.create()
            # Return response to the client in JSON format, converting Python dictionaries to JSON format
            return jsonify(post.read())
        
        def get(self):
            try:
                # Query all entries in the BinaryHistory table
                entries = Leaderboard.query.all()
                # Convert the entries to a list of dictionaries
                results = [entry.read() for entry in entries]
                # Return the list of results in JSON format
                return jsonify(results)
            except Exception as e:
                # Return an error message in case of failure
                return jsonify({"error": str(e)}), 500
            
   
    api.add_resource(_CRUD, '/leaderboard')
if __name__ == '__main__':
    app.run(debug=True)