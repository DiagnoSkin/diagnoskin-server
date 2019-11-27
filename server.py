from flask import Flask
from flask_restful import Api
from resources.diagnosis import Diagnosis
import firebase_admin

firebase_app = firebase_admin.initialize_app()
app = Flask(__name__)
api = Api(app)

api.add_resource(Diagnosis, '/api/diagnosis')

if __name__ == '__main__':
    app.run(debug=True)
