import os, csv, pathlib
from pydub import AudioSegment

import numpy as np
import librosa
import youtube_dl


def timestamps(total_time, split=2500):

    """
    Provides the proper indeces to split audio clip into smaller pieces
    split default: 2500 ms
    """

    iters = int(total_time/split)
    for i in range(1, iters + 1):
        yield (i-1)*split, i * split, i





header = 'filename chroma_stft rmse spectral_centroid spectral_bandwidth rolloff zero_crossing_rate'
for i in range(1, 21):
    header += f' mfcc{i}'
header += ' label'
header = header.split()


"""

to see full header:

from supervisor.util import header
print(header)

"""



def download_youtube_audio(url, title, destination="audio", split=2500, keep_mp3=True, blurb="FULL_AUDIO"):

    """

    Will downlaod the mp3 from youtube, convert to .wav and then split into segments

    FFMPEG MUST BE INSTALLED

    url: video url (includeing https)
    title: what audio should be named
    destination: directory where all files are located default=audio
    split: split duration in ms default=2500
    keep_mp3: wether to keep mp3 file or delete it (NOT IMPLEMENTED)
    blurb: where full interview is held default=FULL_AUDIO


    return: path at which cut audio is located

    usage:

    from supervisor.util import download_youtube_audio
    download_youtube_audio("https://www.youtube.com/watch?v=3HlPkRNNLh8", "sleep")

    >> 'audio/sleep'

    tree:

    ───audio
        ├───FULL_INTERVIEWS
        └───sleep
    """



    pathlib.Path(f'{destination}').mkdir(parents=True, exist_ok=True)


    ydl_opts = {
        'outtmpl': os.path.join(destination, blurb, f"{title}.mp3"),
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'prefer_ffmpeg': True,

    }


    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"{url}"])

    sound = AudioSegment.from_file(os.path.join(destination, blurb, f"{title}.mp3"))
    sound.export(os.path.join(destination, blurb, f"{title}.wav"), format="wav")
    

    pathlib.Path(os.path.join(destination, title)).mkdir(parents=True, exist_ok=True)

    newAudio = AudioSegment.from_wav(os.path.join(destination, blurb, f"{title}.wav"))

    for start, end, val in timestamps(len(newAudio), split):
        cutAudio = newAudio[start:end]
        cutAudio.export(os.path.join(destination, title, f"{title}_{val-1}.wav"), format='wav')

    return os.path.join(destination, title)




def split_audio(path, destination, title=None, split=2500, format='wav'):

    """

    splits audio file into smaller even samples

    """

    return




def dataset_from_segments(path, title, destination='datasets', header=header):

    """
    
    create dataset based on chopped samples

    path: location of directory containing chopped samples
    title: desired title of dataset
    destination: location to store dataset, will be created if non-existent default=datasets
    header: desired labels of columns (do not change)

    returns location of dataset

    usage: 

    from supervisor.util import dataset_from_segments
    dataset_from_segments('audio/sleep', 'sleep')

    >> 'datasets\\sleep.csv'

    """



    pathlib.Path(f'{destination}').mkdir(parents=True, exist_ok=True)

    file = open(os.path.join(destination, f"{title}.csv"), 'w', newline='')

    with file:
        writer = csv.writer(file)
        writer.writerow(header)


    for filename in os.listdir(f'{path}'):
        songname = os.path.join(path, filename)
        y, sr = librosa.load(songname, mono=True)

        rmse = librosa.feature.rms(y=y) #root mean squred ENERGY note. changed to rms form rmse
        chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
        spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        zcr = librosa.feature.zero_crossing_rate(y)
        mfcc = librosa.feature.mfcc(y=y, sr=sr)

        to_append = f'{filename} {np.mean(chroma_stft)} {np.mean(rmse)} {np.mean(spec_cent)} {np.mean(spec_bw)} {np.mean(rolloff)} {np.mean(zcr)}'

        for e in mfcc:
            to_append += f' {np.mean(e)}'

        to_append += f' {title}'

        file = open(os.path.join(destination, f"{title}.csv"), 'a', newline='')
        with file:
            writer = csv.writer(file)
            writer.writerow(to_append.split())

    
    return os.path.join(destination, f"{title}.csv")