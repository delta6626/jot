import os
import mysql.connector
from ctypes import windll
from tkinter import *
import stylings
import subprocess
import json

windll.shcore.SetProcessDpiAwareness(1)

w,h = 1750, 950
home = Tk()

# Creating database connection

jotDB = mysql.connector.connect(
    host="localhost",
    user="root",
    password="05598105800558789969",
    database="jotDB"
)

jotDB.autocommit = True
jotCursor = jotDB.cursor()

# fetching user data

filePath = os.path.dirname(os.path.abspath(__file__)).replace("\src", "\\userDetails.txt")
f = open(filePath, "r")
userDetails = f.readlines()
f.close()

userName = userDetails[0].split("@")[0].capitalize()
jotCursor.execute("SELECT id FROM users WHERE email = (%s)", (userDetails[0].rstrip(),))
for id in jotCursor.fetchone():
    userId = id

# Utility functions

def clearSearchBox(event):
    if(searchBar.get()=="  Search for a note...."):
        searchBar.configure(state="normal")
        searchBar.configure(foreground="black")
        searchBar.delete(0, "end")

def fix():
    if(searchBar.get()==""):
        searchBar.insert(0, "  Search for a note....")
        searchBar.configure(state="normal")
        searchBar.configure(foreground="grey")
    if(len(notesPanelMain.winfo_children())==0):
        render(result)
    if(len(notesPanelMain.winfo_children())==0):
        displayMessage()

def fixOnNotesPanelMain(event):
    notesPanel.focus()
    fix()

def fixOnTopPanel(event):
    topPanel.focus()
    fix()

def fixOnPrePanel(event):
    prePanel.focus()
    fix()

def createNoteBox(noteTitle, noteId):
    def changeNoteBox(event):
        t.config(background=stylings.jotGray)
        n.config(background=stylings.jotGray)

    def resetNoteBox(event):
        t.config(background=stylings.jotGrayer)
        n.config(background=stylings.jotGrayer)
    
    def openNote(noteId, noteTitle):
        filePath = os.path.dirname(os.path.abspath(__file__))+"\details.json"
        d = {
            "id":noteId,
            "title":noteTitle
        }
        f = open(filePath, "w")
        j = json.dumps(d)
        f.write(j)
        f.close()
        subprocess.Popen(["Python", "src/editor.py"])
        exit()

    n = Frame(notesPanelMain, width=w-140, height=140,background=stylings.jotGrayer, cursor="hand2")
    n.pack(padx=40, pady=10)
    t = Label(n, text="Titled : "+noteTitle, font=stylings.defaultMediumFont, background=stylings.jotGrayer, foreground="#fff")
    t.place(anchor="center", rely=0.5, relx=0.5)
    n.bind("<Enter>", changeNoteBox)
    n.bind("<Leave>", resetNoteBox)
    n.bind("<Button-1>", lambda event:openNote(noteId=noteId, noteTitle=noteTitle))
    t.bind("<Button-1>", lambda event:openNote(noteId=noteId, noteTitle=noteTitle))

def updateList(event):
    substring = sv.get()
    if substring == "" or substring == None:
        if(len(notesPanelMain.winfo_children())==0):
            for note in result:
                createNoteBox(noteTitle=note[1], noteId=note[0])
        else:
            pass;
    else:
        for widget in notesPanelMain.winfo_children():
            widget.destroy()
        for note in result:
            if substring in note[1]:
                createNoteBox(noteTitle=note[1], noteId = note[0])        

def createNewNote(event):
    filePath = os.path.dirname(os.path.abspath(__file__))+"\details.json"
    d = {
        "id":0,
        "title":"Untitled"
    }
    f = open(filePath, "w")
    j = json.dumps(d)
    f.write(j)
    f.close()
    subprocess.Popen(["Python", "src/editor.py"])
    exit()

# Setting up the top panel

topPanel = Frame(home, width=w, height=80, background=stylings.jotBlue)
topPanel.pack()
topPanel.bind("<Button-1>", fixOnTopPanel)
greeting = Label(topPanel, text="Hello, "+userName+".", background=stylings.jotBlue, foreground="white",font=stylings.defaultMediumFont)
greeting.place(anchor="w", rely=0.5, x=40)
sv = StringVar()
sv.trace("w", lambda name, index, mode, sv= sv:updateList(sv))
searchBar = Entry(topPanel, width=40,font=stylings.defaultSmallFont, border=0, fg="grey", textvariable=sv)
searchBar.insert(0, "  Search for a note....")
searchBar.place(anchor="center", relx=0.5, rely=0.5, height=45)
searchBar.bind("<Button-1>", clearSearchBox)
plusIcon = PhotoImage(file=os.path.dirname(os.path.abspath(__file__)).replace("\src", "\\images\createButton.png"))
plusIconHover = PhotoImage(file=os.path.dirname(os.path.abspath(__file__)).replace("\src", "\\images\createButtonHover.png"))
createButton = Label(topPanel, image=plusIcon, background=stylings.jotBlue)
createButton.bind("<Enter>", lambda e: createButton.config(image=plusIconHover))
createButton.bind("<Leave>", lambda e: createButton.config(image=plusIcon))
createButton.bind("<Button-1>", createNewNote)
createButton.place(anchor="e", rely=0.4, x=1710)

# pre panel

prePanel = Frame(home, width=w, height=90, background=stylings.jotDark)
prePanel.pack()
prePanel.bind("<Button-1>", fixOnPrePanel)
lblYourNotes = Label(prePanel, text="Your Notes",background=stylings.jotDark, foreground="white", font=stylings.defaultLargeFont)
lblYourNotes.place(anchor="w", y=50, x=40)

# setting up the notes panel

notesPanel = Frame(home, width=w, height=800, background=stylings.jotDark)
notesPanel.pack(fill="both", expand=1)
canvas = Canvas(notesPanel, background=stylings.jotDark, highlightthickness=0)
canvas.pack(side="left", fill="both", expand=1)
sb = Scrollbar(notesPanel, orient="vertical", command=canvas.yview)
sb.pack(side="right", fill="y")
canvas.configure(yscrollcommand=sb.set)
canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion = canvas.bbox("all")))
notesPanelMain = Frame(canvas, background=stylings.jotDark)
notesPanelMain.bind("<Button-1>", fixOnNotesPanelMain)
canvas.create_window((0,0), window=notesPanelMain, anchor="nw")

# Rendering and helper message functions

def displayMessage():
    noNotes = Label(notesPanelMain, text="You don't have any notes as of now.\nClick on the plus button above to create a new note.", foreground="grey", background=stylings.jotDark, font=stylings.defaultSmallFont)
    noNotes.pack(padx= w/3.2 - noNotes.winfo_width(), pady=400-(noNotes.winfo_height()/2))
def render(notesList):
    for note in notesList:
        createNoteBox(noteTitle = note[1], noteId = note[0])

# Checking if user has any notes

jotCursor.execute("SELECT noteId ,noteName from notes WHERE id = (%s)", (userId,))
result = jotCursor.fetchall()
jotDB.close() 

if(result == []):
    displayMessage()
else:
    render(result)

# Main function

def main():
    home.title("Jot")
    screenW = home.winfo_screenwidth()
    screenH = home.winfo_screenheight()
    x,y = (screenW/2) - (w/2), (screenH/2) - (h/2)
    home.geometry('%dx%d+%d+%d' % (w, h, x, y))
    home.resizable(False, False)
    home.iconphoto(True, PhotoImage(file="images/jotLogo.png"))
    home.mainloop()

main()