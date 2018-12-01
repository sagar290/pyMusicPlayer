import os
from tkinter.filedialog import askdirectory
import pygame
from mutagen.id3 import ID3
from tkinter import *

root = Tk()
root.minsize(300, 300)

listofsongs = []
realname = []

v = StringVar()
songlabel = Label(root, textvariable = v, width = 35)

index = 0


def nextSong(event):
    global index
    index += 1
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    updatelabel()

def prevsong(event):
    global index
    index -= 1
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    updatelabel()

def stopsong(event):
    pygame.mixer.music.stop()
    v.set("")

def updatelabel():
    global index
    # global songname
    v.set(str(listofsongs[index]))
    # return songname

def directoryChooser():
    directory = askdirectory()
    os.chdir(directory)

    for files in os.listdir(directory):
        if files.endswith(".mp3"):
            realdir = os.path.realpath(files)
            # audio = ID3(realdir)
            # realname.append(audio["TIT2"].text[0])
            listofsongs.append(files)
            

    pygame.mixer.init()
    pygame.mixer.music.load(listofsongs[0])
    pygame.mixer.music.play()
    updatelabel()
directoryChooser()

label = Label(root, text= "Music Player")
label.pack()


listbox = Listbox(root)
listbox.pack()

listofsongs.reverse()
for items in listofsongs:
    listbox.insert(0, items)
listofsongs.reverse()

nextbutton = Button(root, text = "Next Song")
nextbutton.pack()

previusbutton = Button(root, text = "Previous Song")
previusbutton.pack()

songlabel.pack()


stopbutton = Button(root, text = "Stop Song")
stopbutton.pack()

nextbutton.bind("<Button-1>", nextSong)
previusbutton.bind("<Button-1>", prevsong)
stopbutton.bind("<Button-1>", stopsong)



root.mainloop()