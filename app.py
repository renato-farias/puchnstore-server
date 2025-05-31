import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash


UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
HTTP_HOST = os.getenv("HTTP_HOST", "localhost")
HTTP_PORT = int(os.getenv("HTTP_PORT", 8080))
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "pushnstore")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "pushnstore")
SECURE_FILENAME = int(os.getenv("SECURE_FILENAME", 1))


app = Flask(__name__)


os.makedirs(UPLOAD_FOLDER, exist_ok=True)


auth = HTTPBasicAuth()


users = {
    ADMIN_USERNAME: generate_password_hash(ADMIN_PASSWORD)
}


def ensure_dir_exist(file_path: str):
    """
    Creates all necessary directories in the given file path if they don't exist.

    Parameters:
    - file_path (str): Full path to the file (including filename).

    Example:
    ensure_dir_exist("/path/to/some/folder/file.txt")
    """
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username


@app.route("/upload", methods=["PUT"])
@auth.login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    filename = file.filename
    if SECURE_FILENAME == 1:
        filename = secure_filename(file.filename)

    filepath = os.path.join(UPLOAD_FOLDER, filename)
    ensure_dir_exist(filepath)
    file.save(filepath)

    return jsonify({"message": f"File {filename} uploaded successfully"}), 200


if __name__ == "__main__":
    app.run(host=HTTP_HOST, port=HTTP_PORT)
