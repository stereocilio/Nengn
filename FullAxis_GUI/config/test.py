from tkinter import *
from tkinter import ttk

count = 0
print("aqui")
root = Tk()
note = ttk.Notebook(root)

def add():
	global count
	exec("tab{} = Frame(note)".format(count))
	exec("d{0}=note.add(tab{0}, text = {0})".format(count))
	count =count+1

def addframe():
	Frame(d3, background='red').pack(fill=BOTH)


Button(root, text='+', command=add).grid(row=1, column=1)
Button(root, text='()', command=addframe).grid(row=1, column=2)

note.grid(row=1)



root.mainloop()