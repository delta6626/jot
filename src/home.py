import os
from ctypes import windll
from tkinter import *
import stylings

windll.shcore.SetProcessDpiAwareness(1)

w,h = 1750, 950
home = Tk()

# fetching user data

filePath = os.path.dirname(os.path.abspath(__file__)).replace("\src", "\\userDetails.txt")
f = open(filePath, "r")
userDetails = f.readlines()
f.close()
userName = userDetails[0].split("@")[0].capitalize()

# Utility functions

def clearSearchBox(event):
    if(searchBar.get()=="   Search for a note...."):
        searchBar.configure(state="normal")
        searchBar.configure(foreground="black")
        searchBar.delete(0, "end")

def fixOnNotePanel(event):
    notesPanel.focus()
    if(searchBar.get()==""):
        searchBar.insert(0, "   Search for a note....")
        searchBar.configure(state="normal")
        searchBar.configure(foreground="grey")

def fixOnTopPanel(event):
    topPanel.focus()
    if(searchBar.get()==""):
        searchBar.insert(0, "   Search for a note....")
        searchBar.configure(state="normal")
        searchBar.configure(foreground="grey")

# Setting up the top panel

topPanel = Frame(home, width=w, height=80, background=stylings.jotBlue)
topPanel.pack()
topPanel.bind("<Button-1>", fixOnTopPanel)
greeting = Label(topPanel, text="Hello, "+userName+".", background=stylings.jotBlue, foreground="white",font=stylings.defaultMediumFont)
greeting.place(anchor="w", rely=0.5, x=40)
searchBar = Entry(topPanel, width=40,font=stylings.defaultSmallFont, border=0, fg="grey")
searchBar.insert(0, "   Search for a note....")
searchBar.place(anchor="center", relx=0.5, rely=0.5, height=45)
searchBar.bind("<Button-1>", clearSearchBox)
searchBar.bind()
plusIcon = PhotoImage(file=os.path.dirname(os.path.abspath(__file__)).replace("\src", "\\images\createButton.png"))
plusIconHover = PhotoImage(file=os.path.dirname(os.path.abspath(__file__)).replace("\src", "\\images\createButtonHover.png"))
createButton = Label(topPanel, image=plusIcon, background=stylings.jotBlue)
createButton.bind("<Enter>", lambda e: createButton.config(image=plusIconHover))
createButton.bind("<Leave>", lambda e: createButton.config(image=plusIcon))
createButton.place(anchor="e", rely=0.4, x=1710)

# setting up the notes panel

notesPanel = Frame(home, width=w, height=870, background=stylings.jotDark)
notesPanel.bind("<Button-1>", fixOnNotePanel)
notesPanel.pack()

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