import os
from tkinter.filedialog import askopenfilename
import json

class Obj():
	def __init__(self, id, dbms, carver_file, type, schema, record_cnt, page_size, evidence_file):
		self.id = id
		self.dbms = dbms
		self.carver_file = carver_file
		self.type = type
		self.page_cnt = 1
		self.schema = schema
		self.record_cnt = record_cnt
		self.page_size = page_size
		self.evidence_file = evidence_file
		self.basefile = os.path.basename(self.carver_file)
	
	def incrementPageCnt(self):
		self.page_cnt += 1
		
	def updateRecordCnt(self, nbr):
		self.record_cnt += nbr
		
	def getTreeLabel(self):
		label = str(self.id)
		return label
		
	def getSQL(self):
		return "INSERT INTO Objects VALUES (?, ?, ?, ?, ?, ?);"
		
				