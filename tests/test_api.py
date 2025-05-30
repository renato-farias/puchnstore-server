import os
import io
import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_upload_success(client):
    data = {
        "file": (io.BytesIO(b"Hello, world!"), "hello.txt")
    }
    response = client.put(
        "/upload",
        data=data,
        content_type="multipart/form-data",
        headers={
            "Authorization": "Basic cHVzaG5zdG9yZTpwdXNobnN0b3Jl"  # base64(pushnstore:pushnstore)
        }
    )
    assert response.status_code == 200
    assert "uploaded successfully" in response.json["message"]
    assert os.path.exists(os.path.join("uploads", "hello.txt"))
    os.remove(os.path.join("uploads", "hello.txt"))  # Cleanup


def test_upload_no_file(client):
    response = client.put(
        "/upload",
        data={},
        content_type="multipart/form-data",
        headers={
            "Authorization": "Basic cHVzaG5zdG9yZTpwdXNobnN0b3Jl"
        }
    )
    assert response.status_code == 400
    assert response.json["error"] == "No file part in the request"

def test_upload_unauthenticated(client):
    response = client.put("/upload", data={})
    assert response.status_code == 401
