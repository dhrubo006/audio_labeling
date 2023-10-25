from flask import Flask, request, render_template, redirect, url_for,  send_from_directory
from werkzeug.utils import secure_filename
from src.audio_processing import process_audio
import pandas as pd
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
def review_audio():

    """
    Serves the 'review_audio' page where users can listen to the audio chunks and 
    label their perceived emotion from the audio. Each audio chunk can be played 
    directly from the page and is accompanied by a system-generated emotion label.
    
    The user is presented with a dropdown menu to submit their own label. Upon 
    submission, a confirmation dialog appears. If confirmed, the user's label is 
    saved to the CSV file and the audio entry is removed from the page.

    Returns:
        render_template: Renders the 'review_audio.html' template with audio clip data.
    """

    # Reading from the CSV file
    df = pd.read_csv("audio_clips.csv")
    audio_clips = df.to_dict(orient="records")

    return render_template("review_audio.html", audio_clips=audio_clips)


@app.route('/uploads/<filename>', methods=['GET'])
def uploaded_file(filename):
    """
    Serves uploaded audio files to the frontend when requested. This allows the 
    frontend audio player to play the uploaded audio chunks. The function fetches 
    the audio file based on the filename provided in the URL and sends it as a 
    response.

    Parameters:
        filename (str): Name of the audio file to be served.

    Returns:
        send_from_directory: Serves the requested audio file from the UPLOAD_FOLDER.
    """
    return send_from_directory(UPLOAD_FOLDER, filename)



@app.route('/submit_labels', methods=['POST'])
def submit_labels():

    """
    Handles the submission of user labels for the audio chunks. When a user submits 
    their emotion label for an audio chunk, this function is triggered to save 
    the label to the 'audio_clips.csv' file.

    It first loads the CSV into a DataFrame. Then, it checks for the 'User_Label' 
    column and creates it if absent. Subsequently, it updates the user's label 
    for the respective audio chunk in the DataFrame and saves the changes back 
    to the CSV file.

    Returns:
        redirect: Redirects the user back to the 'review_audio' route.
    """

    df = pd.read_csv('audio_clips.csv')

    # Check if 'User_Label' column exists, if not, create it.
    if 'User_Label' not in df.columns:
        df['User_Label'] = ''

    clipID = request.form.get('clipID')
    user_label = request.form.get(f'label{clipID}')

    # Update the specific row's 'User_Label' column in the DataFrame
    df.loc[df['ID'] == f'clip{clipID}', 'User_Label'] = user_label

    # Save the updated DataFrame back to the CSV file
    df.to_csv('audio_clips.csv', index=False)

    return redirect(url_for('review_audio'))





if __name__ == "__main__":
    app.run(debug=True)
