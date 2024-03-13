"""
THis box is used to show high-level information about each tree object select. For example a DBMS
instance or a object ID.
"""

import tkinter as tk
#import ttk
from tkinter import ttk
#import Tkinter

class TreeDataBox(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		self.parent = parent		
		self.tree=ttk.Treeview(self.parent,style="mystyle.Treeview")
		s = ttk.Style()
		s.configure('mystyle.Treeview', rowheight=35) 
		
		self.tree.grid(row = 100, column = 0, columnspan = 1, rowspan = 60, sticky=tk.NSEW)
		
		#style = ttk.Style()
		#style.configure("mystyle.Treeview", relief="flat")
		
		self.tree["columns"] = ("Values")
		
		self.tree.column("#0", width=80, minwidth=50, stretch=tk.NO)
		self.tree.column("Values", width=80, minwidth=50, stretch=tk.NO)
		
		self.tree.heading("#0",text="Properties",anchor=tk.W)
		self.tree.heading("Values",text="",anchor=tk.W)
		
	def addNode(self, label, value):
		self.newNode = self.tree.insert("", "end", text=label, values=(value))	

	def clearTree(self):
		for i in self.tree.get_children():
			self.tree.delete(i)
		
	def displayInstance(self, object):
		self.clearTree()
		MBs = round(((object.page_size * object.pages)/1.0)/2**20, 2)
		data = {"DBMS": object.dbms, "Page Size": object.page_size, "Pages": object.pages, "Storage(MBs)": MBs}
		
		for key, value in data.items():
			self.addNode(key, value)
		
	def displayObject(self, object):
		self.clearTree()
		try:
			MBs = str(round(((object.page_size * object.page_cnt)/1.0)/2**20, 2)) + "(MB)"
			page_size = "%s(KB)" % (object.page_size/1024)
			avg_rec = (object.record_cnt * 1.00)/object.page_cnt
			schema = str(object.schema).replace("'", "")
			schema = schema.replace("[", "")
			schema = schema.replace("]", "")
			schema = schema.replace(",", "")
			schema = schema.replace(" ", "")
			schema = schema.replace("Nbr", "N")
			schema = schema.replace("Str", "S")
			#data = {"1.ObjectID": str(object.id), "2.Type": object.type, "3.Schema": schema, "4.Pages": object.page_cnt, "5.Page Size": page_size, "6.Storage": MBs, "7.Records": object.record_cnt, "8.Avg Rec/Page": avg_rec}
			data = {"1.ObjectID": str(object.id), "2.Type": object.type, "3.Schema": schema, "4.Pages": object.page_cnt, "5.Page Size": page_size, "6.Storage": MBs}
			for key, value in sorted(data.items()):
				self.addNode(key[2:], value)		
		except:
			data = {"N/A": "N/A"}
			for key, value in data.items():
				self.addNode(key, value)
		
	