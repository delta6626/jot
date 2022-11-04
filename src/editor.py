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
boldIcon = PhotoImage(file=os.path.dirname(os.path.abspath(__file__)).replace("\src", "\\images\Bold.png"))
boldIconHover = PhotoImage(file=os.path.dirname(os.path.abspath(__file__)).replace("\src", "\\images\BoldHover.png"))
bold = Label(controlsPanel, image=boldIcon, background=stylings.jotBlue)
bold.bind("<Enter>", lambda e: bold.config(image=boldIconHover))
bold.bind("<Leave>", lambda e: bold.config(image=boldIcon))
bold.place(anchor="w",relx=0.01, rely=0.5)

underlineIcon = PhotoImage(file=os.path.dirname(os.path.abspath(__file__)).replace("\src", "\\images\_Underline.png"))
underlineIconHover = PhotoImage(file=os.path.dirname(os.path.abspath(__file__)).replace("\src", "\\images\_UnderlineHover.png"))
underline = Label(controlsPanel, image=underlineIcon, background=stylings.jotBlue)
underline.bind("<Enter>", lambda e: underline.config(image=underlineIconHover))
underline.bind("<Leave>", lambda e: underline.config(image=underlineIcon))
underline.place(anchor="w",relx=0.08, rely=0.5)

italicsIcon = PhotoImage(file=os.path.dirname(os.path.abspath(__file__)).replace("\src", "\\images\Italics.png"))
italicsIconHover = PhotoImage(file=os.path.dirname(os.path.abspath(__file__)).replace("\src", "\\images\ItalicsHover.png"))
italics = Label(controlsPanel, image=italicsIcon, background=stylings.jotBlue)
italics.bind("<Enter>", lambda e: italics.config(image=italicsIconHover))
italics.bind("<Leave>", lambda e: italics.config(image=italicsIcon))
italics.place(anchor="w",relx=0.15, rely=0.5)

listIcon = PhotoImage(file=os.path.dirname(os.path.abspath(__file__)).replace("\src", "\\images\List.png"))
listIconHover = PhotoImage(file=os.path.dirname(os.path.abspath(__file__)).replace("\src", "\\images\ListHover.png"))
list = Label(controlsPanel, image=listIcon, background=stylings.jotBlue)
list.bind("<Enter>", lambda e: list.config(image=listIconHover))
list.bind("<Leave>", lambda e: list.config(image=listIcon))
list.place(anchor="w",relx=0.395, rely=0.5)

fontIcon = PhotoImage(file=os.path.dirname(os.path.abspath(__file__)).replace("\src", "\\images\Font.png"))
fontIconHover = PhotoImage(file=os.path.dirname(os.path.abspath(__file__)).replace("\src", "\\images\FontHover.png"))
font = Label(controlsPanel, image=fontIcon, background=stylings.jotBlue)
font.bind("<Enter>", lambda e: font.config(image=fontIconHover))
font.bind("<Leave>", lambda e: font.config(image=fontIcon))
font.place(anchor="w",relx=0.465, rely=0.5)

colorpickerIcon = PhotoImage(file=os.path.dirname(os.path.abspath(__file__)).replace("\src", "\\images\ColorPicker.png"))
colorpickerIconHover = PhotoImage(file=os.path.dirname(os.path.abspath(__file__)).replace("\src", "\\images\ColorPickerHover.png"))
colorpicker = Label(controlsPanel, image=colorpickerIcon, background=stylings.jotBlue)
colorpicker.bind("<Enter>", lambda e: colorpicker.config(image=colorpickerIconHover))
colorpicker.bind("<Leave>", lambda e: colorpicker.config(image=colorpickerIcon))
colorpicker.place(anchor="w",relx=0.535, rely=0.5)

saveIcon = PhotoImage(file=os.path.dirname(os.path.abspath(__file__)).replace("\src", "\\images\Save.png"))
saveIconHover = PhotoImage(file=os.path.dirname(os.path.abspath(__file__)).replace("\src", "\\images\SaveHover.png"))
save = Label(controlsPanel, image=saveIcon, background=stylings.jotBlue)
save.bind("<Enter>", lambda e: save.config(image=saveIconHover))
save.bind("<Leave>", lambda e: save.config(image=saveIcon))
save.place(anchor="e",x=1710, rely=0.5)

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