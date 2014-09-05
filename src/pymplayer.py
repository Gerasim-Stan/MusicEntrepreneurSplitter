from os import path
from pygame import mixer
from pydub import AudioSegment
import numpy as np
import subprocess as sp


class MusicPlayer:
    main_mixer = mixer
    sound_path = ""

    def __init__(self):
        MusicPlayer.main_mixer.init()

    def importFile(self, file_path):
        if(path.isfile(file_path) and file_path[-4:] == ".mp3"):
            MusicPlayer.sound_path = file_path
            MusicPlayer.main_mixer.music.load(file_path)
            return

    def play(self):
        try:
            MusicPlayer.main_mixer.music.stop()
        except:
            pass
        MusicPlayer.main_mixer.music.play()

    def pause(self):
        MusicPlayer.main_mixer.music.pause()

    def stop(self):
        MusicPlayer.main_mixer.music.stop()

    def unpause(self):
        MusicPlayer.main_mixer.music.unpause()

    def setPlayPosition(self, position):
        MusicPlayer.main_mixer.music.set_pos(position)

    def setVolume(self, value):
        MusicPlayer.main_mixer.music.set_volume(value)

    def getCond(self):
        return MusicPlayer.main_mixer.music.get_busy()

    def getLength(self):
        sound = AudioSegment.from_mp3(MusicPlayer.sound_path)
        return sound.duration_seconds

    def cut(self, starting_p, ending_p, filePathAndName,
            startLulling, endLulling):
        sound = AudioSegment.from_mp3(MusicPlayer.sound_path)
        splitted_sound = sound[starting_p*1000:ending_p * 1000]
        if startLulling:
            splitted_sound = splitted_sound.fade_in(4000)
        if endLulling:
            splitted_sound = splitted_sound.fade_out(4000)
        splitted_sound.export(filePathAndName + " (Splitted).mp3")

    def concat(self, leftTune, rightTune, songWritePath):
        sound1 = AudioSegment.from_mp3(leftTune)
        sound2 = AudioSegment.from_mp3(rightTune)
        final_sound = sound1 + sound2
        final_sound.export(songWritePath + " (Concatenated).mp3")

    def soundToArray(self, filePath=sound_path):
        command = ["ffmpeg", '-i', filePath, '-f', 's16le', '-acodec',
                   'pcm_s16le', '-ar', '44100', '-ac', '2', '-']
        pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10**8)
        raw_audio = pipe.stdout.read(88200*4)
        audio_array = np.fromstring(raw_audio, dtype="int16")
        audio_array = audio_array.reshape((len(audio_array)/2, 2))

        return audio_array
