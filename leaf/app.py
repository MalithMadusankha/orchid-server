from flask import Flask, request, jsonify

import torch
from PIL import Image
import pathlib
import os

from service.imageService import make_predictions_type, make_predictions_disease

app = Flask(__name__)

pathlib.PosixPath = pathlib.WindowsPath
print("Current Working Directory:", os.getcwd())
model_type = torch.hub.load('ultralytics/yolov5', 'custom', path='type_predict.pt', force_reload=False)
model_disease = torch.hub.load('ultralytics/yolov5', 'custom', path='disease.pt', force_reload=False)
print("Available Classes : " , model_type.names)
print("Available Classes : " , model_disease.names)

@app.route('/growlight', methods=['POST'])
def grow_light():
    if 'file1' not in request.files:
        return jsonify({'error': 'No image provided'})

    image_file1 = request.files['file1']
    image_pil1 = Image.open(image_file1)

    result = {}
    Req_Light = 0

    try:
        prediction = make_predictions_type(image_pil1, confidence_threshold=0.1, model=model_type)

        if prediction["class"] == "Dendrobium":
            Req_Light = 100
        elif prediction["class"] == "Vanda":
            Req_Light = 200
        elif prediction["class"] == "phalaenopsis":
            Req_Light = 300
        else:
            pass

        result["results"] ={
            "header" : {
                "Orchid_Type" : prediction["class"],
                "Req_Light" : Req_Light
            }
        }
    except:
        result["results"] ={
            "header" : {
                "Orchid_Type" : "ERROR",
                "Req_Light" : 0
            }
        }

    print(result)
    return jsonify(result)


@app.route('/uvlight', methods=['POST'])
def upload_file_uv():
    if 'file1' not in request.files:
        return jsonify({'error': 'No image provided'})

    image_file1 = request.files['file1']
    image_pil1 = Image.open(image_file1)

    result = {}

    try:
        prediction = make_predictions_disease(image_pil1, confidence_threshold=0.1, model=model_disease)

        result["results"] ={
            "header" : {
                "Orchid_Type" : "",
                "Disease_Type": prediction["class"],
                "Fungicides": "",
            }
        }
    except:
        result["results"] ={
            "header" : {
                "Orchid_Type": "ERROR",
                "Disease_Type": "ERROR",
                "Fungicides":"ERROR",
            }
        }
    print(result)
    return jsonify(result)


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
