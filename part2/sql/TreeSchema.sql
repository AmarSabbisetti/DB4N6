CREATE TABLE Evidence(
	E_FileName VARCHAR(100),
	E_Size NUMBER,
	CONSTRAINT EvidencePK PRIMARY KEY (E_FileName)
);
CREATE TABLE Instance(
	I_EvidenceFile VARCHAR(100),
	I_CarvedDataFile VARCHAR(100),
	I_DBMS VARCHAR(25),
	I_PageSize NUMBER,
	I_Pages NUMBER,
	I_Storage NUMBER,
	I_CarvingTime VARCHAR(40),
	I_ForensicTool VARCHAR(40),	
	CONSTRAINT InstancePK PRIMARY KEY (I_CarvedDataFile),
	CONSTRAINT FileFK FOREIGN KEY (I_EvidenceFile) 
		REFERENCES Evidence(E_FileName)
);
CREATE TABLE Objects(
	O_ID VARCHAR(25),
	O_Type VARCHAR(25),
	O_Pages NUMBER,
	O_ColumnTypes VARCHAR(100),
	O_DBMS VARCHAR(25),
	O_InstFile VARCHAR(100),	
	CONSTRAINT ObjectsPK PRIMARY KEY (O_ID, O_InstFile),
	CONSTRAINT DBMS_FK FOREIGN KEY (O_InstFile) 
		REFERENCES INSTANCE(I_CarvedDataFile)
);
CREATE TABLE Page(
	P_Offset NUMBER,
	P_PageID NUMBER,
	P_Records NUMBER,
	P_ObjectID VARCHAR(25),
	P_DBMS VARCHAR(25),
	P_InstFile VARCHAR(100),
	CONSTRAINT PagePK PRIMARY KEY (P_Offset, P_ObjectID, P_InstFile),
	CONSTRAINT ObjectFK FOREIGN KEY (P_ObjectID)
		REFERENCES Objects(O_ID)
	CONSTRAINT DBMS_FK2 FOREIGN KEY (P_InstFile) 
		REFERENCES INSTANCE(I_CarvedDataFile)

);
CREATE TABLE Records(
	R_Offset NUMBER,
	R_PageOffset NUMBER,
	R_RowID NUMBER,
	R_Allocated NUMBER,
	R_Values VARCHAR(200),
	R_PageID NUMBER,
	R_ObjectID VARCHAR(25),
	CONSTRAINT RecordPK PRIMARY KEY (R_PageOffset, R_Offset, R_PageID),
	CONSTRAINT PageFK FOREIGN KEY (R_PageID)
		REFERENCES Page(P_Offset)
);