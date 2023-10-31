import pandas as pd
from flask import request, redirect, url_for


def submit_labels():
    """
    Handles the submission of user labels for the audio chunks.

    When a user submits their emotion label for an audio chunk,
    this function is triggered to save the label to the 'review_clips.csv' file.
    Then it calls the compare_labels to compare the user label and system label.
    """
    if request.method == "POST":
        clipID = request.form.get("clipID")
        user_label = request.form.get(f"label{clipID}")

        audio_df = pd.read_csv("audio_clips.csv")
        clip_data = audio_df[audio_df["ID"] == clipID]

        # If no data is found for the clipID, print a message
        if clip_data.empty:
            print(f"No data found for clipID: {clipID}")
            return redirect(url_for("review_audio_route"))

        # Append clip_data with the User_Label to review_clips.csv
        append_to_review(clip_data, user_label)

        result = compare_labels(clipID)
        if result:
            print("User label matches the system emotion for this clip!")
        else:
            print("Mismatch between user label and system emotion for this clip.")

        return redirect(url_for("review_audio_route"))


def append_to_review(clip_data, user_label):
    """
    Append the provided clip data along with the User_Label to the 'review_clips.csv' file.
    """
    clip_data = clip_data.copy()  # Ensure we're working on a copy, not a view
    clip_data["User_Label"] = user_label

    review_file = "review_clips.csv"
    if not pd.io.common.file_exists(review_file):
        clip_data.to_csv(review_file, index=False)
    else:
        review_df = pd.read_csv(review_file)
        review_df = pd.concat([review_df, clip_data], ignore_index=True)
        review_df.to_csv(review_file, index=False)


def compare_labels(clipID):
    """
    Compares the User_Label and Emotion for a specific clipID in the 'audio_clips.csv' file.

    Parameters:
        clipID (str): The ID of the clip to check.

    Returns:
        bool: True if the User_Label matches the Emotion for the given clipID, False otherwise.
    """
    # Read the CSV
    df = pd.read_csv("review_clips.csv")

    # Fetch the specific row based on clipID
    clip_data = df[df["ID"] == clipID]

    # If no data is found for the clipID, return False
    if clip_data.empty:
        print(f"No data found for clipID: {clipID}")
        return False

    # Compare User_Label and Emotion for the clip and return the result
    return clip_data.iloc[0]["User_Label"] == clip_data.iloc[0]["Emotion"]
