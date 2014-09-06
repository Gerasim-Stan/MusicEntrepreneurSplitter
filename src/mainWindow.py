import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from pymplayer import *
import os
import matplotlib
import pylab
import numpy as np
import scipy
import matplotlib.pyplot as plt
from scipy import ndimage
import wand.image as Image

mainPlayer = MusicPlayer()


class MainWindow(QMainWindow):
    """Defines view for the main window of the app,
       and instantiates other objects for the GUI.
    """
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.resize(1030, 530)
        self.move(200, 100)
        self.mainImage = sys.path[0][:-4] + "/files/backgroundForPlayer.jpg"
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(self.mainImage)))
        self.setPalette(palette)
        self.setWindowTitle("Music Entrepreneur Splitter")
        self.songLength = 0
        self.addTime = 0
        self.saveDirectory = ""
        self.playImagePath = sys.path[0][:-4] + "/files/play.png"
        self.pauseImagePath = sys.path[0][:-4] + "/files/pause.png"
        self.stopImagePath = sys.path[0][:-4] + "/files/stop.png"

        self.addLullingPartWidget = LullingPartWidget(self)
        self.addCutEndWidget = CutEndWidget(self)
        self.addPlayButtonWidget = PlayButtonWidget(self)
        self.addTuneListWidget = TuneListWidget(self)
        self.addOpenFileWidget = OpenFileWidget(self)
        self.addSoundSliderWidget = SoundSliderWidget(self)
        self.addTimerWidget = TimerWidget(self)
        self.addStopButtonWidget = StopButtonWidget(self)
        self.addCutStartWidget = CutStartWidget(self)
        self.addCutButtonWidget = CutButtonWidget(self)
        self.addConcatenateTunesWidget = ConcatenateTunesWidget(self)
        self.show()


class PlayButtonWidget(QWidget):
    """Defines behaviour for play button"""
    iconSetter = 0

    def __init__(self, parent):

        super(PlayButtonWidget, self).__init__(parent)
        self.setGeometry(0, 340, 120, 100)
        self.layout = QVBoxLayout(self)
        self.playButton = QPushButton(self)
        self.playButton.setSizePolicy(QSizePolicy.Expanding,
                                      QSizePolicy.Expanding)
        self.playButton.setIcon(QIcon(parent.playImagePath))
        self.playButton.setIconSize(QSize(80, 80))
        self.playButton.clicked.connect(self.playControl)
        self.show()
        self.layout.addWidget(self.playButton)
        self.parent = parent

    def playControl(self):
        """Defines behaviour after clicking instantiated play/pause button"""
        if mainPlayer.getCond() == 0:
            return
        if self.iconSetter == 1:
            self.playButton.setIcon(QIcon(self.parent.playImagePath))
            self.iconSetter = 0
            mainPlayer.pause()
        else:
            self.playButton.setIcon(QIcon(self.parent.pauseImagePath))
            self.iconSetter = 1
            if mainPlayer.getCond() != 0:
                mainPlayer.unpause()
            else:
                mainPlayer.play()


class StopButtonWidget(QWidget):
    """Defines behaviour for stop button"""
    def __init__(self, parent):

        super(StopButtonWidget, self).__init__(parent)
        self.setGeometry(105, 340, 120, 100)
        self.layout = QVBoxLayout(self)
        self.stopButton = QPushButton(self)
        self.stopButton.setSizePolicy(QSizePolicy.Expanding,
                                      QSizePolicy.Expanding)
        self.stopButton.setIcon(QIcon(parent.stopImagePath))
        self.stopButton.setIconSize(QSize(80, 80))
        self.stopButton.clicked.connect(self.stopControl)
        self.show()
        self.layout.addWidget(self.stopButton)
        self.parent = parent

    def stopControl(self):
        """Defines behaviour after clicking instantiated stop button"""
        self.parent.addPlayButtonWidget.iconSetter = 0
        self.parent.addPlayButtonWidget.playButton.setIcon(
            QIcon(self.parent.playImagePath))
        mainPlayer.stop()
        if hasattr(self.parent.addTuneListWidget, "timer"):
            self.parent.addTuneListWidget.timer.stop()


