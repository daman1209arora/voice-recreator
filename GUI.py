import sys 
import math 
import numpy as np
import simpleaudio as sa
from PyQt5.QtCore import Qt 
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtWidgets import QFileDialog,QPushButton,QLabel,QApplication,QSlider,QWidget,QVBoxLayout,QScrollArea,QGroupBox,QHBoxLayout

harmonic_slider_width=1000
#try to set slider to fill entire space available to it if possible


tick_interval=1
interval=(0,100)


app=QApplication(sys.argv) 
mainWindow=QWidget()
playerWindow=QWidget(mainWindow)
fileWindow=QWidget(mainWindow)
harmonics=QScrollArea()
harmonicSliders=[]
#playerWindow,harmonics and fileWindow go on top of the mainWindow. Make better GUI arrangements in terms of layout



samplingRate=44100
base_freq=2000


def createSoundBuffer(base_freq):
    buffer=np.zeros(int(samplingRate/base_freq))
    nH=int(20000/base_freq)
    for i in range(0,len(buffer)):
        for slider in harmonicSliders:
            buffer[i]+=slider.value()*np.sin(2*np.pi*i*base_freq/samplingRate)
    buffer*=32767/max(buffer)
    buffer=buffer.astype(np.int16)
    return buffer

def playSound():
    buffer=createSoundBuffer(base_freq)
    player=sa.play_buffer(buffer,1,2,samplingRate)
    player.wait_done()


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
            slider.setValue(100)
        else:
            slider.setValue(0)
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
    base_freq=100
    layout=QVBoxLayout()
    layout.addWidget(harmonics)
    layout.addWidget(fileWindow)
    layout.addWidget(playerWindow)
    mainWindow.setLayout(layout)
    playSound()

def init():
    nH=int(20000/base_freq)
    createHarmonics(100,nH)
    createPlayer()
    createFileSystem()
    createMainWindow()

if __name__=="__main__":
    init()
    mainWindow.show()
    app.exec_()
