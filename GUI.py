import sys 
import matplotlib.pyplot as plt
import pygame
import math 
import wave,struct
import numpy as np
import simpleaudio as sa
from PyQt5.QtCore import Qt 
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtWidgets import QFileDialog,QPushButton,QLabel,QApplication,QSlider,QWidget,QVBoxLayout,QScrollArea,QGroupBox,QHBoxLayout


sampleRate=44100


harmonic_slider_width=1000
#try to set slider to fill entire space available to it if possible


tick_interval=1
interval=(0,100)

soundPlayer=None
app=QApplication(sys.argv) 
mainWindow=QWidget()
playerWindow=QWidget(mainWindow)
fileWindow=QWidget(mainWindow)
harmonics=QScrollArea()
harmonicSliders=[]
#playerWindow,harmonics and fileWindow go on top of the mainWindow. Make better GUI arrangements in terms of layout

isPlaying=False

def stop(q):
    global soundPlayer,isPlaying
    if(isPlaying==True):
        isPlaying=False
        soundPlayer.stop()

def play(q):
    global isPlaying
    if(isPlaying==False):
        isPlaying=True
        playSound()

samplingRate=44100
base_freq=100


def createSoundBuffer(base_freq):
    buffer=np.zeros(int(samplingRate/base_freq))
    nH=int(20000/base_freq)
    for i in range(0,len(buffer)):
        for j in range(0,len(harmonicSliders)):
            buffer[i]+=harmonicSliders[j].value()*np.sin(2*np.pi*i*(j+1)*base_freq/samplingRate)
    buffer*=32767.0/max(buffer)
    buffer=buffer.astype(np.int16)
    return buffer

def playSound():
    global soundPlayer
    buffer=createSoundBuffer(base_freq)
    file = wave.open('temp.wav','w')
    file.setnchannels(2)
    file.setsampwidth(2)
    file.setframerate(sampleRate)
    for v in buffer:
        file.writeframesraw(struct.pack('<h',v ))
    file.close()
    soundPlayer=pygame.mixer.Sound('temp.wav')
    soundPlayer.play(-1)
    

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
        if(i==0):
            slider.setValue(interval[1])
        else:
            slider.setValue(interval[0])
        slider.valueChanged.connect(playSound)
        harmonicSliders.append(slider)
        layout.addWidget(slider)
        box.setLayout(layout)
        main_layout.addWidget(box)

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
    layout=QHBoxLayout()
    layout.addWidget(saveButton)
    layout.addWidget(loadButton)
    fileWindow.setLayout(layout)

def createMainWindow():
    global base_freq
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
