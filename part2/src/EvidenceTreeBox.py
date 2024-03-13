"""
THis box is used to store the evidence tree describe in the paper.
"""


import tkinter as tk
from tkinter import ttk
from tkinter import *
#import Tkinter

class EvidenceTreeBox(tk.Frame):
	def __init__(self, parent, tree_data_box, data_box, conn):
		tk.Frame.__init__(self, parent)
		self.parent = parent		
		self.tree=ttk.Treeview(self.parent,style="mystyle.Treeview")
		self.tree.grid(row = 0, column = 0, columnspan = 1, rowspan = 100, sticky=tk.NSEW)
		style = ttk.Style()
		#style.configure("mystyle.Treeview", relief="raised", borderwidth=5)
		#style.configure("mystyle.Treeview", relief = 'flat', borderwidth = 10  )
		
		self.tree.column("#0", width=160, minwidth=50, stretch=tk.NO)
		self.tree.heading("#0",text="Evidence",anchor=tk.W)
		self.tree.bind("<Double-1>", self.OnDoubleClick)
		self.nodes = {}
		self.tree_data_box = tree_data_box
		self.data_box = data_box
		self.conn = conn
		self.page_limit = 100
	
	def addNode(self, object, parentNode=""):
		label = object.getTreeLabel()
		self.nodes[label] = object
		self.newNode = self.tree.insert(parentNode, "end", text=label, values=())		
		
	def OnDoubleClick(self, event):
		item = self.tree.selection()[0]
		label = self.tree.item(item, "text")	
		self.selected = self.nodes[label]
		object = self.nodes[label]
		self.data_box.clearTree()
		
		pages = []
		pg_limit = 10
		
		
		"""
		try:
			x = int(label)
			try:
				print "We're in"
				self.tree_data_box.displayInstance(object)
				#self.data_box.clearTree()
				
				sql = "SELECT * FROM Page WHERE P_InstFile LIKE '%s%s'"# AND P_InstFile IN (SELECT O_InstFile FROM Objects, Instance WHERE O_InstFile = I_DBMS AND I_EvidenceFile = '%s') "
				fields = ("%", object.evidence_file)#, object.evidence_file)  #("%", object.basefile)
				pages = self.getPages(sql, fields)			
				print pages
				cnt = 0
				for page in pages:
					cnt += 1
					self.data_box.addPage(page)
					sql = "SELECT * FROM Records WHERE R_PageID = %s" #And pageoffset
					fields = (page[1])
					records = self.getRecords(sql, fields)	
					for record in records:
						
						self.data_box.addRecord(record)
					if cnt == pg_limit:
						break
			except Exception as e:
				print str(e)
		except:
		"""
		try:
			x = int(len(label))
			
			self.tree_data_box.displayObject(object)
			fields = (object.evidence_file, object.dbms, label)
			sql = "SELECT * FROM Page WHERE P_InstFile = '%s' and P_DBMS = '%s' AND P_ObjectID = '%s'"
			pages = self.getPages(sql, fields)
			for page in pages:				
				self.data_box.addPage(page)					
				sql = "SELECT * FROM Records WHERE R_PageID = %s AND R_PageOffset = %s AND R_ObjectID = '%s'"
				fields = (page[1], page[0], label)
				records = self.getRecords(sql, fields)	
				for record in records:
					
					self.data_box.addRecord(record)
		except Exception as e:
			#print "EvidenceTreeBox 79", str(e)
			pass
	
	def getRecords(self, sql, values):
		cur = self.conn.cursor()
		sql = sql % values
		records = cur.execute(sql).fetchall()
		return records

	def getPages(self, sql, values):
		cur = self.conn.cursor()
		sql = sql % values
		records = cur.execute(sql).fetchall()
		
		if len(records) > self.page_limit:
			return records[:self.page_limit]		
		return records	
