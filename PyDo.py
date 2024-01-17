import tkinter
from datetime import datetime
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *

from PIL import ImageTk, Image

import customtkinter
import mysql.connector
from customtkinter import CTkToplevel, CTkLabel
from tkcalendar import DateEntry
from Task import Task

createDB = "CREATE DATABASE IF NOT EXISTS pydo"
createTable = "CREATE TABLE IF NOT EXISTS task (" \
							"id int NOT NULL AUTO_INCREMENT," \
							"name VARCHAR(255) COLLATE utf8mb4_bin NOT NULL," \
							"startDate date DEFAULT NULL," \
							"endDate date DEFAULT NULL," \
							"goalDate date NOT NULL," \
							"state TINYINT NOT NULL DEFAULT '0' COMMENT '0 = To do\r\n1 = Running\r\n2 = Finished'," \
							"PRIMARY KEY (id))"

database = mysql.connector.connect(
	host='localhost',
	user='root',
	password='',
)
cursor = database.cursor()

cursor.execute(createDB)
database.database = 'pydo'
cursor.execute(createTable)

taskList = []


def clean():
	entry.delete(0, END)

	taskList.clear()
	tree.delete(*tree.get_children())

	select = "SELECT * FROM task"
	cursor.execute(select)
	rows = cursor.fetchall()

	for row in rows:
		taskList.append(Task(row[1], row[4], row[2], row[3], row[5]))


def dbShow():
	clean()

	if switch.get() != 'Off':
		showFinishedTasks()
		return

	for task in taskList:
		state = "Not started" if task.state == 0 else "Started"
		if task.state != 2:
			startDate = task.startDate.strftime("%d/%m/%Y") if task.startDate is not None else ""
			endDate = task.endDate.strftime("%d/%m/%Y") if task.endDate is not None else ""
			goalDate = task.goalDate.strftime("%d/%m/%Y") if task.goalDate is not None else ""
			tree.insert('', END, values=(task.name, state, startDate, endDate, goalDate), tags=(task.state,))

	colorTree()


def showFinishedTasks():
	clean()

	for task in taskList:
		match task.state:
			case 0:
				state = "Not started"
			case 1:
				state = "Started"
			case 2:
				state = "Finished"
		startDate = task.startDate.strftime("%d/%m/%Y") if task.startDate is not None else ""
		endDate = task.endDate.strftime("%d/%m/%Y") if task.endDate is not None else ""
		goalDate = task.goalDate.strftime("%d/%m/%Y") if task.goalDate is not None else ""
		tree.insert('', END, values=(task.name, state, startDate, endDate, goalDate), tags=(task.state,))
	colorTree()


def colorTree():
	tree.tag_configure('0', background='#DB949B')
	tree.tag_configure('1', background='#FFD085')
	tree.tag_configure('2', background='#98D7AE')


def FinishedTasks():
	if switch.cget("text") != 'On':
		dbShow()
		return

	showFinishedTasks()


def addEntry():
	if entry.get() is not None:
		insert = "INSERT INTO task(name) VALUES ('" + entry.get() + "')"
		cursor.execute(insert)
		database.commit()
		dbShow()


def deleteEntry():
	sql = "DELETE FROM task WHERE	name = '" + tree.item(tree.focus()).get("values")[0] + "'"
	cursor.execute(sql)
	database.commit()
	dbShow()


def updateNameEntry():
	sql = "UPDATE task SET name = '" + entry.get() + "' WHERE	name = '" + tree.item(tree.focus()).get("values")[0] + "'"
	cursor.execute(sql)
	database.commit()
	dbShow()


def updateGoalDateEntry():
	sql = "UPDATE task SET goalDate = '" + entry.get() + "' \
				 WHERE	name = '" + tree.item(tree.focus()).get("values")[0] + "'"
	cursor.execute(sql)
	database.commit()
	dbShow()


def startTask():
	sql = "UPDATE task SET startDate = '" + datetime.now().strftime(
		"%Y-%m-%d") + "', state = '1' WHERE	name = '" + tree.item(tree.focus()).get("values")[0] + "'"
	cursor.execute(sql)
	database.commit()
	dbShow()


