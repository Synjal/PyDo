import tkinter
import tkinter.messagebox

from Task import Task
from datetime import datetime


def dbConnect(cursor, database):
	"""Database connection"""
	createDB = "CREATE DATABASE IF NOT EXISTS pydo"

	createTable = "CREATE TABLE IF NOT EXISTS task (" \
								"id int NOT NULL AUTO_INCREMENT," \
								"name VARCHAR(255) COLLATE utf8mb4_bin NOT NULL," \
								"startDate date DEFAULT NULL," \
								"endDate date DEFAULT NULL," \
								"goalDate date NOT NULL," \
								"state TINYINT NOT NULL DEFAULT '0'," \
								"PRIMARY KEY (id))"

	cursor.execute(createDB)
	database.database = 'pydo'
	cursor.execute(createTable)


def clean(entry, tree, taskList):
	"""Clean all the components"""
	taskList.clear()
	entry.delete(0, tkinter.END)
	tree.delete(*tree.get_children())


def dbShow(cursor, entry, tree, taskList, switch):
	"""Fill the Treeview, create objects from database and update the objects list """
	showAll = True if switch.get() != 'Off' else False
	state_mapping = {0: "Not started", 1: "Started", 2: "Finished"}

	def convertDate(rawDate): return rawDate.strftime("%d/%m/%Y") if rawDate is not None else ""

	def insert():
		tree.insert('',
								tkinter.END,
								values=(task.name,
											  state_mapping.get(task.state, "Unknown state"),
											  convertDate(task.startDate),
											  convertDate(task.endDate),
											  convertDate(task.goalDate)),
								tags=(task.state,))

	clean(entry, tree, taskList)

	select = "SELECT * FROM task"
	cursor.execute(select)
	rows = cursor.fetchall()

	for row in rows: taskList.append(Task(row[1], row[4], row[2], row[3], row[5]))
	for task in taskList: insert() if showAll or (not showAll and task.state != 2) else None

	colorTree(tree)


def colorTree(tree):
	"""Update the Treeview with row colors based on the tag name"""
	colors = ['#DB949B', '#FFD085', '#98D7AE']
	for c, color in enumerate(colors): tree.tag_configure(str(c), background=color)


def addEntry(cursor, entry, tree, taskList, switch):
	"""Insert new task in database and show()"""
	if entry.get() != "":
		insert = "INSERT INTO task(name) VALUES ('" + entry.get() + "')"
		cursor.execute(insert)
		dbShow(cursor, entry, tree, taskList, switch)
	else: tkinter.messagebox.showinfo("Error", "Come on, you forgot the name...")


def deleteEntry(cursor, entry, tree, taskList, switch):
	"""Delete task in database and show()"""
	try:
		sql = "DELETE FROM task WHERE	name = '" + tree.item(tree.focus()).get("values")[0] + "'"
		cursor.execute(sql)
		dbShow(cursor, entry, tree, taskList, switch)
	except: tkinter.messagebox.showinfo("Error", "No task selected")


def updateNameEntry(cursor, entry, tree, taskList, switch):
	"""Update task name in database and show()"""
	try:
		sql = "UPDATE task SET name = '" + entry.get() + "' WHERE	name = '" + tree.item(tree.focus()).get("values")[0] + "'"
		cursor.execute(sql)
		dbShow(cursor, entry, tree, taskList, switch)
	except: tkinter.messagebox.showinfo("Error", "No task selected")


def startTask(cursor, entry, tree, taskList, switch):
	"""Update task start date in database and show()"""
	try:
		sql = "UPDATE task SET startDate = '" + datetime.now().strftime(
			"%Y-%m-%d") + "', state = '1' WHERE	name = '" + tree.item(tree.focus()).get("values")[0] + "'"
		cursor.execute(sql)
		dbShow(cursor, entry, tree, taskList, switch)
	except: tkinter.messagebox.showinfo("Error", "No task selected")


def endTask(cursor, entry, tree, taskList, switch):
	"""Update task end date in database and show()"""
	try:
		sql = "UPDATE task SET endDate = '" + datetime.now().strftime(
			"%Y-%m-%d") + "', state = '2' WHERE name = '" + tree.item(tree.focus()).get("values")[0] + "'"
		cursor.execute(sql)
		dbShow(cursor, entry, tree, taskList, switch)
	except: tkinter.messagebox.showinfo("Error", "No task selected")


def setGoalDate(cursor, top, cal, entry, tree, taskList, switch):
	"""Update task goal date in database and show()"""
	sql = ("UPDATE task SET goalDate = '" + str(cal.get_date()) + "' \
				 WHERE	name = '" + tree.item(tree.focus()).get("values")[0] + "'")
	cursor.execute(sql)
	dbShow(cursor, entry, tree, taskList, switch)
	top.destroy()
