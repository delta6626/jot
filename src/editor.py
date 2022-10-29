import os
import mysql.connector
from ctypes import windll
from tkinter import *
import stylings
import json


windll.shcore.SetProcessDpiAwareness(1)

filePath = os.path.dirname(os.path.abspath(__file__))+"\details.json"
w,h = 1750, 950
editorWin = Tk()
noteText = ""

# Creating database connection

jotDB = mysql.connector.connect(
    host="localhost",
    user="root",
    password="05598105800558789969",
    database="jotDB"
)

jotDB.autocommit = True
jotCursor = jotDB.cursor()

# Utiltiy

def getNoteText():
    f = open(filePath)
    details = json.load(f)
    if details["id"] == 0:
        pass;
    else:
        jotCursor.execute("SELECT noteText FROM notes WHERE noteId = (%s)", (details["id"],))
        global noteText
        noteText = jotCursor.fetchone()[0]
        jotDB.close() # Remove later
        


# UI

controlsPanel = Frame(editorWin, width=w, height=150, background=stylings.jotBlue)
controlsPanel.pack()
editorPanel = Frame(editorWin, width=w, height=h-150,background=stylings.jotGrayer)
editorPanel.pack()
textEditor = Text(editorPanel, width=90, height=20, border=0, font=stylings.defaultMediumFont, background=stylings.jotGrayer, foreground="white", insertbackground="white")
textEditor.place(anchor="center", relx=0.5, rely=0.5)
textEditor.focus()
getNoteText()
textEditor.insert(0.0, noteText)


def main():
    f = open(filePath)
    details = json.load(f)
    editorWin.title(details["title"]+" - Jot")
    f.close()
    screenW = editorWin.winfo_screenwidth()
    screenH = editorWin.winfo_screenheight()
    x,y = (screenW/2) - (w/2), (screenH/2) - (h/2)
    editorWin.geometry('%dx%d+%d+%d' % (w, h, x, y))
    editorWin.resizable(False, False)
    editorWin.iconphoto(True, PhotoImage(file="images/jotLogo.png"))
    editorWin.mainloop()

main()