from flask_restful import Resource, abort, reqparse
from config import Config
from PIL import Image
import numpy as np
import base64
from io import BytesIO
from flask import request

class Crop(Resource):
    def __init__(self):
        super().__init__()
        self.config = Config('./config.json')
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('image', required=True)
        self.parser.add_argument('center', action='append', type=int)
        self.parser.add_argument('radius', type=int)
        self.parser.add_argument('refImageSize', action='append', type=int)

    def post(self):
        image = self.__get_image_from_request()
        return { 'result': self.__encode_image(image) }

    def __get_image_from_request(self):
        data = self.parser.parse_args()
        image = Image.open(BytesIO(base64.b64decode(data.image)))
        box = self.__get_crop_size(data.center, data.radius, data.refImageSize, (image.width, image.height))
        image = image.crop(box)
        image = image.resize((self.config.imageWidth, self.config.imageHeight))
        return image

    def __get_crop_size(self, center, radius, refSize, targetSize):
        scale = targetSize[0] / refSize[0]
        targetCenter = (center[0] * scale, center[1] * scale)
        targetRadius = radius * scale
        return (int(targetCenter[0] - targetRadius), int(targetCenter[1] - targetRadius), int(targetCenter[0] + targetRadius), int(targetCenter[1] + targetRadius))

    def __encode_image(self, image):
        # image.save('./image.jpg')
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())
        return f"{img_str}"[2:-1]
