import pandas as pd
from flask import render_template, send_from_directory
import os


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

    # Reading from the audio_clips.csv file
    df_audio = pd.read_csv("audio_clips.csv")

    # Check if review_clips.csv exists
    if not os.path.exists("review_clips.csv"):
        # If it doesn't exist, create it with specified columns
        df_review = pd.DataFrame(columns=["ID", "Location", "Emotion", "User_Label"])
        df_review.to_csv("review_clips.csv", index=False)
    else:
        # If it exists, read its content
        df_review = pd.read_csv("review_clips.csv")

    # Find clips that are in df_audio but not in df_review
    unmatched_clips = df_audio[~df_audio["ID"].isin(df_review["ID"])]

    audio_clips = unmatched_clips.to_dict(orient="records")
    return render_template("review_audio.html", audio_clips=audio_clips)


def uploaded_file(filename, UPLOAD_FOLDER):
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
