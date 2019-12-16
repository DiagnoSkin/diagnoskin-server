from flask_restful import Resource, abort, reqparse
from flask import request
import base64
from io import BytesIO
from PIL import Image
import numpy as np
class Hello(Resource):
    def post(self):
        if 'Authentication' in request.headers:
            token = request.headers['Authentication']
            parser = reqparse.RequestParser()
            parser.add_argument('image', required=True)
            data = parser.parse_args()

            image = Image.open(BytesIO(base64.b64decode(data.image)))
            image_numpy = np.array(image)
            return { 'message': f"data: {image_numpy}" }
        else:
            abort(400, error='Cannot find Authentication header')

    def get(self):
        from main import model
        return { 'message': f"{model.layers}" }

