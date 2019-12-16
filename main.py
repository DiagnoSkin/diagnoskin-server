from tensorflow.keras.models import load_model
from tensorflow.python.lib.io import file_io

model_file = file_io.FileIO('gs://prediction-model-storage/EfficientNetB0-1024-0.4-1024-7.best.h5', mode='rb')

temp_model_location = './temp_model.h5'
temp_model_file = open(temp_model_location, 'wb')
temp_model_file.write(model_file.read())
temp_model_file.close()
model_file.close()

model = load_model(temp_model_location)

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
    app.run(debug=True)
