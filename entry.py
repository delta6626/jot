# The official Jot source code
# Copyright (c) github.com/delta911ee | M. Hassan
# Licensed under the MIT license

userDetails = []

import subprocess
import mysql.connector
from ctypes import windll
from tkinter import *
import re
from src import stylings

windll.shcore.SetProcessDpiAwareness(1)

# Connect to jotDB

jotDB = mysql.connector.connect(
    host="localhost",
    user="root",
    password="05598105800558789969",
    database="jotDB"
)

jotDB.autocommit = True
jotCursor = jotDB.cursor()

# Window opening functions

def openMain():
    subprocess.Popen(["Python", "src/home.py"])
    exit()

def showSuccess():
    f = open("userDetails.txt", "w")
    userDetails = [email.get(),"\n",password.get()]
    f.writelines(userDetails)
    f.close()
    leftPanel.destroy()
    rightPanel.destroy()
    slWindow.config(background=stylings.jotDark)
    successMessagePanel = Frame(slWindow, background=stylings.jotDark)
    successMessage = Label(successMessagePanel, text="Congratulations!\nAccount creation was successful.", font=stylings.defaultLargeFont, background=stylings.jotDark, foreground=stylings.jotGreen)
    successMessage.pack()
    createSeparator(successMessagePanel, height=15, bg=stylings.jotDark)
    proceedButton = Button(successMessagePanel, text="Let's get started.", width=28, border=0, font=stylings.defaultSmallFont,command=openMain)
    proceedButton.bind("<Enter>", lambda e : proceedButton.config(background=stylings.jotGreen))
    proceedButton.bind("<Leave>", lambda e : proceedButton.config(background="SystemButtonFace") )
    proceedButton.pack()
    successMessagePanel.place(anchor="center", relx=0.5, rely=0.5)


# Utility functions for Entry

def clearEmailPlaceholder(event):
    if(email.get() == "  Enter your email"):
        email.configure(state = "normal")
        email.delete(0, "end")
    if(password.get()==""):
        password.insert(0, "  Choose a password")

def clearPasswordPlaceholder(event):
    if(password.get() == "  Choose a password" or password.get()=="  Enter your password"):
        password.configure(state = "normal")
        password.delete(0, "end")
    if(email.get()==""):
        email.insert(0, "  Enter your email")

def switch(event): #Switch the signup button with login button and vice versa
    if(btnSignup["text"] == "Sign Up"):
        btnSignup["text"] = "Login"
        lblLogin["text"] = "Click here to sign up instead."
        password.delete(0, "end")
        password.insert(0, "  Enter your password")
    elif(btnSignup["text"] == "Login"):
        btnSignup["text"] = "Sign Up"
        lblLogin["text"] = "Click here to login instead."
        password.delete(0, "end")
        password.insert(0, "  Choose a password")

# Input validation functions

def preCheck():
    if(password.get() == "" or password.get()=="  Choose a password" or email.get()=="" or email.get()=="  Enter your email"):
        try:
            warning.config(text="Please enter all the details")
            return warning.pack_info()
        except:
            createSeparator(rightPanelWc, height=15, bg=stylings.jotGreen)
            warning.pack()
    else:
        if(btnSignup["text"] == "Sign Up"):
            signUp()
        elif(btnSignup["text"] == "Login"):
            login()

def validEmail(email):
    emailFormat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.fullmatch(emailFormat, email)):
        return True
    else:
        return False

def validPassword(password):
    minLength = 8
    maxLength = 30
    if (len(password) >= minLength and len(password) <=maxLength):
        return True
    else:
        return False

# Sign up and Log in functions

def signUp():
    # Checking wether user exists

    jotCursor.execute("SELECT id FROM users WHERE email = %s", (email.get(),))
    result = jotCursor.fetchall()

    if (validEmail(email.get()) == False):
        try:
            warning.config(text="Please enter a valid email address.")
            return warning.pack_info()
        except:
            createSeparator(rightPanelWc, height=15, bg=stylings.jotGreen)
            warning.pack()

    elif(validPassword(password.get()) == False):
        try:
            warning.config(text="Password should be more than 8 characters\nand less than 30 characters.")
            return warning.pack_info()
        except:
            createSeparator(rightPanelWc, height=15, bg=stylings.jotGreen)
            warning.pack()
    
    elif result != []:
        try:
            warning.config(text="This Email address already exists.")
            return warning.pack_info()
        except:
            createSeparator(rightPanelWc, height=15, bg=stylings.jotGreen)
            warning.pack()
    else:
        jotCursor.execute(f"INSERT INTO users (email, password) VALUES(%s,%s)", (email.get(), password.get()))
        jotDB.close()
        showSuccess()

