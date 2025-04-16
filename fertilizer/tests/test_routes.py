import pytest
from fastapi.testclient import TestClient
from main import app  # Import your FastAPI app
import os
from pathlib import Path

client = TestClient(app)

# Test data
TEST_IMAGE_PATH = Path("tests/test_images/test.jpg")  # Add a small test image

# def test_upload_images():
#     # Prepare test files
#     files = {
#         "file1": ("image1.jpg", open(TEST_IMAGE_PATH, "rb"), "image/jpeg"),
#         "file2": ("image2.jpg", open(TEST_IMAGE_PATH, "rb"), "image/jpeg"),
#         "file3": ("image3.jpg", open(TEST_IMAGE_PATH, "rb"), "image/jpeg"),
#     }
    
#     response = client.post("/features", files=files)
#     assert response.status_code == 200
#     assert "class_counts" in response.json()
    
#     # Close file handles
#     for f in files.values():
#         f[1].close()

def test_predict_growth():
    test_data = {
        "number_of_flowers": 10,
        "number_of_leaves": 20,
        "area_of_roots": 1234,  # in pixels
        "number_of_stems": 2,
        "img_url": "/results/result_1ebc5f6c-401b-44d3-bb22-4b100b200986.jpg"
    }
    
    response = client.post("/plant-growth", json=test_data)
    assert response.status_code == 200
    assert "prediction" in response.json()

def test_get_plant_growths():
    response = client.get("/plant-growths")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
