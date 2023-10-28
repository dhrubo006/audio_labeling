import pandas as pd
from flask import render_template, send_from_directory

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

    # Filtering the DataFrame to only include rows where 'user_label' is NaN (not available)
    df_filtered = df[pd.isna(df['User_Label'])]

    audio_clips = df_filtered.to_dict(orient="records")
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
