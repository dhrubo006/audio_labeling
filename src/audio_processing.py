import os
import random
import soundfile as sf
import librosa
import pandas as pd
import numpy as np
from speechbrain.pretrained.interfaces import foreign_class


UPLOAD_FOLDER = "uploads"  # Assuming you have an 'uploads' folder to save the chunks

# Global setup for the classifier
classifier = foreign_class(
    source="speechbrain/emotion-recognition-wav2vec2-IEMOCAP",
    pymodule_file="custom_interface.py",
    classname="CustomEncoderWav2vec2Classifier",
)


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
    Assigns an emotion to each chunk using SpeechBrain's classifier.
    """
    for chunk in chunks:
        _, _, _, emotion = classifier.classify_file(chunk[1])  # chunk[1] is the path of the chunk
        chunk.append(emotion[0])  # append the detected emotion
    return chunks


def save_chunks_to_csv(chunks_with_emotions):
    """
    Saves chunk details into a CSV file.
    """
    # Creating the dataframe with an additional user_label column initialized with NaN values
    df = pd.DataFrame(chunks_with_emotions, columns=["ID", "Location", "Emotion"])

    # If the CSV file exists, concatenate the new chunks to the existing ones
    if os.path.exists("audio_clips.csv"):
        df_existing = pd.read_csv("audio_clips.csv")
        df = pd.concat([df_existing, df], ignore_index=True)

    # Saving the combined dataframe to CSV
    df.to_csv("audio_clips.csv", index=False)
