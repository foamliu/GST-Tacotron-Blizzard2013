import librosa
import os
import config as hp
from tqdm import tqdm

if __name__ == "__main__":
    files = [f for f in os.listdir(hp.wav_folder) if f.endswith('.wav')]
    files = [os.path.join(hp.wav_folder, f) for f in files]
    print('num_files: ' + str(len(files)))

    total_duration = 0

    for file in tqdm(files):
        y, sr = librosa.load(file)
        duration = librosa.get_duration(y, sr)
        total_duration += duration

    print('total_duration: ' + str(total_duration))
