import unittest
import os

from audiocat.utils import (
    download_youtube_audio,
    split_audio,
    dataset_from_segments
)


class UtilTest(unittest.TestCase):

    def test_download_youtube_audio(self):
        x= download_youtube_audio("https://www.youtube.com/watch?v=3HlPkRNNLh8", "sleep")
        self.assertNotEqual(x, None)


    def test_split_audio(self):
        x = split_audio('audio/FULL_AUDIO/sleep.wav', 'audio/sleepcut', 'sleep')
        self.assertNotEqual(x, None)

    def test_dataset_from_segmetns(self):
        x= dataset_from_segments('audio/sleep', 'sleep')
        self.assertNotEqual(x, None)



if __name__ == '__main__':
    unittest.main()