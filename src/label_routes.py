import pandas as pd
from flask import request, redirect, url_for

def submit_labels():
    """
    Handles the submission of user labels for the audio chunks.

    When a user submits their emotion label for an audio chunk, 
    this function is triggered to save the label to the 'audio_clips.csv' file.
    """
    if request.method == 'POST':
        clipID = request.form.get('clipID')
        user_label = request.form.get(f'label{clipID}')

        df = pd.read_csv('audio_clips.csv')
        if 'User_Label' not in df.columns:
            df['User_Label'] = ''

        df = set_user_label(df, clipID, user_label)
        df.to_csv('audio_clips.csv', index=False)

        return redirect(url_for('review_audio_route'))


def set_user_label(df, clipID, user_label):
    """
    Update the provided DataFrame with the given user label for the specified clipID.
    """
    mask = df['ID'] == f'{clipID}'
    df.loc[mask, 'User_Label'] = user_label
    return df