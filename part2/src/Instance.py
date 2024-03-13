import os
from tkinter.filedialog import askopenfilename
import src.Object as o
import json

class Instance():
	def __init__(self, conn, id, e_id, carver_file=None):
		self.conn = conn
		self.id = id
		self.e_id = e_id
		self.objects = {}			
		self.pages = 0
		self.storage = 0
		self.carver_file = carver_file
		if self.carver_file is None:
			self.carver_file = id
			#askopenfilename()
		
		self.size = os.path.getsize(self.carver_file)
		self.basefile = os.path.basename(self.carver_file)
		
		try:
			self.getStatistics()
		except Exception as e:			
			print("Warning!!! Incorrect DB3F header format!", str(e))
		try:
			self.loadData()
		except Exception as e:
			pass

	def getStatistics(self):
		input = open(self.carver_file, "r")
		cnt = 0
		for line in input:
			cnt += 1
			page = json.loads(line)
			if cnt == 1:
				self.dbms = page['dbms']
				self.page_size = page['page_size']
				self.time = page['carving_time']
				self.tool = None
				#page['forensic_tool']
				continue
			objectID = str(page["object_id"])
			record_cnt = 0 #TODO
			try:
				object = self.objects[objectID]
				object.incrementPageCnt()
				
			except:
				type = page['page_type']
				schema = page['schema']
				clean_schema = []
				for dtype in schema:
					clean_schema.append(str(dtype))

				object = o.Obj(objectID, self.dbms, self.carver_file, type, str(clean_schema), record_cnt, self.page_size, self.e_id )
				#(self, id, dbms, carver_file, type, schema, record_cnt, page_size, evidence_file)
				self.objects[objectID] = object
		input.close()
		self.pages = cnt - 1
		self.storage = self.page_size * self.pages

		
	def loadData(self):
		input = open(self.carver_file, "r")
		cnt = 0
		for line in input:
			cnt += 1
			page = json.loads(line)
			if cnt == 1:				
				self.dbms = page['dbms']
				self.page_size = page['page_size']
				continue
			objectID = str(page["object_id"])
			record_cnt = 0 #TODO
			try:
				object = self.objects[objectID]
				#object.incrementPageCnt()
				
			except Exception as e:
				type = page['page_type']
				column_cnt = 0 #TODO
				object = o.Obj(objectID, self.dbms, self.carver_file, type, column_cnt, record_cnt, self.page_size)
				self.objects[objectID] = object
			
			records = page['records']
			row_cnt = 0
			for value in records:
				row_cnt +=1
				sql = "INSERT INTO Records VALUES (?, ?, ?, ?, ?, ?, ?)"	
				values = (value['offset'], page['offset'], value['row_id'], str(value['allocated']), str(value['values']), page['page_id'], objectID)
				self.insertRecord(sql, values)	
			
			sql = "INSERT INTO Page VALUES (?, ?, ?, ?, ?, ?)"
			if page['page_id'] is None:
				page['page_id'] = page['offset']
			values = (page['offset'], page['page_id'], row_cnt, page["object_id"], self.dbms, self.e_id)
			self.insertRecord(sql, values)					
			object.updateRecordCnt(row_cnt)				
			self.conn.commit()			
		input.close()
		self.pages = cnt - 1
		self.storage = self.page_size * self.pages
		
	def insertRecord(self, sql, values):
		cur = self.conn.cursor()
		try:
			cur.execute(sql, values)
		except Exception as e:
			#print str(e)
			pass
		self.conn.commit()

	def getTreeLabel(self):
		#label = "%s" % (self.basefile)
		label = self.dbms
		return label		
			
	def setTreeNode(self, node):
		self.treeNode = node	
		
	def getSQL(self):
		return "INSERT INTO Instance VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
		
		
		
		
		
		
		
		
		
		
		
