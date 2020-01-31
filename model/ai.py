from tensorflow.keras.models import load_model
from tensorflow.python.lib.io import file_io
from os import path
import numpy as np
import aiohttp
import asyncio
import efficientnet.tfkeras
from google.cloud import storage
from keras import backend as K

# model_file = file_io.FileIO('gs://prediction-model-storage/EfficientNetB0-1024-0.4-1024-7.best.h5', mode='rb')
local_model_name = './model/EfficientNetB0-1024-0.4-1024-7.best.h5'
bucket_name = "prediction-model-storage"
bucket_model_name = "EfficientNetB0-1024-0.4-1024-7.best.h5"

def map_prediction_to_label(prediction):
    labels = ['akiec', 'bcc', 'bkl', 'df', 'mel','nv', 'vasc']
    pred_index = np.argmax(prediction[0])
    return labels[pred_index]

def recall_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

async def download_from_bucket():
    if path.exists(local_model_name): return
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(bucket_model_name)
    blob.download_to_filename(local_model_name)

async def setup_model():
    await download_from_bucket()
    model = load_model(local_model_name, compile=False)
    model.compile(loss='categorical_crossentropy',optimizer="sgd",metrics=["accuracy", recall_m])
    return model

loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_model())]
model = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()

from lime import lime_image
explainer = lime_image.LimeImageExplainer()