class OpenFileWidget(QWidget):
    """Define view for button, used for loading of files"""
    def __init__(self, parent):

        super(OpenFileWidget, self).__init__(parent)
        self.setGeometry(100, 445, 90, 60)
        self.layout = QVBoxLayout(self)
        self.openFileButton = QPushButton("Add", self)
        self.openFileButton.setSizePolicy(QSizePolicy.Expanding,
                                          QSizePolicy.Expanding)
        self.openFileButton.clicked.connect(
            parent.addTuneListWidget.searchAndOpenFile)
        self.openFileButton.setStyleSheet(
            "QPushButton { font: 14pt; font-weight:420;}")
        self.show()
        self.layout.addWidget(self.openFileButton)


class SoundSliderWidget(QWidget):
    """Defines view and behaviour of slider for volume control"""
    def __init__(self, parent):

        super(SoundSliderWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.setGeometry(746, 330, 100, 200)
        self.slider = QSlider(Qt.Vertical, self)
        self.slider.setFocusPolicy(Qt.NoFocus)
        self.show()
        self.layout.addWidget(self.slider)
        self.slider.valueChanged.connect(self.setVolume)
        self.slider.setValue(int(self.slider.maximum() / 2) + 1)
        self.slider.setTickPosition(3)
        self.slider.setSingleStep(25)

    def setVolume(self):
        """Sets volume level"""
        mainPlayer.setVolume(
            value=self.slider.value() / self.slider.maximum())


class TuneListWidget(QListWidget):
    """ This class defines behaviour for the list of tunes.
        Mainly, it controls the events, and draws sound graphics
    """
    fileNames = {}

    def __init__(self, parent):
        super(TuneListWidget, self).__init__(parent)
        self.setGeometry(810, 7, 214, 520)
        self.parent = parent
        self.slider = QSlider(Qt.Horizontal, self.parent)
        self.slider.setGeometry(0, 310, 800, 30)
        self.slider.setFocusPolicy(Qt.NoFocus)
        self.doubleClicked.connect(self.openTrackFromList)
        self.delRecords = QAction(self)
        self.delRecords.setShortcut(Qt.Key_Delete)
        self.addAction(self.delRecords)
        self.connect(self.delRecords, SIGNAL("triggered()"), self.removeTune)

    def removeTune(self):
        """Removes tune from the list, after clicking "Delete" button"""
        if len(self.fileNames) < 1 or self.currentRow() < 0:
            return
        if QMessageBox.question(self, "Delete tune from list",
                                "Are you sure you want to delete this tune?",
                                QMessageBox.Yes,
                                QMessageBox.No) == QMessageBox.No:
            return
        del self.fileNames[self.currentRow() + 1]
        deleteItem = self.takeItem(self.currentRow())
        deleteItem = None

    def searchAndOpenFile(self):
        """Provides tools to load a file into the tunes list"""
        file = str(QFileDialog.getOpenFileName(
                   self, "Pick mp3 file", "", "*.mp3"))
        if file == "":
            return
        for i in range(len(self.fileNames)):
            if self.fileNames[i + 1] == file:
                QMessageBox.about(self, "Warning",
                                  "File with such name is already added")
                return
        self.fileNames[len(self.fileNames) + 1] = file
        songName = str(self.fileNames[len(self.fileNames)]).split("/")[-1]
        item = QListWidgetItem(self)
        item.setText(str(len(self.fileNames)) + ". " + songName[0:-4])

    def openTrackFromList(self):
        """Plays a double-clicked file from the tunes list and
           draws sound graphics for it
        """
        mainPlayer.importFile(
            self.fileNames[int(self.currentItem().text()[0:1])])
        mainPlayer.play()
        self.parent.addPlayButtonWidget.iconSetter = 1
        self.parent.addPlayButtonWidget.playButton.setIcon(
            QIcon(self.parent.pauseImagePath))
        self.parent.songLength = mainPlayer.getLength()

        matplotlib.use("TkAgg")
        pylab.plot(mainPlayer.soundToArray(
            filePath=self.fileNames[int(self.currentItem().text()[0:1])]),
            "b-")
        pylab.savefig(sys.path[0][:-4] + "/files/image.png")
        pltImage = scipy.ndimage.imread(sys.path[0][:-4] + "/files/image.png")
        croppedImage = pltImage[65: 535, 100: 715]
        plt.imsave(sys.path[0][:-4] + "/files/image.png", croppedImage)
        image = Image.Image(filename=sys.path[0][:-4] + "/files/image.png")
        image.resize(800, 300)
        image.save(filename=sys.path[0][:-4] + "/files/image.png")

        self.diagram = QLabel(self.parent)
        self.diagram.setGeometry(0, 0, 800, 300)
        self.diagram.setPixmap(QPixmap(sys.path[0][:-4] + "/files/image.png"))
        self.diagram.repaint()
        self.diagram.show()
        os.remove(sys.path[0][:-4] + "/files/image.png")
        pylab.close()
        self.parent.addCutEndWidget.endBox.setText(
            str("%.2f" % (self.parent.songLength - 0.01)))

        self.slider.valueChanged.connect(self.sliderPlay)
        self.slider.setValue(int(self.slider.minimum()))
        self.slider.setTickPosition(1)
        self.slider.setSingleStep(1)

        self.timer = QTimer()
        self.timer.timeout.connect(self.runTimer)
        self.timer.start(60)

    def runTimer(self):
        """Sets value for the timer"""
        if mainPlayer.mainMixer.music.get_pos() < 0:
            return
        positionLength = len(str(mainPlayer.mainMixer.music.get_pos()))
        timerValue = float(str(
            mainPlayer.mainMixer.music.get_pos()/1000)
            [:positionLength - 1]) + float(self.parent.addTime)
        self.parent.addTimerWidget.timerLabel.setText(str(timerValue))
        if timerValue >= self.parent.songLength:
            mainPlayer.stop()
            self.timer.stop()

    def sliderPlay(self):
        """Plays music at position, equivalent to the state of slider"""
        mainPlayer.stop()
        mainPlayer.play()
        mainPlayer.setPlayPosition((
            self.slider.value() * (self.parent.songLength / 100)))
        self.parent.addTime = str(
            self.slider.value() * (self.parent.songLength / 100))[:3]


class TimerWidget(QWidget):
    """Defines view for timer widget"""
    def __init__(self, parent):
        super(TimerWidget, self).__init__(parent)
        self.setGeometry(0, 450, 100, 50)
        self.layout = QVBoxLayout(self)
        self.timerLabel = QLabel(self)
        self.timerLabel.setStyleSheet(
            "QLabel { background-color : black; color : blue;" +
            "font: 19pt; font-weight:400;}")
        self.timerLabel.setText("0")
        self.timerLabel.setAlignment(Qt.AlignCenter)
        self.show()
        self.layout.addWidget(self.timerLabel)


class CutStartWidget(QWidget):
    """Defines view for textbox to input starting position for cut"""
    def __init__(self, parent):
        super(CutStartWidget, self).__init__(parent)
        self.setGeometry(220, 340, 100, 50)
        self.layout = QVBoxLayout(self)
        self.startBox = QLineEdit(self)
        self.startBox.setSizePolicy(QSizePolicy.Expanding,
                                    QSizePolicy.Expanding)
        self.startBox.setStyleSheet("QLineEdit { font: 18pt;}")
        self.startBox.setText("0")
        self.startBox.setAlignment(Qt.AlignCenter)
        self.show()
        self.layout.addWidget(self.startBox)


class CutEndWidget(QWidget):
    """Defines view for textbox to input ending position for cut"""
    def __init__(self, parent):
        super(CutEndWidget, self).__init__(parent)
        self.setGeometry(310, 340, 100, 50)
        self.layout = QVBoxLayout(self)
        self.endBox = QLineEdit(self)
        self.endBox.setSizePolicy(QSizePolicy.Expanding,
                                  QSizePolicy.Expanding)
        self.endBox.setStyleSheet("QLineEdit { font: 18pt;}")
        self.endBox.setText("0")
        self.endBox.setAlignment(Qt.AlignCenter)
        self.show()
        self.layout.addWidget(self.endBox)


class CutButtonWidget(QWidget):
    """Provides tools for cutting tune.

       Takes and checks values of instantiated
       CutStartWidget and CutEndWidget objects.

       Saves the file in folder by choice.
    """
    def __init__(self, parent):
        super(CutButtonWidget, self).__init__(parent)
        self.setGeometry(430, 350, 120, 70)
        self.layout = QVBoxLayout(self)
        self.cutButton = QPushButton("Cut!", self)
        self.cutButton.setSizePolicy(QSizePolicy.Expanding,
                                     QSizePolicy.Expanding)
        self.cutButton.clicked.connect(self.cutTune)
        self.cutButton.setStyleSheet(
            "QPushButton { font: 19pt; font-weight:600;}")
        self.show()
        self.parent = parent
        self.layout.addWidget(self.cutButton)

    def cutTune(self):
        """Checks all possible error inputs, and performs the cutting"""
        if mainPlayer.getCond() == 0:
            QMessageBox.about(self, "Warning", "First play music!")
            return
        startBox = float(self.parent.addCutStartWidget.startBox.text())
        endBox = float(self.parent.addCutEndWidget.endBox.text())
        if startBox > endBox:
            QMessageBox.about(self, "Warning",
                              "Length can't be negative number!")
            return
        wrongCut = False
        if endBox > float(self.parent.songLength) or endBox < 0:
            self.parent.addCutEndWidget.endBox.setText(
                str("%.2f" % (self.parent.songLength - 0.01)))
            wrongCut = True
        if startBox > float(self.parent.songLength) or startBox < 0:
            self.parent.addCutStartWidget.startBox.setText("0")
            wrongCut = True
        if wrongCut:
            QMessageBox.about(self, "Warning",
                              "This value is outside of boundaries")
            return

        if self.parent.saveDirectory == "":
            self.parent.saveDirectory = str(QFileDialog.getExistingDirectory(
                self, "Select directory to save files"))
        if self.parent.saveDirectory == "":
            return
        songWritePath = self.parent.saveDirectory + "/" +\
            self.parent.addTuneListWidget.currentItem().text()[3:]
        self.startLulling = self.parent.addLullingPartWidget.startLulling
        self.endLulling = self.parent.addLullingPartWidget.endLulling
        mainPlayer.cut(startingPos=startBox, endingPos=endBox,
                       filePathAndName=songWritePath,
                       startLulling=self.startLulling,
                       endLulling=self.endLulling)


class LullingPartWidget(QWidget):
    """Defines view for two buttons - left is for fading in the beginning,
       right is for fading in the end.

       After odd number of clicks of any of the buttons,
       the button turns green, whick indicates, that after cutting,
       the tune will be fading (4 sec). Alternatively, if the clicks are even,
       the button turns red, and no fading effect will be added.
    """
    startLulling = False
    endLulling = False

    def __init__(self, parent):
        super(LullingPartWidget, self).__init__(parent)
        self.setGeometry(230, 390, 180, 100)
        self.startLullingButton = QPushButton("Lullung\nstart", self)
        self.endLullingButton = QPushButton("Lulling\nend", self)
        self.startLullingButton.setGeometry(10, 0, 62, 42)
        self.endLullingButton.setGeometry(100, 0, 62, 42)
        self.startLullingButton.setStyleSheet(
            "QPushButton { font: 12pt; font-weight:600; color : red;}")
        self.endLullingButton.setStyleSheet(
            "QPushButton { font: 12pt; font-weight:600; color : red;}")
        self.startLullingButton.clicked.connect(self.startLull)
        self.endLullingButton.clicked.connect(self.endLull)

    def startLull(self):
        """Paints symbols in the left button to red or green"""
        if self.startLulling is False:
            self.startLullingButton.setStyleSheet(
                "QPushButton { font: 12pt; font-weight:600; color : green;}")
            self.startLulling = True
        else:
            self.startLullingButton.setStyleSheet(
                "QPushButton { font: 12pt; font-weight:600; color : red;}")
            self.startLulling = False

    def endLull(self):
        """Paints symbols in the right button to red or green"""
        if self.endLulling is False:
            self.endLullingButton.setStyleSheet(
                "QPushButton { font: 12pt; font-weight:600; color : green;}")
            self.endLulling = True
        else:
            self.endLullingButton.setStyleSheet(
                "QPushButton { font: 12pt; font-weight:600; color : red;}")
            self.endLulling = False


class ConcatenateTunesWidget(QWidget):
    """Provides tools for concatenating two tunes"""
    def __init__(self, parent):
        super(ConcatenateTunesWidget, self).__init__(parent)
        self.setGeometry(415, 425, 150, 100)
        self.layout = QVBoxLayout(self)
        self.concatButton = QPushButton("Concatenate", self)
        self.concatButton.setGeometry(50, 50, 90, 60)
        self.concatButton.show()
        self.concatButton.setStyleSheet(
            "QPushButton {font: 16pt; font-weight:600; }")
        self.show()
        self.layout.addWidget(self.concatButton)
        self.parent = parent
        self.concatButton.clicked.connect(self.concatenateTunes)

    def concatenateTunes(self):
        """Checks if there is at least one tune for concatenation.

           Two QMessageBox-es take the indexes (from list) of tunes,
           then performs the concatenation and saves the result.
        """
        self.fileNames = self.parent.addTuneListWidget.fileNames
        if len(self.fileNames) < 1:
            QMessageBox.about(self, "Warning",
                              "You have to input at least 1 file")
            return
        self.listSize = self.parent.addTuneListWidget.count()
        self.pickLeftTune = QInputDialog.getText(
            self, "Pick tune", "Select the number of the 'left' tune")[0]
        if self.pickLeftTune.isdigit():
            self.pickLeftTune = int(self.pickLeftTune)
        else:
            QMessageBox.about(self, "Warning",
                              "You have to input number")
            return
        if self.pickLeftTune > len(self.fileNames) or self.pickLeftTune < 1:
            QMessageBox.about(self, "Warning",
                              "This is not a number from the list")
            return

        self.pickRightTune = QInputDialog.getText(
            self, "Pick tune", "Select the number of the 'right' tune")[0]
        if self.pickRightTune.isdigit():
            self.pickRightTune = int(self.pickRightTune)
        else:
            QMessageBox.about(self, "Warning",
                              "You have to input number")
            return
        if self.pickRightTune > len(self.fileNames) or self.pickRightTune < 1:
            QMessageBox.about(self, "Warning",
                              "This is not a number from the list")
            return

        if self.parent.saveDirectory == "":
            self.parent.saveDirectory = str(QFileDialog.getExistingDirectory(
                self, "Select directory to save files"))
        if self.parent.saveDirectory == "":
            return
        songWritePath = self.parent.saveDirectory + "/"
        songWritePath += self.fileNames[
            self.pickLeftTune].split("/")[-1][:-4] + " + "
        songWritePath += self.fileNames[
            self.pickRightTune].split("/")[-1][:-4]

        mainPlayer.concat(
            self.fileNames[self.pickLeftTune],
            self.fileNames[self.pickRightTune],
            songWritePath)
