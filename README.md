# pushnstore-server 🚀

A lightweight Flask API to receive and store files via HTTP PUT requests — with built-in authentication and simplicity.

## 🔧 Features

- Upload files via `/upload` endpoint
- Basic authentication (username & password)
- Saves files to disk (default: `uploads/` folder)
- Easy to run and extend

## 📁 API Usage

### Endpoint

`PUT /upload`

### Auth

Basic Authentication required:

```config
username: pushnstore
password: pushnstore
```

🐳 Run with Docker
You can run the API in a container using Docker:

1. Build the Docker image
```bash
docker build -t rcdfs/pushnstore-server:dev -f Dockerfile .
```

2. Run the container
```bash
docker run -ti --rm -p 8080:8080 rcdfs/pushnstore-server:dev
```

This will start the server at http://localhost:8080. You can now test it using the client or curl.

### Code Example

```python
import requests
from requests.auth import HTTPBasicAuth

API_URL = 'http://localhost:8080/upload'
USERNAME = 'admin'
PASSWORD = 'password123'
FILE_PATH = 'example.txt'

with open(FILE_PATH, 'rb') as f:
    files = {'file': (FILE_PATH, f)}
    response = requests.put(API_URL, files=files, auth=HTTPBasicAuth(USERNAME, PASSWORD))

print(f'Status: {response.status_code}')
print(response.json())
```
