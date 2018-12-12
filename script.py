import os
from tkinter.filedialog import askdirectory
import threading
try:
    import pygame
    from mutagen.id3 import ID3       
except ImportError:
    print("Trying to Install required module: requests\n")
    os.system('python -m pip install pygame')
    os.system('python -m pip install mutagen')
    import pygame
    from mutagen.id3 import ID3
from tkinter import *

root = Tk()
root.minsize(300, 300)

leftframe = Frame(root)
leftframe.grid(row=0,column=0, padx=10, pady=20)
rightframe = Frame(root)
rightframe.grid(row=0, column=1, padx=10, pady=20)

controlerframe = Frame(rightframe)
controlerframe.pack()

infoframe = Frame(rightframe)
infoframe.pack()

volumectroleframe = Frame(rightframe, height=2, bd=1, relief=GROOVE)
volumectroleframe.pack()

# variable declarion 
listofsongs = []
realname = []
playsong = False
volumeValue = .30

v = StringVar()
songlabel = Label(infoframe, textvariable = v, width = 35)

index = 0

def playtrack():
    global playsong, listofsongs, t1
    if listofsongs:
        if playsong == True:
            pygame.mixer.music.pause()
            playButton.config(image = playphoto)
            playsong = False
        else:
            pygame.mixer.music.unpause()
            playButton.config(image = pausephoto)
            playsong = True
            t1 =  threading.Thread(target=loop)
            t1.start()

def nextSong():
    global index, listofsongs
    if listofsongs: 
        # index += 1
        # pygame.mixer.music.load(listofsongs[index])
        # pygame.mixer.music.play()
        # updatelabel()
        if index != len(listofsongs) - 1:
            index += 1
            pygame.mixer.music.load(listofsongs[index])
            pygame.mixer.music.play()
            updatelabel()
        else:
            index = 0
            pygame.mixer.music.load(listofsongs[0])
            pygame.mixer.music.play()
            updatelabel()
def prevsong():
    global index, listofsongs
    if listofsongs:
        if index != 0: 
            index -= 1
            pygame.mixer.music.load(listofsongs[index])
            pygame.mixer.music.play()
            updatelabel()
        else:
            index = len(listofsongs) - 1
            pygame.mixer.music.load(listofsongs[index])
            pygame.mixer.music.play()
            updatelabel()    

def stopsong():
    global playsong
    playsong = False
    if playsong:
        pygame.mixer.music.stop()
    v.set("")


def volumecontroller(value):
    global volumeValue, listofsongs
    if listofsongs:
        volumeValue = int(value) / 100
        pygame.mixer.music.set_volume(volumeValue)

def updatelabel():
    global index
    # global songname
    v.set(str(listofsongs[index]))

# Looping all song    
import time
def loop(): 
    global playsong, listofsongs
    if listofsongs: 
        while playsong:
            time.sleep(2)
            if pygame.mixer.music.get_busy():
                pass
            else: 
                nextSong()
#declasre thread


def directoryChooser():
    global playsong, listofsongs, volumeValue
    listofsongs = []
    directory = askdirectory()
    if directory:
        pass
    else: 
        return
    os.chdir(directory)

    for files in os.listdir(directory):
        if files.endswith(".mp3"):
            realdir = os.path.realpath(files)
            # audio = ID3(realdir)
            # realname.append(audio["TIT2"].text[0])
            listofsongs.append(files)
            
    if listofsongs: 
        pygame.mixer.init()
        pygame.mixer.music.load(listofsongs[index])
        pygame.mixer.music.set_volume(volumeValue)
        pygame.mixer.music.play()
        updatelabel()
        listofsongs.reverse()
        for items in listofsongs:
            listbox.insert(0, items)
        listofsongs.reverse()
        playButton.config(image = pausephoto)
        playsong = True
        vloume.set(30)
        t1 =  threading.Thread(target=loop)
        t1.start()
        

# label = Label(root, text= "Music Player")
# label.pack()

# Listbox 
listbox = Listbox(leftframe)
listbox.pack()

#UI

addButton = Button(leftframe, text="Add", command=directoryChooser)
addButton.pack()

prevphoto = PhotoImage(file="img/prev.png")
prevButton = Button(controlerframe, image = prevphoto, command = prevsong)
prevButton.pack(side=LEFT)

pausephoto = PhotoImage(file="img/pause.png")
playphoto = PhotoImage(file="img/play.png")
playButton = Button(controlerframe, image = playphoto, command=playtrack)
playButton.pack(side=LEFT)

nextphoto = PhotoImage(file="img/next.png")
nextButton = Button(controlerframe, image = nextphoto, command= nextSong)
nextButton.pack(side=RIGHT, pady=10)

speakerPhoto = PhotoImage(file="img/speaker.png")
speakerlabel = Label(volumectroleframe, image = speakerPhoto)
speakerlabel.grid(row=0, column=0)

vloume = Scale(volumectroleframe, from_ =0, to=100, orient=HORIZONTAL, command = volumecontroller)
vloume.grid(row=0, column=1)
songlabel.pack()


# Stop all loop after closing close button
def on_closing():
    stopsong()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
