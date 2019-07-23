import sys 
import pygame
import math 
import wave,struct
import numpy as np
import simpleaudio as sa
from PyQt5.QtCore import Qt 
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtWidgets import QFileDialog,QPushButton,QLabel,QApplication,QSlider,QWidget,QVBoxLayout,QScrollArea,QGroupBox,QHBoxLayout

class SoundPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.isPlaying=False
        self.player=pygame.mixer

    def play(self,buffer):
        if(self.isPlaying==True):
            self.player.stop() 
       #else: 
        file = wave.open('temp.wav','w')
        file.setnchannels(2)
        file.setsampwidth(2)
        file.setframerate(samplingRate)
        for v in buffer:
            file.writeframesraw(struct.pack('<h',v ))
        file.close()
        self.isPlaying=True
        self.player.Sound('temp.wav').play(-1)

    def stop(self):
        if(self.isPlaying==True):
            self.player.stop()
            self.isPlaying=False


class FileHandler():
    def writeInFile(self,filename,sliders):
        file=open(filename,'w')
        base_freq_txt=str(base_freq)+' '
        file.write(base_freq_txt)
        for slider in sliders:
            txt=str(slider.value())+' '
            file.write(txt)
        file.close()

    def readFile(self,filename):
        file=open(filename,'r')
        s=file.readlines()[0].split(' ')
        return (int(s[0]),list(map(int,s[1:len(s)-1])))



harmonic_slider_width=1000
#try to set slider to fill entire space available to it if possible
app=QApplication(sys.argv)
 
tick_interval=1
interval=(0,1000)

samplingRate=44100
base_freq=100

fl=FileHandler()
soundPlayer=SoundPlayer()
mainWindow=QWidget()
playerWindow=QWidget(mainWindow)
fileWindow=QWidget(mainWindow)
harmonics=QScrollArea()
harmonicSliders=[]

#playerWindow,harmonics and fileWindow go on top of the mainWindow. Make better GUI arrangements in terms of layout
def stop():
    soundPlayer.stop()

def play():
    b=createSoundBuffer(base_freq)
    soundPlayer.play(b)

def saveFile():
    print("Here")
    fname,_ = QFileDialog.getSaveFileName(None, 'Save file', '/home/daman1209arora/voice-recreator')
    fl.writeInFile(fname,harmonicSliders)
   
def loadFile():
    fname,_=QFileDialog.getOpenFileName(None,'Open file', '/home/daman1209arora/voice-recreator')
    freq,hrmncs=fl.readFile(fname)
    setSliderValues(freq,hrmncs)

def setSliderValues(freq,values):
    for i in range(0,len(values)):
        harmonicSliders[i].setValue(values[i])

def createSoundBuffer(base_freq):
    buffer=np.zeros(int(samplingRate/base_freq))
    nH=int(20000/base_freq)
    for i in range(0,len(buffer)):
        for j in range(0,len(harmonicSliders)):
            buffer[i]+=harmonicSliders[j].value()*np.sin(2*np.pi*i*(j+1)*base_freq/samplingRate)
    buffer*=32767.0/max(buffer)
    buffer=buffer.astype(np.int16)
    return buffer


def createHarmonics(freq,n): 
    harmonicWindow=QWidget(mainWindow)
    harmonics.setWidgetResizable(True)
    harmonics.setFixedWidth(harmonic_slider_width)
    main_layout=QVBoxLayout()
    for i in range(0,n):
        layout=QVBoxLayout()
        txt='Harmonic '+str(i+1)+' Frequency: '+str(freq*(i+1)) 
        box=QGroupBox(txt)
        slider=QSlider(orientation=Qt.Horizontal,parent=harmonicWindow)
        slider.setTickInterval(tick_interval) 
        slider.setMinimum(interval[0]) 
        slider.setMaximum(interval[1]) 
        slider.sliderReleased.connect(play)
        harmonicSliders.append(slider)
        layout.addWidget(slider)
        box.setLayout(layout)
        main_layout.addWidget(box)

    values=np.full(n,interval[0])
    values[0]=interval[1]

    setSliderValues(base_freq,values)

    harmonicWindow.setLayout(main_layout)
    harmonics.setWidget(harmonicWindow)


def createPlayer():
    playButton,pauseButton=QPushButton('Play'),QPushButton('Pause')
    playButton.setIcon(QIcon(QPixmap('playbutton.png')))
    pauseButton.setIcon(QIcon(QPixmap('pausebutton.png')))
    playButton.clicked.connect(play)
    pauseButton.clicked.connect(stop)
    layout=QHBoxLayout()
    layout.addWidget(playButton)
    layout.addWidget(pauseButton)
    playerWindow.setLayout(layout)

def createFileSystem():
    saveButton,loadButton=QPushButton('Save'),QPushButton('Load')
    saveButton.setIcon(QIcon(QPixmap('savebutton.png')))
    loadButton.setIcon(QIcon(QPixmap('loadbutton.jpeg')))
    saveButton.clicked.connect(saveFile)
    loadButton.clicked.connect(loadFile)
    layout=QHBoxLayout()
    layout.addWidget(saveButton)
    layout.addWidget(loadButton)
    fileWindow.setLayout(layout)

def createMainWindow():
    layout=QVBoxLayout()
    layout.addWidget(harmonics)
    layout.addWidget(fileWindow)
    layout.addWidget(playerWindow)
    mainWindow.setLayout(layout)

def init():
    pygame.mixer.init()
    nH=int(20000/base_freq)
    createHarmonics(base_freq,nH)
    createPlayer()
    createFileSystem()
    createMainWindow()

if __name__=="__main__":
    init()
    mainWindow.show()
    app.exec_()
