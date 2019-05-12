from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

app.run(port='5002')

class Clasificador(Resource):
    def get(self):
        return {'clase': [1]}  # Fetches first column that is Employee ID


class ArbolDeDecision(Resource):
    def get(self):

        return {'clase': []}  # Fetches first column that is Employee ID



api.add_resource(Clasificador, '/clasificador')  # Route_1
api.add_resource(ArbolDeDecision, '/arboldedecision')  # Route_1

if __name__ == "__main__":
  app.run()