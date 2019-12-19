from tkinter import *
from tkinter import ttk


root = Tk()
note = ttk.Notebook(root)



variables = {}
for name, colour, shape in Applist:
    variables[name + "_n"] = name



tab = Frame(note)
d=note.add(tab, text = "ddd")


#Button(root, text='+', command=add).grid(row=1, column=1)

note.grid(row=1)



root.mainloop()