from os import path
from functools import partial
try:
	from Tkinter import *
except ImportError:
	from tkinter import *
try:
	from ScrolledText import ScrolledText
except:
	from tkinter.scrolledtext import ScrolledText
import xerox

import os
curr_dir = os.getcwd()
import utils


def clear_session(root):
	root.destroy()
	# clear data in file
	with open(curr_dir + "/clix/clips_data", "wb") as f:
		print( "session cleared")
	# clear global clips
	utils.clips=[]
	clipboard(utils.clips)
	

class clipboard():
	def __init__(self, clips):
		"""
		initialization function
		"""
		# root (top level element) config
		H, W = 250, 300
		self.root = Tk()
		self.root.title("clix")
		self.root.minsize(width = W, height = H)
		self.position_window()

		img = PhotoImage(file = "icon.png")
		self.root.tk.call('wm', 'iconphoto', self.root._w, img)

		self.menu_bar=Menu(self.root)
		self.menu_bar.add_command(label="Clear", command= lambda: clear_session(self.root) )
		self.root.config(menu=self.menu_bar)

		# canvas to hold main scrollbar
		self.canvas = Canvas(self.root, height = H - 10, width = W - 20)
		self.canvas.pack(side = RIGHT, expand = True)

		# scrollbar config
		self.scrollbar = Scrollbar(self.root, command = self.canvas.yview)
		self.scrollbar.pack(side = RIGHT, fill = 'y')
		self.canvas.configure(yscrollcommand = self.scrollbar.set)

		# main frame (inside root) config
		self.mainFrame = Frame(self.root, padx = 5, pady = 5, bg = "white")
		self.mainFrame.pack(fill = BOTH, expand = True, side = TOP)

		# canvas window over mainFrame
		self.canvas.create_window((0,0), window = self.mainFrame, anchor = 'nw')
		self.mainFrame.bind('<Configure>', self.on_configure)

		# clipboard frames inside main frame
		self.colors = ['orange', 'tomato', 'gold']

		self.frames = []
		self.textBoxes = []
		self.no_of_clips=len(clips)

		for i in range(self.no_of_clips):
			self.add_new_clip(clips[i],i)

		self.check_new_clip()

		# call mainloop of Tk object

		self.root.mainloop()
		self.root.quit()
		utils.active=0


	def check_new_clip(self):
		if len(utils.clips)>self.no_of_clips:
			self.add_new_clip(utils.clips[-1],self.no_of_clips)
			self.no_of_clips+=1

		self.mainFrame.after(500,self.check_new_clip)


	def add_new_clip(self,clip,i):
		frame = Frame(self.mainFrame, padx = 5, pady = 5, bg = self.colors[i%3])
		
		Button(frame, text = "clip it", font = "Helvetica 12 bold",  
			    command = partial(self.copy_to_clipboard, i), relief = RAISED, 
			    padx = 5, pady = 5, bg = 'dark violet', fg = 'white').grid(row = 0, column = 0, ipady = 10)

		textBox = ScrolledText(frame, height = 3, width = 20,font = "Helvetica 12 bold")
		textBox.insert(END, clip)

		textBox.grid(row = 0, column = 1, sticky = E, padx = 5)
		self.textBoxes.append(textBox)

		frame.pack(fill = 'both', expand = True, pady = 5)
		self.frames.append(frame)


	def copy_to_clipboard(self, idx):
		"""
		function to copy text of frame no. idx to clipboard
		"""
		text = self.textBoxes[idx].get("1.0", END)
		xerox.copy(text)


	def on_configure(self, event):
		"""
		utility function to enable scrolling over canvas window
		"""
		self.canvas.configure(scrollregion = self.canvas.bbox('all'))


	def position_window(self):
		"""
		function to position window to current mouse position
		"""
		x, y = self.root.winfo_pointerxy()
		self.root.geometry('+%d+%d' % (x, y))	


if __name__ == "__main__":
	example_clips = ["hello", "copy it"]
	clipboard(example_clips)
