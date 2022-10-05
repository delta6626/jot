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
userName = userDetails[0].split("@")[0]

# Setting up the top panel

topPanel = Frame(home, width=w, height=140, background=stylings.jotPink)
topPanel.pack()

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