def endTask():
	sql = "UPDATE task SET endDate = '" + datetime.now().strftime(
		"%Y-%m-%d") + "', state = '2' WHERE name = '" + tree.item(tree.focus()).get("values")[0] + "'"
	cursor.execute(sql)
	database.commit()
	dbShow()


def popupCalendar():
	def setGoalDate():
		sql = "UPDATE task SET goalDate = '" + str(cal.get_date()) + "' \
					 WHERE	name = '" + tree.item(tree.focus()).get("values")[0] + "'"
		cursor.execute(sql)
		database.commit()
		dbShow()

	top = CTkToplevel(root)
	top.title("Date picker")
	top.geometry('300x200')
	top.resizable(False, False)
	top.focus()
	style.theme_use("clam")
	style.configure("DateEntry", bordercolor="#A0E014", fieldbackground="#242424", background="#242424",
									foreground="#A0E014")
	CTkLabel(top, text='Set the deadline', text_color='#A0E014').pack(padx=10, pady=10)
	cal = DateEntry(top, width=12, background='#343638', borderwidth=2, anchor='w', justify='center')
	cal.pack(padx=10, pady=10)
	tkinter.Button(top, command=setGoalDate, image=addIcon, bg='#242424', borderwidth=0).pack(padx=10, pady=10)


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

root = customtkinter.CTk()
root.title('PyDo')
root.geometry('600x550')
root.resizable(False, False)
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", background="#343638", foreground="#A0E014",
								font=("Helvetica", 13, 'bold'), borderwidth=0)
style.configure("Treeview", fieldbackground="#242424", font=("Helvetica", 12),
								bordercolor="#A0E014")

acceptIcon = ImageTk.PhotoImage(Image.open("assets/accept.png").resize((60, 60)))
deleteIcon = ImageTk.PhotoImage(Image.open("assets/delete.png").resize((60, 60)))
playIcon = ImageTk.PhotoImage(Image.open("assets/play.png").resize((60, 60)))
updateIcon = ImageTk.PhotoImage(Image.open("assets/refresh.png").resize((60, 60)))
dateIcon = ImageTk.PhotoImage(Image.open("assets/settings.png").resize((60, 60)))
addIcon = ImageTk.PhotoImage(Image.open("assets/favourite.png").resize((60, 60)))

entry = customtkinter.CTkEntry(root, width=420, border_color='#A0E014')
switch = customtkinter.CTkSwitch(root, text="Show all", command=FinishedTasks,
																 variable=customtkinter.StringVar(value='Off'), onvalue="On", offvalue="Off",
																 progress_color='#A0E014', text_color="#A0E014")

columns = ('Tasks', 'State', 'Start', 'End', 'Deadline')
tree = ttk.Treeview(root, columns=columns, height=22, show='headings')
tree.column("# 1", width=300, anchor=S)
tree.column("# 2", width=90, anchor=S)
tree.column("# 3", width=90, anchor=S)
tree.column("# 4", width=90, anchor=S)
tree.column("# 5", width=90, anchor=S)
tree.heading('Tasks', text='Tasks')
tree.heading('State', text='Status')
tree.heading('Start', text='Started')
tree.heading('End', text='Ended')
tree.heading('Deadline', text='Deadline')

new = tkinter.Button(root, command=addEntry, image=addIcon, bg='#242424', borderwidth=0)
date = tkinter.Button(root, command=popupCalendar, image=dateIcon, bg='#242424', borderwidth=0)
start = tkinter.Button(root, command=startTask, image=playIcon, bg='#242424', borderwidth=0)
finished = tkinter.Button(root, command=endTask, image=acceptIcon, bg='#242424', borderwidth=0)
update = tkinter.Button(root, command=updateNameEntry, image=updateIcon, bg='#242424', borderwidth=0)
delete = tkinter.Button(root, command=deleteEntry, image=deleteIcon, bg='#242424', borderwidth=0)

entry.place(x=33, y=20)
tree.place(x=40, y=120)
switch.place(x=35, y=60)
new.place(x=580, y=10)
date.place(x=650, y=10)
start.place(x=40, y=603)
update.place(x=243, y=603)
finished.place(x=447, y=603)
delete.place(x=650, y=603)

dbShow()
root.mainloop()
