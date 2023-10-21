import os
from flask import render_template


def label_renderer(app_obj):
    """
    routing to the page of labelling with required params

    arg:
        app : is the flask object

    output:
        render the template

    """
    files = os.listdir(app_obj.config["UPLOAD_DIRECTORY"])
    audio_files = []

    for file_ in files:
        if os.path.splitext(file_)[1].lower() in app_obj.config["ALLOWED_EXTENSIONS"]:
            audio_files.append(file_)

    return render_template("audio_labeling.html", audio_files=audio_files)
