from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from __init__ import app, db
from model.checklist_progress import ChecklistProgress
import json

checklist_api = Blueprint('checklist_api', __name__, url_prefix='/api')
api = Api(checklist_api)

class ChecklistAPI:
    class _Checklist(Resource):

        def get(self):
            """
            GET /api/checklist?user=username
            """
            user = request.args.get('user')
            if not user:
                return {'message': 'Missing user parameter'}, 400

            checklist = ChecklistProgress.query.filter_by(user=user).first()
            if not checklist:
                return {'message': 'Checklist not found'}, 404

            return jsonify(checklist.read())

        def post(self):
            """
            POST /api/checklist
            Body: { "user": "student1", "progress": { "Install Python": true, ... } }
            """
            data = request.get_json()
            user = data.get('user')
            progress = data.get('progress')

            if not user or progress is None:
                return {'message': 'Missing user or progress'}, 400

            # Check if one already exists
            if ChecklistProgress.query.filter_by(user=user).first():
                return {'message': 'Checklist for this user already exists'}, 400

            checklist = ChecklistProgress(user=user, progress=progress)
            try:
                checklist.create()
                return jsonify(checklist.read())
            except Exception as e:
                return {'message': f'Error saving checklist: {e}'}, 500

        def put(self):
            """
            PUT /api/checklist
            Body: { "user": "student1", "progress": { ... } }
            """
            data = request.get_json()
            user = data.get('user')
            progress = data.get('progress')

            if not user or progress is None:
                return {'message': 'Missing user or progress'}, 400

            checklist = ChecklistProgress.query.filter_by(user=user).first()
            if not checklist:
                return {'message': 'Checklist not found'}, 404

            if checklist.update(progress):
                return jsonify({"message": "Checklist updated", "progress": progress})
            else:
                return {'message': 'Error updating checklist'}, 500

        def delete(self):
            """
            DELETE /api/checklist
            Body: { "user": "student1" }
            """
            data = request.get_json()
            user = data.get('user')

            if not user:
                return {'message': 'Missing user'}, 400

            checklist = ChecklistProgress.query.filter_by(user=user).first()
            if not checklist:
                return {'message': 'Checklist not found'}, 404

            try:
                checklist.delete()
                return jsonify({'message': f'Checklist for {user} deleted'})
            except Exception as e:
                return {'message': f'Error deleting checklist: {e}'}, 500

    api.add_resource(_Checklist, '/checklist')