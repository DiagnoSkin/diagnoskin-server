from flask import Flask
from flask_restful import Api
from resources.diagnosis import Diagnosis
from resources.hello import Hello
import firebase_admin

firebase_app = firebase_admin.initialize_app()
app = Flask(__name__)
api = Api(app)

api.add_resource(Diagnosis, '/api/diagnosis')
api.add_resource(Hello, '/api/hello')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)
