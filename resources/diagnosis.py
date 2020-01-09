from flask_restful import Resource, abort, reqparse
from config import Config
from PIL import Image
import numpy as np
from firebase_admin import auth
import base64
from io import BytesIO
import model.ai as ai
from flask import request

class Diagnosis(Resource):
    def __init__(self):
        super().__init__()
        self.config = Config('./config.json')
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('image', required=True)

    def post(self):
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'][7:]
            # TODO validate token using firebase admin api
            # for testing the endpoint is not secured
            image = self.__get_image_from_request()
            valid, error = self.__validate_image(image)
            if valid:
                prediction = ai.model.predict(image)
                return { 'diagnosis': prediction }
            else:
                abort(400, error=error)
        else:
            abort('Cannot authenticate user')

    def get(self):
        ai.model.summary()
        return { 'model': 'ok' }

    def __validate_image(self, image):
        error = ''
        valid = True
        if hasattr(image, 'shape'):
            if image.shape != (self.config.imageHeight, self.config.imageWidth, 3):
                error = f'image has to be {self.config.imageHeight}x{self.config.imageWidth} and rgb'
                valid = False
        else:
            error = 'cannot extract the image from the request'
            valid = False
        return valid, error

    def __get_image_from_request(self):
        data = self.parser.parse_args()
        image = Image.open(BytesIO(base64.b64decode(data.image)))
        image_numpy = np.array(image)[:,:,:3]
        return image_numpy
