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
    # Test data with all required fields
    test_data = {
        "number_of_flowers": 10,
        "number_of_leaves": 20,
        "area_of_roots": 1234,  # in pixels
        "number_of_stems": 2,
        "img_url": "/results/result_1ebc5f6c-401b-44d3-bb22-4b100b200986.jpg"
    }
    
    # Make the API request
    response = client.post("/plant-growth", json=test_data)
    
    # Verify response structure
    assert response.status_code == 200
    response_data = response.json()
    
    # Check if response has the expected structure
    assert isinstance(response_data, dict)
    assert "predicted_class" in response_data  # Top-level field
    assert isinstance(response_data["predicted_class"], int)  # Verify type
    
    # Optional: Check for additional fields if your API returns them
    if "confidence" in response_data:
        assert isinstance(response_data["confidence"], float)

def test_get_plant_growths():
    # Make the API request
    response = client.get("/plant-growths")
    
    # Verify response structure
    assert response.status_code == 200
    response_data = response.json()
    
    # Check if response has the expected wrapper structure
    assert isinstance(response_data, dict)
    assert "data" in response_data  # Check for data wrapper
    assert isinstance(response_data["data"], list)  # Verify data is a list
    
    # If list is not empty, verify item structure
    if len(response_data["data"]) > 0:
        sample_item = response_data["data"][0]
        assert "_id" in sample_item  # Check for required fields
        assert "fertilizer_recommendation" in sample_item
        assert isinstance(sample_item["fertilizer_recommendation"], dict)