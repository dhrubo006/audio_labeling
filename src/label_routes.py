import pandas as pd
from flask import request, redirect, url_for


def submit_labels():
    """
    Handles the submission of user labels for the audio chunks.

    When a user submits their emotion label for an audio chunk,
    this function is triggered to save the label to the 'audio_clips.csv' file.
    Then it calls the check_labels_match to compare the user label and system label
    """
    if request.method == "POST":
        clipID = request.form.get("clipID")
        user_label = request.form.get(f"label{clipID}")

        df = pd.read_csv("audio_clips.csv")
        if "User_Label" not in df.columns:
            df["User_Label"] = ""

        df = set_user_label(df, clipID, user_label)
        df.to_csv("audio_clips.csv", index=False)

        result = check_labels_match(clipID)
        if result:
            print("User label matches the system emotion for this clip!")
        else:
            print("Mismatch between user label and system emotion for this clip.")

        return redirect(url_for("review_audio_route"))


def set_user_label(df, clipID, user_label):
    """
    Update the provided DataFrame with the given user label for the specified clipID.
    """
    mask = df["ID"] == f"{clipID}"
    df.loc[mask, "User_Label"] = user_label
    return df



def check_labels_match(clipID):
    """
    Compares the User_Label and Emotion for a specific clipID in the 'audio_clips.csv' file.
    
    Parameters:
        clipID (str): The ID of the clip to check.
    
    Returns:
        bool: True if the User_Label matches the Emotion for the given clipID, False otherwise.
    """
    # Read the CSV
    df = pd.read_csv("audio_clips.csv")
    
    # Fetch the specific row based on clipID
    clip_data = df[df["ID"] == clipID]
    
    # If no data is found for the clipID, return False
    if clip_data.empty:
        print(f"No data found for clipID: {clipID}")
        return False

    # Compare User_Label and Emotion for the clip and return the result
    return clip_data.iloc[0]["User_Label"] == clip_data.iloc[0]["Emotion"]






