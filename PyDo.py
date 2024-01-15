from tkcalendar import DateEntry
from datetime import datetime
from tkinter import *

import mysql.connector

from Task import Task

database = mysql.connector.connect(
	host='localhost',
	user='root',
	password='',
	database='pydo'
)
cursor = database.cursor()
taskList = []


def clean():
	entry.delete(0, END)
	ListName.delete(0, END)
	ListGoalDate.delete(0, END)
	ListState.delete(0, END)
	taskList.clear()

	select = "SELECT * FROM task"
	cursor.execute(select)
	rows = cursor.fetchall()

	for row in rows:
		taskList.append(Task(row[1], row[4], row[2], row[3], row[5]))


def dbShow():
	if showFinished['text'] == 'Show tasks':
		showFinishedTasks()
		return

	clean()

	for i in range(len(taskList)):
		match taskList[i].state:
			case 0:
				state = 'Not started'
			case 1:
				state = 'Started'
		if taskList[i].state != 2:
			ListName.insert(i, taskList[i].name)
			if taskList[i].goalDate is not None:
				ListGoalDate.insert(i, taskList[i].goalDate.strftime("%x"))
			ListState.insert(i, state)


def showFinishedTasks():
	clean()
	for i in range(len(taskList)):
		if taskList[i].state == 2:
			ListName.insert(i, taskList[i].name)
			if taskList[i].goalDate is not None:
				ListGoalDate.insert(i, taskList[i].goalDate.strftime("%x"))
			ListState.insert(i, 'Finished')


def FinishedTasks():
	if showFinished['text'] != 'Show finished tasks':
		showFinished['text'] = 'Show finished tasks'
		dbShow()
		return

	showFinished['text'] = 'Show tasks'
	showFinishedTasks()


def addEntry():
	if entry.get() is not None:
		insert = "INSERT INTO task(name) VALUES ('" + entry.get() + "')"
		cursor.execute(insert)
		database.commit()
		dbShow()


def deleteEntry():
	sql = "DELETE FROM task WHERE	name = '" + ListName.get(ListName.curselection()) + "'"
	cursor.execute(sql)
	database.commit()
	dbShow()


def updateNameEntry():
	sql = "UPDATE task SET name = '" + entry.get() + "' WHERE	name = '" + ListName.get(ListName.curselection()) + "'"
	cursor.execute(sql)
	database.commit()
	dbShow()


def updateGoalDateEntry():
	sql = "UPDATE task SET goalDate = '" + entry.get() + "' WHERE	name = '" + ListName.get(ListName.curselection()) + "'"
	cursor.execute(sql)
	database.commit()
	dbShow()


def startTask():
	sql = "UPDATE task SET startDate = '" + datetime.now().strftime(
		"%Y-%m-%d") + "', state = '1' WHERE	name = '" + ListName.get(
		ListName.curselection()) + "'"
	cursor.execute(sql)
	database.commit()
	dbShow()


def endTask():
	sql = "UPDATE task SET endDate = '" + datetime.now().strftime(
		"%Y-%m-%d") + "', state = '2' WHERE name = '" + ListName.get(
		ListName.curselection()) + "'"
	cursor.execute(sql)
	database.commit()
	dbShow()


def updateNameAndGoalEntry(ID, name, goalDate):
	sql = "UPDATE task SET name = '" + name + "', goalDate = '" + goalDate + "' WHERE id = " + str(ID)
	cursor.execute(sql)
	database.commit()
	dbShow()


def buttons(event):
	new['state'] = DISABLED if entry.get() == "" else NORMAL
	update['state'] = DISABLED if entry.get() == "" else NORMAL


def clickNormal(event):
	start['state'] = NORMAL
	finished['state'] = NORMAL
	delete['state'] = NORMAL
	date['state'] = NORMAL


def clickDisable(event):
	start['state'] = DISABLED
	finished['state'] = DISABLED
	delete['state'] = DISABLED
	date['state'] = DISABLED


def popupCalendar():
	def setGoalDate():
		sql = "UPDATE task SET goalDate = '" + str(cal.get_date()) + "' WHERE	name = '" + ListName.get(
			ListName.curselection()) + "'"
		cursor.execute(sql)
		database.commit()
		dbShow()

	top = Toplevel(root)
	top.geometry('200x150')
	top.resizable(False, False)
	Label(top, text='Choose date').pack(padx=10, pady=10)
	cal = DateEntry(top, width=12, background='darkblue', foreground='white', borderwidth=2)
	cal.pack(padx=10, pady=10)
	Button(top, text='Set', command=setGoalDate).pack(padx=10)


root = Tk()
root.title('PyDo')
root.geometry('500x550')
root.resizable(False, False)

entry = Entry(root, width=60)
entry.bind('<Key>', buttons)
entry.place(x=20, y=20)

Label(root, text='Tasks :'	 ).place(x=20 , y=80)
Label(root, text='State :'	 ).place(x=205, y=80)
Label(root, text='Deadline :').place(x=330, y=80)

ListName = 		 Listbox(root, width=30, height=22, activestyle=DOTBOX, selectmode=SINGLE)
ListGoalDate = Listbox(root, width=20, height=22, activestyle=DOTBOX, selectmode=SINGLE)
ListState = 	 Listbox(root, width=20, height=22, activestyle=DOTBOX, selectmode=SINGLE)

ListName.bind(		'<<ListboxSelect>>', clickNormal)
ListGoalDate.bind('<<ListboxSelect>>', clickDisable)
ListState.bind(		'<<ListboxSelect>>', clickDisable)

ListName.place(		 x=20 , y=100)
ListGoalDate.place(x=330, y=100)
ListState.place(	 x=205, y=100)

new 		 		 = Button(root, text='New task'						, width=12, command=addEntry			 , state=DISABLED)
date 		 		 = Button(root, text='Set a deadline' 		, width=12, command=popupCalendar	 , state=DISABLED)
start 	 		 = Button(root, text='Start'   						, width=13, command=startTask			 , state=DISABLED)
finished 		 = Button(root, text='Done'		    				, width=13, command=endTask				 , state=DISABLED)
update 	 		 = Button(root, text='Update'  						, width=13, command=updateNameEntry, state=DISABLED)
delete 	 		 = Button(root, text='Delete'  						, width=13, command=deleteEntry		 , state=DISABLED)
showFinished = Button(root, text='Show finished tasks', width=65, command=FinishedTasks)

new.place(				 x=400, y=20 )
date.place(				 x=400, y=47 )
start.place(			 x=20 , y=480)
finished.place(		 x=140, y=480)
update.place(			 x=260, y=480)
delete.place(			 x=380, y=480)
showFinished.place(x=16 , y=510)

dbShow()
root.mainloop()
