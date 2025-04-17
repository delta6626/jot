
---

# 📝 Basic Note Taking App (Python + MySQL + Tkinter)

This is one of my early Python projects I did in high schol — a simple note-taking app built as a way to learn how to connect Python to a MySQL database using `mysql-connector` for python, and to experiment with GUI programming using `Tkinter`.

⚠️ **Heads-up**: This isn't my proudest code! I knew what I was doing but I just didn't care enough to write clean code as I had a deadline to submit this project.

---

## 🚀 Features

- Add, view, and delete notes  
- GUI built using Tkinter  
- Data stored in a local MySQL database  

---

## 🛠️ Technologies Used

- Python 3  
- MySQL  
- `mysql-connector-python`  
- Tkinter  

---

## 📦 Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. **Install dependencies**
   ```bash
   pip install mysql-connector-python
   ```

3. **Configure your MySQL connection**

   Update the database connection details in the script:
   ```python
   mydb = mysql.connector.connect(
       host="localhost",
       user="your-username",
       password="your-password",
       database="your-database-name"
   )
   ```

---

## 🧩 Database Setup (Kinda DIY)

I, uh... didn’t save the original schema 😅  
If you want to run this project, you’ll likely have to **reverse-engineer the database** by reading through the code and figuring out what tables and fields it’s expecting.
Could be a fun little puzzle if you're into that kind of thing, and if you *do* end up recreating the schema, feel free to open a PR and help out the next brave soul 🙌

---

## 🔍 What Could Be Better

- Code organization (GUI + DB logic is a bit tangled)  
- Better error handling  
- UI polish  
- Security considerations

---

## ✨ Lessons Learned

- Hooking up Python with external databases  
- Building basic GUIs  
- Making local apps that persist data  

---

## 🧠 Future Plans

I might come back to this someday and rewrite it with Flask or PyQt—or at least clean up the code and add the missing schema for future me.

---

## 🙏 Acknowledgements

Shoutout to Stack Overflow, docs, and YouTube tutorials that kept me afloat while I figured this all out.

---
