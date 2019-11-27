from flask_restful import Resource, abort, reqparse
import werkzeug
from config import Config
from PIL import Image
import numpy
from firebase_admin import auth

class Diagnosis(Resource):
    def __init__(self):
        super().__init__()
        self.config = Config('./config.json')
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('image', type=werkzeug.datastructures.FileStorage, location='files')

    def post(self):
        image = self.__get_image_from_request()
        valid, error = self.__validate_image(image)
        if valid:
            return { 'diagnosis': 'Cancer xd' }
        else:
            abort(400, error=error)

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
        image_store = data['image']
        if image_store != None:
            image_pil = Image.open(image_store.stream)
            image_pil.load()
            return numpy.array(image_pil)[:,:,:3]
        else:
            abort(400, error='cannot find file with key \'image\' in the request')
        return numpy.ndarray((1))
