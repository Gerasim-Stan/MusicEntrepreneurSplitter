from os import path
from pygame import mixer
from pydub import AudioSegment
import numpy as np
import subprocess as sp


class MusicPlayer:
    """Defines and implements functions for control of music player,
       and editing music.
    """
    mainMixer = mixer
    soundPath = ""

    def __init__(self):
        MusicPlayer.mainMixer.init()

    def importFile(self, filePath):
        """Provides tools for importing of file"""
        if(path.isfile(filePath) and filePath[-4:] == ".mp3"):
            MusicPlayer.soundPath = filePath
            MusicPlayer.mainMixer.music.load(filePath)
            return

    def play(self):
        """Plays loaded tune"""
        try:
            MusicPlayer.mainMixer.music.stop()
        except:
            pass
        MusicPlayer.mainMixer.music.play()

    def pause(self):
        """Pauses playing tune"""
        MusicPlayer.mainMixer.music.pause()

    def stop(self):
        """Stops playing tune"""
        MusicPlayer.mainMixer.music.stop()

    def unpause(self):
        """Unpauses paused tune"""
        MusicPlayer.mainMixer.music.unpause()

    def setPlayPosition(self, position):
        """Sets position for the tune to start"""
        MusicPlayer.mainMixer.music.set_pos(position)

    def setVolume(self, value):
        """Sets volume in range [0, 1]"""
        MusicPlayer.mainMixer.music.set_volume(value)

    def getCond(self):
        """Gets current condition of the player"""
        return MusicPlayer.mainMixer.music.get_busy()

    def getLength(self):
        """Gets length of the current loaded tune"""
        sound = AudioSegment.from_mp3(MusicPlayer.soundPath)
        return sound.duration_seconds

    def cut(self, startingPos, endingPos, filePathAndName,
            startLulling, endLulling):
        """Cuts mp3 file in range [starting Pos, endingPos],
           and eventually fades in the beginning or the end"""
        sound = AudioSegment.from_mp3(MusicPlayer.soundPath)
        splittedSound = sound[startingPos*1000:endingPos * 1000]
        if startLulling:
            splittedSound = splittedSound.fade_in(4000)
        if endLulling:
            splittedSound = splittedSound.fade_out(4000)
        splittedSound.export(filePathAndName + " (Splitted).mp3")

    def concat(self, leftTune, rightTune, songWritePath):
        """Concatenates two tunes, and writes the result at given directory"""
        sound1 = AudioSegment.from_mp3(leftTune)
        sound2 = AudioSegment.from_mp3(rightTune)
        finalSound = sound1 + sound2
        finalSound.export(songWritePath + " (Concatenated).mp3")

    def soundToArray(self, filePath=soundPath):
        """Converts the loaded mp3 file to numpy array"""
        command = ["ffmpeg", '-i', filePath, '-f', 's16le', '-acodec',
                   'pcm_s16le', '-ar', '44100', '-ac', '2', '-']
        pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10**8)
        rawAudio = pipe.stdout.read(88200*4)
        audioArray = np.fromstring(rawAudio, dtype="int16")
        audioArray = audioArray.reshape((len(audioArray)/2, 2))

        return audioArray
