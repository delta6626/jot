import os
import mysql.connector
from ctypes import windll
from tkinter import *
import stylings


windll.shcore.SetProcessDpiAwareness(1)

w,h = 1750, 950
editor = Tk()

# Creating database connection

jotDB = mysql.connector.connect(
    host="localhost",
    user="root",
    password="05598105800558789969",
    database="jotDB"
)

jotDB.autocommit = True
jotCursor = jotDB.cursor()

def main():
    editor.title("Untitled")
    screenW = editor.winfo_screenwidth()
    screenH = editor.winfo_screenheight()
    x,y = (screenW/2) - (w/2), (screenH/2) - (h/2)
    editor.geometry('%dx%d+%d+%d' % (w, h, x, y))
    editor.resizable(False, False)
    editor.iconphoto(True, PhotoImage(file="images/jotLogo.png"))
    editor.mainloop()

main()