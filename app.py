from flask import Flask, send_from_directory, jsonify
from src.label_renderer import label_renderer
import random


app = Flask(__name__)
app.config["UPLOAD_DIRECTORY"] = "uploads/"
app.config["ALLOWED_EXTENSIONS"] = [".wav", ".mp3", ".aac", ".ogg", ".flac"]
# A list of possible labels
labels = ['happy', 'sad', 'depressed']



@app.route("/label")
def label():
    return label_renderer(app)


@app.route("/play_audio/<filename>", methods=["GET"])
def play_audio(filename):
    return send_from_directory(app.config["UPLOAD_DIRECTORY"], filename)


@app.route('/get_random_label', methods=['GET'])
def get_random_label():
    # Select a random label from the list
    random_label = random.choice(labels)
    
    # Return the selected label as a JSON response
    response_data = {'label': random_label}
    
    return jsonify(response_data)




if __name__ == "__main__":
    app.run(debug=True)
