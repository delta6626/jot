import os
import subprocess
import mysql.connector
from ctypes import windll
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import font
from tkinter import colorchooser
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

# Fetch user

userNameFilePath = os.path.dirname(os.path.abspath(__file__)).replace("\src", "\\userDetails.txt")
f = open(userNameFilePath, "r")
userDetails = f.readlines()
f.close()
userName = userDetails[0].split("@")[0].capitalize()
jotCursor.execute("SELECT id FROM users WHERE email = (%s)", (userDetails[0].rstrip(),))
for id in jotCursor.fetchone():
    userId = id

# Utiltiy

def getNoteText():
    f = open(filePath)
    details = json.load(f)
    if details["id"] == 0:
        pass;
    else:
        jotCursor.execute("SELECT noteText FROM notes WHERE noteId = (%s)", (details["id"],))
        global noteText
        noteText = jotCursor.fetchone()[0].decode("utf-8")
        
# Utility functions

def boldText(event):
    if "boldText" in textEditor.tag_names("sel.first"):
        textEditor.tag_remove("boldText", "sel.first", "sel.last")
    else:
        textEditor.tag_add("boldText", "sel.first", "sel.last")

def underlineText(event):
    if "underlineText" in textEditor.tag_names("sel.first"):
        textEditor.tag_remove("underlineText", "sel.first", "sel.last")
    else:
        textEditor.tag_add("underlineText", "sel.first", "sel.last")

def italicsText(event):
    if "italicsText" in textEditor.tag_names("sel.first"):
        textEditor.tag_remove("italicsText", "sel.first", "sel.last")
    else:
        textEditor.tag_add("italicsText", "sel.first", "sel.last")

def listItem(event):
    textEditor.insert("end", "• ")

def selectFont(event):
    fonts = font.families()
    fontSelector = Toplevel(editorWin)
    def updateFont(e):
        try:
            selected = display.get(display.curselection())
            textEditor.config(font=str(fonts[fonts.index(selected)])+" 20")
            fontSelector.destroy()
        except:
            messagebox.showerror(title="Font error", message="Sorry. This font is not supported.")

    fontSelector.title("Select Font")
    fontSelector.geometry("400x400")
    display = Listbox(fontSelector)
    display.pack(fill="both", expand="yes", side="left")
    scroll = Scrollbar(fontSelector)
    scroll.pack(side="right", fill="y", expand="no")
    scroll.configure(command=display.yview)
    display.configure(yscrollcommand=scroll.set)
    for item in fonts:
        display.insert("end",item)
    display.bind("<<ListboxSelect>>", updateFont)

def pickColor(event):
    color = colorchooser.askcolor(title="Choose color")
    textEditor.config(foreground=color[1])

def goHome(event):
    subprocess.Popen(["Python", "src/home.py"])
    exit()

def deleteNote(event):
    f = open(filePath)
    details = json.load(f)
    noteId = details["id"]

    yes = messagebox.askyesno("Delete Note", message="Are you sure you want to delete this note?")

    if(yes):
        if(noteId == 0 and editorWin.title()=="Untitled - Jot"):
            subprocess.Popen(["Python", "src/home.py"])
            exit()
        elif(editorWin.title()!="Untitled - Jot"):
            jotCursor.execute("DELETE FROM notes WHERE noteId = (%s)", (noteId,))
            messagebox.showinfo(title="Deleted Note", message="Note deleted successfully.")
            subprocess.Popen(["Python", "src/home.py"])
            exit()
    else:
        pass
        


def saveNote(event):
    if(editorWin.title() == "Untitled - Jot"):
        noteName = simpledialog.askstring(title="Name your note", prompt="Enter your note title....")
        if(str(noteName) == "" or noteName is None):
            messagebox.showerror(title="An error occured", message="Please provide a name to your note and try again.")
        else:
            t = textEditor.get("1.0", "end")
            saveText = bytearray(t, encoding="utf-8")
            jotCursor.execute("INSERT INTO notes (id, noteName, noteText) VALUES(%s,%s,%s)", (userId,noteName,saveText))
            editorWin.title(noteName+" - Jot")
            i = jotCursor.execute("SELECT LAST_INSERT_ID();")
            id = jotCursor.fetchone()[0]
            d = {
                "id":id,
                "title":noteName
            }
            f = open(filePath, "w")
            j = json.dumps(d)
            f.write(j)
            f.close()
            messagebox.showinfo(title="Note saved", message="Your note has been saved successfully.")
            
    else:
        t = textEditor.get("1.0", "end")
        saveText = bytearray(t, encoding="utf-8")
        f = open(filePath)
        details = json.load(f)
        i = details["id"]
        jotCursor.execute("UPDATE notes SET noteText = (%s) WHERE noteId = (%s)", (saveText, i))
        messagebox.showinfo(title="Note saved", message="Your note has been saved successfully.")

# UI

controlsPanel = Frame(editorWin, width=w, height=70, background=stylings.jotBlue)
boldIcon = PhotoImage(file=os.path.dirname(os.path.abspath(__file__)).replace("\src", "\\images\Bold.png"))
boldIconHover = PhotoImage(file=os.path.dirname(os.path.abspath(__file__)).replace("\src", "\\images\BoldHover.png"))
bold = Label(controlsPanel, image=boldIcon, background=stylings.jotBlue)
bold.bind("<Enter>", lambda e: bold.config(image=boldIconHover))
bold.bind("<Leave>", lambda e: bold.config(image=boldIcon))
bold.bind("<Button-1>", boldText)
bold.place(anchor="w",relx=0.010, rely=0.5)

