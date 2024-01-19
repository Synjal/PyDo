import customtkinter
import mysql.connector

from lib import *
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkcalendar import DateEntry
from customtkinter import CTkToplevel, CTkLabel

taskList = []  # Objects list


# ----------------------------------------------------Pop up------------------------------------------------------------
def popupCalendar():
	top = CTkToplevel(root)
	top.title("Date picker")
	top.geometry('300x200')
	top.resizable(False, False)
	top.focus()

	CTkLabel(top, text='Set the deadline', text_color='#A0E014').pack(padx=10, pady=10)
	cal = DateEntry(top, width=12, background='#343638', borderwidth=2, anchor='w', justify='center')
	cal.pack(padx=10, pady=10)
	tkinter.Button(top, command=lambda: setGoalDate(cursor, top, cal, entry, tree, taskList, switch), image=addIcon,
								 bg='#242424', borderwidth=0).pack(padx=10, pady=10)


# ---------------------------------------------------Main frame---------------------------------------------------------
root = customtkinter.CTk()
root.title('PyDo')
root.geometry('600x550')
root.resizable(False, False)

# ---------------------------------------------------Styles-------------------------------------------------------------
style = ttk.Style()
style.theme_use("clam")

style.configure("DateEntry",
								bordercolor="#A0E014",
								fieldbackground="#242424",
								background="#242424",
								foreground="#A0E014")

style.configure("Treeview.Heading",
								background="#343638",
								foreground="#A0E014",
								font=("Helvetica", 13, 'bold'),
								borderwidth=0)

style.configure("Treeview",
								fieldbackground="#242424",
								font=("Helvetica", 12),
								bordercolor="#A0E014")

# ---------------------------------------------------Images-------------------------------------------------------------
playIcon 	 = ImageTk.PhotoImage(Image.open("assets/play.png"		 ).resize((60, 60)))
acceptIcon = ImageTk.PhotoImage(Image.open("assets/accept.png"	 ).resize((60, 60)))
deleteIcon = ImageTk.PhotoImage(Image.open("assets/delete.png"	 ).resize((60, 60)))
dateIcon 	 = ImageTk.PhotoImage(Image.open("assets/settings.png" ).resize((60, 60)))
addIcon 	 = ImageTk.PhotoImage(Image.open("assets/favourite.png").resize((60, 60)))
updateIcon = ImageTk.PhotoImage(Image.open("assets/refresh.png"	 ).resize((60, 60)))

# ---------------------------------------------------Components---------------------------------------------------------
# -----------------------TreeView------------------------
columns 			= ('Tasks'	 , 'State'	, 'Start'	 , 'End'		, 'Deadline')
column_widths = {'# 1': 300, '# 2': 90, '# 3': 90, '# 4': 90, '# 5': 90}

tree = ttk.Treeview(master=root,
										columns=columns,
										height=22,
										show='headings')

for col, width in column_widths.items(): tree.column(col, width=width, anchor=S)
for col in columns: tree.heading(col, text=col)

# -----------------------Buttons-------------------------
date 		 = tkinter.Button(master=root,
													command=popupCalendar,
													image=dateIcon,
													bg='#242424',
													borderwidth=0)

finished = tkinter.Button(master=root,
													command=lambda: endTask(cursor, entry, tree, taskList, switch),
													image=acceptIcon,
													bg='#242424',
													borderwidth=0)

new 		 = tkinter.Button(master=root,
												 command=lambda: addEntry(cursor, entry, tree, taskList, switch),
												 image=addIcon,
												 bg='#242424',
												 borderwidth=0)

start 	 = tkinter.Button(master=root,
												 command=lambda: startTask(cursor, entry, tree, taskList, switch),
												 image=playIcon,
												 bg='#242424',
												 borderwidth=0)

delete 	 = tkinter.Button(master=root,
													command=lambda: deleteEntry(cursor, entry, tree, taskList, switch),
													image=deleteIcon,
													bg='#242424',
													borderwidth=0)

update 	 = tkinter.Button(master=root,
													command=lambda: updateNameEntry(cursor, entry, tree, taskList, switch),
													image=updateIcon,
													bg='#242424',
													borderwidth=0)

# -----------------------Entry-------------------------
entry  = customtkinter.CTkEntry(master=root,
																width=420,
																border_color='#A0E014')

# -----------------------Switch------------------------
switch = customtkinter.CTkSwitch(master=root,
																 text="Show all",
																 command=lambda: dbShow(cursor, entry, tree, taskList, switch),
																 variable=customtkinter.StringVar(value='Off'), onvalue="On", offvalue="Off",
																 progress_color='#A0E014',
																 text_color="#A0E014")

# -----------------------Placement---------------------
new.place			(x=580, y=10 )
entry.place		(x=33 , y=20 )
tree.place		(x=40 , y=120)
date.place		(x=650, y=10 )
switch.place	(x=35 , y=60 )
start.place		(x=40 , y=603)
update.place	(x=243, y=603)
delete.place	(x=650, y=603)
finished.place(x=447, y=603)

# ----------------------------------------------------Database----------------------------------------------------------
database = mysql.connector.connect(
	host='localhost',
	user='root',
	password='')

cursor = database.cursor()
cursor.autocommit = True

# ------------------------------------------------------Run-------------------------------------------------------------
dbConnect(cursor, database)
dbShow(cursor, entry, tree, taskList, switch)
root.mainloop()
