import tkinter as tk
#import tkMessageBox
from tkinter import *
import time
import json
#from tkFileDialog   import askopenfilename
#import ttk
import collections
import sqlite3
import glob
import os
#import lib as lib



class MenuBar():
	#The menu bar at the top of the main UI.
	def __init__(self, root, UI):
		self.root = root
		self.UI = UI
		self.menu = Menu(self.root)
		self.root.config(menu=self.menu)
		self.addFileTab()
		self.addFilterTab()
		
	def addFileTab(self):
		file = Menu(self.menu)
		#file.add_command(label = "Add Evidence (Disk Image)", command = self.root.insertEvidence)
		#file.add_command(label = "Process DB3F Files", command = add_instance)	
		#file.add_command(label = "Refresh Evidence Tree", command = self.UI.buildEvidenceTree)
		file.add_command(label = "Exit", command = self.root.destroy)	
		self.menu.add_cascade(label="File", menu=file)
	
	def addFilterTab(self):
		filter = Menu(self.menu)
		filter.add_command(label="Build Query", command=self.UI.filterQuery)	
		self.menu.add_cascade(label="Filter", menu=filter)