from tkinter import *

def on_click():
	button['text'] = 'Changed'

def on_click

if __name__ == '__main__':
	a = Tk(className = 'abc')
	button = Button(a)
	button['text'] = 'change!'
	button['command'] = on_click
	button.pack()
	label = Label(a)
	label['text'] = 'abcd'
	label.pack()
	a.mainloop()
