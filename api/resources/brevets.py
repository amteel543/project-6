"""
Resource: Brevets
"""
from flask import Response, request
from flask_restful import Resource

# You need to implement this in database/models.py
from database.models import Brevet

class Brevets(Resource):

    def get(self):

        output_json = Brevet.objects().to_json()

        return Response(output_json, mimetype="application/json", status=200)

    def post(self):

        input_json = request.json

        length = input_json["length"]
        
        start_time = input_json["start_time"]

        checkpoints = input_json["checkpoints"]

        result = Brevet(length=length, start_time=start_time, checkpoints=checkpoints).save()
        return {'_id': str(result.id)}, 200
