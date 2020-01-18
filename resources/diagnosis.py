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
        self.parser.add_argument('center', action='append', type=int)
        self.parser.add_argument('radius', type=int)
        self.parser.add_argument('refImageSize', action='append', type=int)

    def post(self):
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'][7:]
            # TODO validate token using firebase admin api
            # for testing the endpoint is not secured
            image = self.__get_image_from_request()
            valid, error = self.__validate_image(image)
            if valid:
                inp = []
                inp.append(image.astype(float))
                inp = np.array(inp)
                prediction = ai.model.predict(inp)
                return { 'diagnosis': ai.map_prediction_to_label(prediction) }
            else:
                abort(400, error=error)
        else:
            abort(400, error='Cannot authenticate user')

    def get(self):
        ai.model.summary()
        return { 'model': 'ok' }

    def __validate_image(self, image):
        error = ''
        valid = True
        if not hasattr(image, 'shape'):
            error = 'cannot extract the image from the request'
            valid = False
        return valid, error

    def __get_image_from_request(self):
        data = self.parser.parse_args()
        image = Image.open(BytesIO(base64.b64decode(data.image)))
        box = self.__get_crop_size(data.center, data.radius, data.refImageSize, (image.width, image.height))
        image = image.crop(box)
        image = image.resize((self.config.imageWidth, self.config.imageHeight))
        image_numpy = np.array(image)[:,:,:3]
        return image_numpy

    def __get_crop_size(self, center, radius, refSize, targetSize):
        scale = targetSize[0] / refSize[0]
        targetCenter = (center[0] * scale, center[1] * scale)
        targetRadius = radius * scale
        return (int(targetCenter[0] - targetRadius), int(targetCenter[1] - targetRadius), int(targetCenter[0] + targetRadius), int(targetCenter[1] + targetRadius))
