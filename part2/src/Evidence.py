import os
from tkinter.filedialog import askopenfilename

class Evidence():
	id = 0
	def __init__(self, file=None, size=None):
		self.id += 1
		if file is None:
			self.file = askopenfilename()
		else:
			self.file = file
		self.size = size #os.path.getsize(self.file)
		self.basefile = os.path.basename(self.file)

	def getTreeLabel(self):
		#MBs = round(((self.size/1.0)/2**20), 2)
		#label = "%s [%s MB]" % (self.basefile, MBs)
		label = "%s" % (self.basefile)
		return label
		
	def setTreeNode(self, node):
		self.treeNode = node
		
	def getSQL(self):
		return "INSERT INTO Evidence VALUES (?, ?);"