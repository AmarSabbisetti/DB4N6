"""
This box is used to display pages and their records.

"""

import tkinter as tk
from tkinter import ttk
from tkinter import *



class DataBox(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		self.parent = parent		
		self.tree=ttk.Treeview(self.parent,style="mystyle.Treeview")
		self.tree.grid(row = 0, column = 1, columnspan = 1, rowspan = 160, sticky=tk.NSEW)
		self.tree["columns"]=("PageID","ObjectID", "RowID", "Allocated", "Record")
		
		self.tree.column("#0", width=90, minwidth=50, stretch=tk.NO, anchor=tk.CENTER)
		self.tree.column("PageID", width=60, minwidth=50, stretch=tk.NO, anchor=tk.CENTER)
		self.tree.column("ObjectID", width=70, minwidth=50, anchor=tk.CENTER)
		self.tree.column("RowID", width=60, minwidth=50, stretch=tk.NO, anchor=tk.CENTER)
		self.tree.column("Allocated", width=80, minwidth=50, stretch=tk.NO, anchor=tk.CENTER)
		self.tree.column("Record", width=600, minwidth=50,stretch=tk.YES)


		self.tree.heading("#0",text="Offset",anchor=tk.CENTER)
		self.tree.heading("PageID", text="PageID",anchor=tk.CENTER)
		self.tree.heading("ObjectID", text="ObjectID",anchor=tk.CENTER)
		self.tree.heading("RowID", text="RowID",anchor=tk.CENTER)
		self.tree.heading("Allocated", text="Allocated",anchor=tk.CENTER)
		self.tree.heading("Record", text="Record",anchor=tk.CENTER)
		self.rec_cnt = 0	
		
		self.tree_cnt = 0	
		self.parent = ""
		
	def addNode(self, parent, posn, label, fields, color=None):
		if color is None:
			self.newNode = self.tree.insert(parent, posn, text=label, values=fields)
		else:
			self.newNode = self.tree.insert(parent, posn, text=label, values=fields, tags=color)
			self.tree.tag_configure('odd', background='#E8E8E8')
			self.tree.tag_configure('even', background='#DFDFDF')	
	

	def addPage(self, fields):
		self.tree_cnt += 1
		label = fields[0]
		values = (fields[1], fields[3], "", "", "")	
		self.addNode("", self.tree_cnt, label, values)
		self.parent = self.newNode
	
	def addRecord(self, fields):
		self.rec_cnt += 1
		label = fields[0]
		rec = fields[4][2:-1].split(', u')
		rec = ", ".join(rec)
		
		color = 'even'
		if self.rec_cnt % 2 == 1:
			color = 'odd'
		values = ("", "", fields[2], fields[3], rec)	
		self.addNode(self.parent, "end", label, values, (color,))
	
	def clearTree(self):
		self.tree_cnt = 0
		for i in self.tree.get_children():
			self.tree.delete(i)
