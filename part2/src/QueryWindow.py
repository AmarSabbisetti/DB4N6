import tkinter as tk
#import tkMessageBox
from tkinter import *
import time
import json
from tkinter.filedialog import askopenfilename
from tkinter import ttk
import json
import datetime



#class QueryWindow(tk.Frame):	
class QueryWindow(tk.Frame):
	cq = 0
	def __init__(self, parentWindow, title, conn):
		QueryWindow.cq +=1
		self.parentWindow = parentWindow
		self.conn = conn
		tk.Frame.__init__(self, self.parentWindow)
		self.w = Toplevel()
		self.w.geometry("600x600")
		self.w.title(title)

		menu = Menu(self.w)
		self.w.config(menu=menu)
		file = Menu(menu)
		file.add_command(label = "Run", command = self.run_data)	
		file.add_command(label = "Exit", command = self.w.destroy)	
		menu.add_cascade(label="File", menu=file)		
		
	def setBoxLabel(self):
		self.query = ""
		self.query += "SELECT *\n"
		self.query += "FROM DB3F_File.Object O \n"
		self.query += "    JOIN DB3F_File.Page P \n"
		self.query += "    JOIN DB3F_File.Record R \n"
		self.query += "WHERE "
		#self.query += "WHERE O.ObjectID = P.ObjectID \n"
		#self.query += "AND P.Offset = R.PageOffset"
	
		self.label = tk.Label(self.frame, text=self.query, bd=5, justify="left")
		self.label.grid(row = 1, column = 1, sticky=W)
		
	def setInputBox(self):
		self.newEntry = Text(self.frame, height=12, width=65)
		self.newEntry.grid(row = 2, column = 1, sticky=W)
		self.newEntry.insert("1.0", "")
		
		
	def buildWindow(self):
		tk.Frame.__init__(self, self.w)#, width=500, height=500, padx = 10, pady = 
		self.frame = tk.Frame(self.w, bd=5, relief=GROOVE)
		self.frame = tk.Frame(self.w, bd=5, relief=GROOVE, width=600, height=600)#, bg='cyan')
		self.frame.grid(row=0, column=0, sticky=W)# columnspan = 100, rowspan = 100)		
		self.setBoxLabel()
		self.setInputBox()
		#Button(self, text='Run', command=self.run_data)
		"""button_frame = tk.Frame
		button_frame.pack(fill=tk.X, side=tk.BOTTOM)
		run_button = tk.Button(button_frame, text='Run')
		button_frame.columnconfigure(1, weight=1)
		run_button.grid(row=0, column=1, sticky=tk.W + tk.E)
		run_button.add_command(label = "Run", command = self.run_data)"""
	def run_data(self):
		self.query = ""
		#self.query += "SELECT *\n"
		#self.query += "FROM Instance, Object, Page, Record \n"
		#self.query += "WHERE I_DB3F_File = O_DB3F_File \n"
		#self.query += "AND O_DB3F_File = P_DB3F_File \n"
		#self.query += "AND O_ID = P_ObjectID \n"
		#self.query += "AND P_Offset = R_PageOffset \n"	
		self.query = """		
				SELECT *
				FROM Instance, Objects, Page, Records
				WHERE I_EvidenceFile = O_InstFile
				AND I_DBMS = O_DBMS
				AND O_ID = P_ObjectID
				AND P_DBMS = O_DBMS
				AND P_InstFile = O_InstFile
				AND P_Offset = R_PageOffset
				AND R_PageID = P_PageID
				AND R_ObjectID = P_ObjectID AND \n"""
		
		self.query = self.query + self.newEntry.get("1.0", END) + ";"
		#print(self.query)
		outfile = "FilteredResults/"+str(QueryWindow.cq)+".json" #(str(datetime.datetime.now()))
		out = open(outfile, "w")
		out.write("%s\n" % self.getDB3Fheader())
		cur = self.conn.cursor()
		cur.execute(self.query)
		pages = {}
		for line in cur.fetchall():
			values = line[8:]
			page_offset = values[6]
			page_id = values[7]
			object_id = int(values[0])
			page_type = values[1]
			schema = values[3]
			
			record_offset =  values[12]
			
			record_allocated = values[15]
			if record_allocated == "True":
				record_allocated = True
			else:
				record_allocated = False
			
			row_id = values[14]
			record_values = values[16]
			
			output = {
			'offset': page_offset,
			'page_id': page_id, 
			'object_id': object_id, 
			#'recordcnt': header['record_cnt'],
			'page_type': page_type,
			'schema': schema,
			'records': [{'offset': record_offset, 'allocated': record_allocated, 'row_id': row_id, 'values': record_values}]					
			}
			output = json.dumps(output)
			out.write("%s%s" % (output, "\n"))

	def getDB3Fheader(self):
		db_type = None
		pg_sz = None
		evidence_file = None
		dct = {"@context": {"name": None, "uri": None}, "dbms": db_type, "page_size": pg_sz, "forensic_tool": "Filtered DBCarver", "carving_time": str(datetime.datetime.now()), "evidence_file": evidence_file}	
		output = json.dumps(dct)
		return output
		
	def getDB3Fpage(self, values):
		return str(values)












