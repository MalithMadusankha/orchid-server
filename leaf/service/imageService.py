import cv2
import numpy as np


def resize_image(img, target_size=(416, 416)):
    img_copy = np.copy(img)
    return cv2.resize(img_copy, target_size)

def make_predictions_type(img, confidence_threshold=0.1, model=None):
    results = model(resize_image(img))
    predictions = results.xyxy[0].cpu().numpy()

    class_predictions = {}

    for pred in predictions:
        class_index = int(pred[5])
        confidence = pred[4]

        if confidence >= confidence_threshold:
            if class_index not in class_predictions or confidence > class_predictions[class_index]['confidence']:
                class_predictions[class_index] = {
                    'class': model.names[class_index],
                    'confidence': confidence
                }

    return_list = []

    for class_index, pred in class_predictions.items():
        return_list.append({
            'class': pred['class'],
            'confidence': float(pred['confidence'])
        })

    highest_confidence_entry = max(class_predictions.values(), key=lambda x: x['confidence'], default=None)

    highest_confidence_entry['confidence'] = float(highest_confidence_entry['confidence'])

    return highest_confidence_entry


def make_predictions_disease(img, confidence_threshold=0.1, model=None):
    results = model(resize_image(img))
    predictions = results.xyxy[0].cpu().numpy()

    class_predictions = {}

    for pred in predictions:
        class_index = int(pred[5])
        confidence = pred[4]

        if confidence >= confidence_threshold:
            if class_index not in class_predictions or confidence > class_predictions[class_index]['confidence']:
                class_predictions[class_index] = {
                    'class': model.names[class_index],
                    'confidence': confidence
                }

    return_list = []

    for class_index, pred in class_predictions.items():
        return_list.append({
            'class': pred['class'],
            'confidence': float(pred['confidence'])
        })

    highest_confidence_entry = max(class_predictions.values(), key=lambda x: x['confidence'], default=None)

    highest_confidence_entry['confidence'] = float(highest_confidence_entry['confidence'])

    return highest_confidence_entry