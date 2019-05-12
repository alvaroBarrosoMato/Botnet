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


class Employees_Name(Resource):
    def get(self, employee_id):
        conn = db_connect.connect()
        query = conn.execute("select * from employees where EmployeeId =%d " % int(employee_id))
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)


api.add_resource(Clasificador, '/clasificador')  # Route_1
api.add_resource(ArbolDeDecision, '/arboldedecision')  # Route_1