def login():
    jotCursor.execute("SELECT id, password FROM users WHERE email = %s", (email.get(),))
    result = jotCursor.fetchall()
    
    if result == []:
        try:
            warning.config(text="This Email does not exists. Create a new account.")
            return warning.pack_info()
        except:
            createSeparator(rightPanelWc, height=15, bg=stylings.jotGreen)
            warning.pack()
    else:
        if (password.get() != result[0][1]):
            try:
                warning.config(text="Incorrect password. Please try again.")
                return warning.pack_info()
            except:
                createSeparator(rightPanelWc, height=15, bg=stylings.jotGreen)
                warning.pack()
        else:
            jotDB.close()
            openMain()

# UI

def createSeparator(master, height, bg):
    return Frame(master=master, height=height, background=bg).pack()

w,h = 1280,800
slWindow = Tk()

# Left panel layout

leftPanel = Frame(slWindow, width=w/2, height=h, background=stylings.jotDark)
leftPanel.pack(side="left")

leftPanelWC = Frame(leftPanel, background=stylings.jotDark)  

logo = PhotoImage(file="images/jotLogoSlwindow.png")
logoCont = Label(leftPanelWC, image=logo, background=stylings.jotDark)
heroText1 = Label(leftPanelWC, text="Take\nthe best notes.", font=stylings.defaultLargeFont,
            background=stylings.jotDark, foreground="#fff")
heroText2 = Label(leftPanelWC, text="Meet Jot.", font=stylings.defaultLargeFont,
            background=stylings.jotDark, foreground="#fff")

logoCont.pack()
heroText1.pack()
heroText2.pack()

leftPanelWC.place(anchor="center", relx=0.5, rely=0.5) # centering 

# Right panel layout

rightPanel = Frame(slWindow, width=w/2, height=h, background=stylings.jotGreen)
rightPanel.pack(side="right")

rightPanelWc = Frame(rightPanel, background=stylings.jotGreen)

header = Label(rightPanelWc, text="Welcome to Jot", font=stylings.defaultMediumFont, background=stylings.jotGreen, fg="black")
email = Entry(rightPanelWc, width=32, font=stylings.defaultSmallFont, border=0, fg="black")
email.insert(0,"  Enter your email")
email.bind("<Button-1>", clearEmailPlaceholder)
password = Entry(rightPanelWc, width=32, font=stylings.defaultSmallFont, border=0, fg="black")
password.insert(0, "  Choose a password")
password.bind("<Button-1>", clearPasswordPlaceholder)
btnSignup = Button(rightPanelWc, text="Sign Up", width=28, border=0, font=stylings.defaultSmallFont, command=preCheck)
btnSignup.bind("<Enter>", lambda e : btnSignup.config(background=stylings.jotPink))
btnSignup.bind("<Leave>", lambda e : btnSignup.config(background="SystemButtonFace") )
warning = Label(rightPanelWc, background=stylings.jotGreen, fg=stylings.jotRed, font=stylings.defaultSmallFont)
lblLogin = Label(rightPanelWc, text="Click here to login instead.", fg="black", background=stylings.jotGreen, font=stylings.defaultSmallFont)
lblLogin.bind("<Enter>", lambda e : lblLogin.config(foreground=stylings.jotPink))
lblLogin.bind("<Leave>", lambda e : lblLogin.config(foreground="Black") )
lblLogin.bind("<Button-1>", switch)

header.pack()
createSeparator(rightPanelWc, height=25, bg=stylings.jotGreen)
email.pack(ipadx=10, ipady=10)
createSeparator(rightPanelWc, height=15, bg=stylings.jotGreen)
password.pack(ipadx=10, ipady=10)
createSeparator(rightPanelWc, height=15, bg=stylings.jotGreen)
btnSignup.pack(ipadx=8, ipady=10)
createSeparator(rightPanelWc, height=15, bg=stylings.jotGreen)
lblLogin.pack()
rightPanelWc.place(anchor="center", relx=0.5, rely=0.5)

# setting up the main window

def main():
    slWindow.title("Jot")
    screenW = slWindow.winfo_screenwidth()
    screenH = slWindow.winfo_screenheight()
    x,y = (screenW/2) - (w/2), (screenH/2) - (h/2)
    slWindow.geometry('%dx%d+%d+%d' % (w, h, x, y)) # setting the window position to center
    slWindow.resizable(False, False)
    slWindow.iconphoto(True, PhotoImage(file="images/jotLogo.png"))
    slWindow.mainloop()

if (__name__ == "__main__"):
    main()
else:
    exit()