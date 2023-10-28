from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from src.audio_processing import process_audio
from src.audio_routes import review_audio, uploaded_file
from src.label_routes import submit_labels
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"  # Assuming you have an 'uploads' folder to save the chunks
ALLOWED_EXTENSIONS = {"wav", "mp3", "aac", "ogg", "flac"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    """
    Checks if the provided filename has a valid extension.

    This function takes a filename string and checks if it has an extension
    that matches one of the extensions in the ALLOWED_EXTENSIONS set. It's used
    to ensure that users can only upload audio files with the desired formats
    to the application.

    Args:
    - filename (str): The name of the file to check.

    Returns:
    - bool: True if the file has an allowed extension, False otherwise.
    """

    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Serves the main page and handles the audio file uploads.

    This function is linked to the root URL of the Flask application.
    If accessed via a GET request, it simply renders the main page
    (presumably with an upload form). If accessed via a POST request
    (e.g., when a user uploads a file), it handles the file upload process,
    checks if the file has a valid extension using the allowed_file function,
    saves the file, processes it using the process_audio function from the
    audio_processing module, and then sends a response to the user.

    Returns:
    - str: A message indicating the result of the operation. This can be
           customized further based on the application's needs.
    """

    if request.method == "POST":
        file = request.files["file"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            process_audio(filepath)
            return "Audio processed and saved to CSV!"
    return render_template("index.html")


@app.route("/review_audio", methods=["GET", "POST"])
def review_audio_route():
    return review_audio()

@app.route('/uploads/<filename>', methods=['GET'])
def uploaded_file_route(filename):
    return uploaded_file(filename, UPLOAD_FOLDER)


@app.route('/submit_labels', methods=['POST'])
def submit_labels_route():
    return submit_labels()


if __name__ == "__main__":
    app.run(debug=True)