underlineIcon = PhotoImage(file=os.path.dirname(os.path.abspath(__file__)).replace("\src", "\\images\_Underline.png"))
underlineIconHover = PhotoImage(file=os.path.dirname(os.path.abspath(__file__)).replace("\src", "\\images\_UnderlineHover.png"))
underline = Label(controlsPanel, image=underlineIcon, background=stylings.jotBlue)
underline.bind("<Enter>", lambda e: underline.config(image=underlineIconHover))
underline.bind("<Leave>", lambda e: underline.config(image=underlineIcon))
underline.bind("<Button-1>", underlineText)
underline.place(anchor="w",relx=0.045, rely=0.5)


italicsIcon = PhotoImage(file=os.path.dirname(os.path.abspath(__file__)).replace("\src", "\\images\Italics.png"))
italicsIconHover = PhotoImage(file=os.path.dirname(os.path.abspath(__file__)).replace("\src", "\\images\ItalicsHover.png"))
italics = Label(controlsPanel, image=italicsIcon, background=stylings.jotBlue)
italics.bind("<Enter>", lambda e: italics.config(image=italicsIconHover))
italics.bind("<Leave>", lambda e: italics.config(image=italicsIcon))
italics.bind("<Button-1>", italicsText)
italics.place(anchor="w",relx=0.08, rely=0.5)

listIcon = PhotoImage(file=os.path.dirname(os.path.abspath(__file__)).replace("\src", "\\images\List.png"))
listIconHover = PhotoImage(file=os.path.dirname(os.path.abspath(__file__)).replace("\src", "\\images\ListHover.png"))
list = Label(controlsPanel, image=listIcon, background=stylings.jotBlue)
list.bind("<Enter>", lambda e: list.config(image=listIconHover))
list.bind("<Leave>", lambda e: list.config(image=listIcon))
list.bind("<Button-1>", listItem)
list.place(anchor="w",relx=0.4475, rely=0.5)

fontIcon = PhotoImage(file=os.path.dirname(os.path.abspath(__file__)).replace("\src", "\\images\Font.png"))
fontIconHover = PhotoImage(file=os.path.dirname(os.path.abspath(__file__)).replace("\src", "\\images\FontHover.png"))
fontChanger = Label(controlsPanel, image=fontIcon, background=stylings.jotBlue)
fontChanger.bind("<Enter>", lambda e: fontChanger.config(image=fontIconHover))
fontChanger.bind("<Leave>", lambda e: fontChanger.config(image=fontIcon))
fontChanger.bind("<Button-1>", selectFont)
fontChanger.place(anchor="w",relx=0.4825, rely=0.5)

colorpickerIcon = PhotoImage(file=os.path.dirname(os.path.abspath(__file__)).replace("\src", "\\images\ColorPicker.png"))
colorpickerIconHover = PhotoImage(file=os.path.dirname(os.path.abspath(__file__)).replace("\src", "\\images\ColorPickerHover.png"))
colorpicker = Label(controlsPanel, image=colorpickerIcon, background=stylings.jotBlue)
colorpicker.bind("<Enter>", lambda e: colorpicker.config(image=colorpickerIconHover))
colorpicker.bind("<Leave>", lambda e: colorpicker.config(image=colorpickerIcon))
colorpicker.bind("<Button-1>", pickColor)
colorpicker.place(anchor="w",relx=0.5175, rely=0.5)

homeIcon = PhotoImage(file=os.path.dirname(os.path.abspath(__file__)).replace("\src", "\\images\Home.png"))
homeIconHover = PhotoImage(file=os.path.dirname(os.path.abspath(__file__)).replace("\src", "\\images\HomeHover.png"))
home = Label(controlsPanel, image=homeIcon, background=stylings.jotBlue)
home.bind("<Enter>", lambda e: home.config(image=homeIconHover))
home.bind("<Leave>", lambda e: home.config(image=homeIcon))
home.bind("<Button-1>", goHome)
home.place(anchor="e",x=1504, rely=0.5)

deleteIcon = PhotoImage(file=os.path.dirname(os.path.abspath(__file__)).replace("\src", "\\images\Delete.png"))
deleteIconHover = PhotoImage(file=os.path.dirname(os.path.abspath(__file__)).replace("\src", "\\images\DeleteHover.png"))
delete = Label(controlsPanel, image=deleteIcon, background=stylings.jotBlue)
delete.bind("<Enter>", lambda e: delete.config(image=deleteIconHover))
delete.bind("<Leave>", lambda e: delete.config(image=deleteIcon))
delete.bind("<Button-1>", deleteNote)
delete.place(anchor="e",x=1617, rely=0.5)

saveIcon = PhotoImage(file=os.path.dirname(os.path.abspath(__file__)).replace("\src", "\\images\Save.png"))
saveIconHover = PhotoImage(file=os.path.dirname(os.path.abspath(__file__)).replace("\src", "\\images\SaveHover.png"))
save = Label(controlsPanel, image=saveIcon, background=stylings.jotBlue)
save.bind("<Enter>", lambda e: save.config(image=saveIconHover))
save.bind("<Leave>", lambda e: save.config(image=saveIcon))
save.bind("<Button-1>", saveNote)
save.place(anchor="e",x=1730, rely=0.5)

controlsPanel.pack()
editorPanel = Frame(editorWin, width=w, height=h-70,background=stylings.jotGrayer)
editorPanel.pack()
textEditor = Text(editorPanel, border=0, font=stylings.textEditorFont, background=stylings.jotGrayer, foreground="white", insertbackground="white")
textEditor.place(anchor="center", relx=0.5, rely=0.5, width=w-50, height=h-100)
textEditor.focus()
getNoteText()
textEditor.insert(0.0, noteText)

textEditor.tag_configure("boldText", font=textEditor.cget("font")+" bold")
textEditor.tag_configure("italicsText", font=textEditor.cget("font")+" italic")
textEditor.tag_configure("underlineText", font=textEditor.cget("font")+" underline")

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