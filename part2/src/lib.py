
def add_instance(file = None, e_id = None):
	i_id = len(instances.keys()) + 1
	if e_id is None:
		e_id = new_ebox.selected.file
	
	new_instance = Instance.Instance(conn, i_id, e_id, file)
	try:
		new_instance.getStatistics()
	except Exception as e:
		print("Run.py 60", str(e))
		pass
	instances[i_id] = new_instance
	evidence = evidences[e_id]
	new_ebox.addNode(new_instance, evidence.treeNode)
	new_instance.setTreeNode(new_ebox.newNode)
	
	sql = "INSERT INTO Instance VALUES (?, ?, ?, ?, ?, ?, ?, ?)"	
	values = (e_id, new_instance.carver_file, new_instance.dbms, new_instance.page_size, new_instance.pages, new_instance.storage, new_instance.time, new_instance.tool)
	insertRecord(sql, values)	
	instanceNode = new_ebox.newNode
	
	
	for key, object in new_instance.objects.iteritems():
		new_ebox.addNode(object, instanceNode)
		loadDecision = testDataLoad(object.id)
		if not loadDecision:
			sql = "INSERT INTO Objects VALUES (?, ?, ?, ?, ?)"
			values = (object.id, object.type, object.page_cnt, object.schema, object.carver_file)
			insertRecord(sql, values)		
	if not loadDecision:		
		try:
			new_instance.loadData()
		except Exception as e:
			print("Run.py 81", str(e))

def add_evidence(file=None):
	e_id = len(evidences.keys()) + 1
	new_evidence = Evidence.Evidence(e_id, file)
	evidences[new_evidence.file] = new_evidence
	new_ebox.addNode(new_evidence) 
	new_evidence.setTreeNode(new_ebox.newNode)
	sql = "INSERT INTO Evidence VALUES (?, ?)"	
	values = (new_evidence.file, new_evidence.size)
	insertRecord(sql, values)

