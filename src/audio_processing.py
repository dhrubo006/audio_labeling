import os
import random
import soundfile as sf
import librosa
import pandas as pd
import numpy as np


UPLOAD_FOLDER = "uploads"  # Assuming you have an 'uploads' folder to save the chunks



def process_audio(file_path):
    """
    Main function to process the provided audio file.
    """
    chunks = split_audio_into_chunks(file_path)
    chunks_with_emotions = assign_emotion_to_chunks(chunks)
    save_chunks_to_csv(chunks_with_emotions)


def split_audio_into_chunks(file_path):
    """
    Splits the provided audio file into 5-second chunks.
    """
    y, sr = librosa.load(file_path, sr=None)
    duration = librosa.get_duration(y=y, sr=sr)

    counter = 1
    chunks = []

    for start in range(0, int(duration), 5):
        end = start + 5
        y_chunk = y[start * sr : end * sr]
        chunk_filename = f"chunk{counter}.wav"
        chunk_path = os.path.join(UPLOAD_FOLDER, chunk_filename)
        sf.write(chunk_path, y_chunk, sr)

        chunks.append([f"clip{counter}", chunk_path])
        counter += 1

    return chunks


def assign_emotion_to_chunks(chunks):
    """
    Assigns a random emotion to each chunk.
    """
    for chunk in chunks:
        emotion = random.choice(["Happy", "Sad", "Elated", "Depressed"])
        chunk.append(emotion)
    return chunks


def save_chunks_to_csv(chunks_with_emotions):
    """
    Saves chunk details into a CSV file.
    """
    # Creating the dataframe with an additional user_label column initialized with NaN values
    df = pd.DataFrame(chunks_with_emotions, columns=["ID", "Location", "Emotion"])
    df["User_Label"] = np.nan
    
    # If the CSV file exists, concatenate the new chunks to the existing ones
    if os.path.exists("audio_clips.csv"):
        df_existing = pd.read_csv("audio_clips.csv")
        df = pd.concat([df_existing, df], ignore_index=True)
    
    # Saving the combined dataframe to CSV
    df.to_csv("audio_clips.csv", index=False)