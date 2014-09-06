import unittest
import sys
import os
sys.path.append(sys.path[0][:-6] + "/src")
from pymplayer import MusicPlayer
import numpy as np


class TestMusicPlayer(unittest.TestCase):
    testFilePath = sys.path[0][:-6] +\
        "/files/Halogen - Length and Brecht Synaecide Remix.mp3"

    def testImportSong(self):
        testMixer = MusicPlayer()
        testMixer.importFile(self.testFilePath)
        self.assertTrue(testMixer.soundPath != '')

    def testPlaySong(self):
        self.assertFalse(MusicPlayer().play())  # Before import.
        testMixer = MusicPlayer()
        testMixer.importFile(self.testFilePath)
        testMixer.stop()
        testMixer.play()
        self.assertTrue(testMixer.getCond() == 1)

    def testStopSong(self):
        testMixer = MusicPlayer()
        testMixer.importFile(self.testFilePath)
        testMixer.play()
        testMixer.stop()
        self.assertTrue(testMixer.getCond() == 0)

    def testCutting(self):
        testMixer = MusicPlayer()
        testMixer.importFile(self.testFilePath)
        testMixer.cut(startingPos=0, endingPos=10,
                      filePathAndName=self.testFilePath[:-4],
                      startLulling=False, endLulling=False)
        assert os.path.exists(self.testFilePath[:-4] + " (Splitted).mp3")

    def testConcatenating(self):
        testMixer = MusicPlayer()
        testMixer.importFile(self.testFilePath)
        testMixer.concat(leftTune=self.testFilePath,
                         rightTune=self.testFilePath,
                         songWritePath=self.testFilePath[:-4])
        assert os.path.exists(self.testFilePath[:-4] + " (Concatenated).mp3")

    def testNumpyArrayGeneration(self):
        testMixer = MusicPlayer()
        testMixer.importFile(self.testFilePath)
        self.assertTrue(testMixer.soundToArray(
            filePath=self.testFilePath).size)
