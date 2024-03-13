import tkinter as tk
from tkinter import *
import json
import sqlite3
import glob
import os
import src.EvidenceTreeBox as EvidenceBox
import src.DataBox as DataBox
import src.TreeDataBox as TreeDataBox
import src.Evidence as Evidence
import src.Instance as Instance
import src.QueryWindow as QueryWindow
import src.MenuBar as MenuBar
import src.lib as lib

def get_db_connection():
	"""Connect to the DBMS"""
	conn = sqlite3.connect('evidencetree.db') 
	return conn

def build_schema():
	"""Build the schema if it doesn't exist."""
	try:
		os.system("sqlite3 evidencetree.db < sql/TreeSchema.sql")
	except Exception as e:
		pass
		#print str(e)


class RootUI():	
	"""Step3. Create the main user interface window."""	
	def __init__(self, conn):	
		self.root = tk.Tk()
		#self.removeDBMSFiles()
		#tk.iconbitmap(default='transparent.ico')
		self.root.geometry("1000x500")
		self.root.title("DB4n6 Reporting")
		self.conn = conn
		
		MenuBar.MenuBar(self.root, self)
		self.addRecordDataBox()
		self.addStatisticsBox()
		self.addTreeDataBox()
		self.buildEvidenceTree()		

	def addRecordDataBox(self):
		"""The big centered UI box containing the records and metadata."""
		self.DataBox = DataBox.DataBox(self.root)

	def addStatisticsBox(self):
		"""The bottom left-hand side UI box containing statistic info."""
		self.StatisticsBox = TreeDataBox.TreeDataBox(self.root)

	def addTreeDataBox(self):
		"""The left-hand side UI box containing the evidence tree."""
		self.TreeBox = EvidenceBox.EvidenceTreeBox(self.root, self.StatisticsBox, self.DataBox, conn)

	def buildEvidenceTree(self):
		
		DB3Fs = glob.glob("/Users/amar/Desktop/DB3F/*")
		tree = {}
		cur=self.conn.cursor()

		"""Collect all of the disk images"""
		for DB3F in DB3Fs:
			evidence_name = self.getImageName(DB3F)
			if evidence_name not in tree.keys():
				NewEvidence = Evidence.Evidence(evidence_name, os.stat(DB3F).st_size)
				tree[evidence_name] = NewEvidence
				self.TreeBox.addNode(NewEvidence)
				NewEvidence.setTreeNode(self.TreeBox.newNode)
				values = (evidence_name, NewEvidence.size) #os.stat(item).st_size
				self.insertRecord(NewEvidence.getSQL(), values)
			ThisEvidence = tree[evidence_name]
			NewInstance = Instance.Instance(self.conn, DB3F, evidence_name)
			self.TreeBox.addNode(NewInstance, ThisEvidence.treeNode)
			NewInstance.setTreeNode(self.TreeBox.newNode)
			values = (evidence_name, NewInstance.carver_file, NewInstance.dbms, NewInstance.page_size, NewInstance.pages, NewInstance.storage, NewInstance.time, NewInstance.tool)
			self.insertRecord(NewInstance.getSQL(), values)
			for objectID, NewObject in NewInstance.objects.items():
				self.TreeBox.addNode(NewObject, NewInstance.treeNode)
				values = (NewObject.id, NewObject.type, NewObject.page_cnt, NewObject.schema, NewInstance.dbms, evidence_name)
				self.insertRecord(NewObject.getSQL(), values)
			self.conn.commit()

	def filterQuery(self):
		popup = QueryWindow.QueryWindow(self.root, "Filter Database Artifacts", self.conn)	
		w = popup.w	
		popup.buildWindow()
			
	def removeDBMSFiles(self):
		dbFiles = glob.glob("*.db")
		for dbFile in dbFiles:
			os.system("rm %s" % dbFile)

	def getImageName(self, file):
		input = open(file, "r")
		for line in input:
			header = json.loads(line)
			image_file = header['evidence_file']	
			return image_file

	def insertRecord(self, sql, values):
		cur = self.conn.cursor()
		try:
			cur.execute(sql,values)
		except Exception as e:
			pass
		self.conn.commit()		
	
def startup_data_display():	
	cur = conn.cursor()
	cur.execute("SELECT * FROM Evidence")
	evids = cur.fetchall()
	for row in evids:
		#add_evidence(row[0])
		
		cur.execute("SELECT * FROM Instance WHERE I_EvidenceFile = '%s'" % (str(row[0])))
		insts = cur.fetchall()
		for row2 in insts:
			evidence = row2[0] 
			carver_file = str(row2[1])
			dbms = row2[2]
			page_size = row2[3]
			pages = row2[4]
			#add_instance(carver_file, evidence)
			
			cur.execute("SELECT * FROM Objects WHERE O_InstFile = '%s'" % (str(carver_file))) 
			objs = cur.fetchall()
			for row3 in objs:
				OID = row3[0]
				type = row3[1]
				page_cnt = row3[2]
				


conn = get_db_connection() 	#Step1
#build_schema() 				#Step2
root = RootUI(conn)


mainloop()