import os
import mysql.connector
from ctypes import windll
from tkinter import *
import stylings

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

def fixOnNotesPanelMain(event):
    notesPanel.focus()
    fix()

def fixOnTopPanel(event):
    topPanel.focus()
    fix()

def fixOnPrePanel(event):
    prePanel.focus()
    fix()

def createNoteBox(noteTitle, noteText):
    def changeNoteBox(event):
        text.config(background=stylings.jotGreen, foreground="black")
        t.config(background=stylings.jotPink, foreground="black")
        n.config(background=stylings.jotPink)

    def resetNoteBox(event):
        text.config(background=stylings.jotGray, foreground="white")
        t.config(background=stylings.jotGrayer, foreground="white")
        n.config(background=stylings.jotGrayer)

    n = Frame(notesPanelMain, width=w-140, height=240,background=stylings.jotGrayer, cursor="hand2")
    n.pack(padx=40, pady=10)
    text = Label(n, width=w-140, height=5, text=noteText[0:40]+"...", font=stylings.defaultMediumFont, background=stylings.jotGray, foreground="#fff")
    text.place(anchor="center", rely=0.2, relx=0.5)
    t = Label(n, text="Titled : "+noteTitle, font=stylings.defaultMediumFont, background=stylings.jotGrayer, foreground="#fff")
    t.place(anchor="center", rely=0.8, relx=0.5)
    n.bind("<Enter>", changeNoteBox)
    n.bind("<Leave>", resetNoteBox)


def createNewNote(event):
    pass;

# Setting up the top panel

topPanel = Frame(home, width=w, height=80, background=stylings.jotBlue)
topPanel.pack()
topPanel.bind("<Button-1>", fixOnTopPanel)
greeting = Label(topPanel, text="Hello, "+userName+".", background=stylings.jotBlue, foreground="white",font=stylings.defaultMediumFont)
greeting.place(anchor="w", rely=0.5, x=40)
searchBar = Entry(topPanel, width=40,font=stylings.defaultSmallFont, border=0, fg="grey")
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
        createNoteBox(noteTitle = note[0], noteText = note[1])

# Checking if user has any notes

jotCursor.execute("SELECT noteName, noteText from notes WHERE id = (%s)", (userId,))
result = jotCursor.fetchall()
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