import os
import hashlib
from tqdm import tqdm
import random
import json
import datetime
from colorama import *
import binascii
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory

class ReportGenerator:
    def __init__(self):
        self.my_path = ""
        self.grpr={}
        self.grrow=0
        self.offset = 99

    def generateReport(self,curr_page, data, alldata, schema=["No schema found"]) -> object:
        if data is None:
            return
        #print(curr_page)
        global offset
        self.all=alldata
        if curr_page in self.grpr:
            self.grrow=self.grpr[curr_page]
        else:
            self.grrow=0
        x=[]
        if data:
            out = ""
            for datatype in schema:
                out += str(datatype) + ","
            out += "\n"
            output=[]

            for frame in data:
                io=[]
                if isinstance(frame, list):
                    for y in frame:
                        if self.is_text(y[0]):
                            try:
                                io.append(str(y[1].decode('utf-8')))
                                out += str(y[1].decode('utf-8')) + ","
                            except UnicodeDecodeError:
                                out +=str(y[1]) + ","
                                io.append(str(y[1]))
                                continue
                        else:
                            out += str(y[1]) + ","
                            io.append(str(y[1]))
                out += "\n"
                output.append(io)
                record = {
                    'allocated': True,
                    'values': io,
                    'row_id': self.grrow,
                    'offset': self.offset+1
                }
                self.offset+=1
                x.append(record)
                self.grrow += 1

            out += "++++++++++++++++++++++++++++\n"
            #print(out)

            self.grpr[curr_page] = self.grrow
            #print(curr_page,self.grrow,x)
            #self.print_hash(path + "/" + filename + '.log')
        for i in range(len(self.all)):

            if self.all[i]['page_id']==int(curr_page):
                #print(alldata[i]['page_id'])
                if 'records' not in self.all[i]:
                    self.all[i]['records'] = x
                else:
                    self.all[i]['records']+=x

    def jsonconvert(self,out,filename,page_size):
        #print(self.all)
        out=open(out+'/'+filename+'.json','w')
        header = {"carving_time": str(datetime.datetime.now()),
                  "dbms": "sqlite",
                  "foresnic_tool": "DB4N6",
                  "evidence_file": filename,
                  "page_size": page_size}
        out1=json.dumps(header)
        out.write("%s\n"% out1)
        for i in self.all:
            out2=json.dumps(i)
            out.write("%s%s" % (out2, "\n"))

    """def jsondump(self):
        print(self.all)
        header={"carving_time": str(datetime.datetime.now()), "dbms": "sqlite", "foresnic_tool": None, "evidence_file": "filename.img", "page_size": 34782}
        try:
            #j1=json.loads(header)
            with open('/Users/amar/Desktop/DF-Toolkit/Images/sqlite.json', "a") as f:
                json.dump(header, f)
        except UnicodeEncodeError:
            print("can not write the record because of unicode errors")

        for i in self.all:
            try:
                #j2=json.load(i)
                with open('/Users/amar/Desktop/DF-Toolkit/Images/sqlite.json', "a") as f:
                    json.dump(i,f)
            except UnicodeEncodeError:
                print("can not write the record because of unicode errors")
        #print(alldata)
    """"""def generate_schema_report(self, path, filename, data, csv):
        if data is None:
            return

        if not os.path.exists(path):
            os.makedirs(path)
        print(data)

        out = ""
        with open(path + "/" + filename + '.log', "a") as f:
            for key, value in data.items():
                # out += str(key) + ", "
                if isinstance(value, list):
                    for y in value:
                        out += str(y) + ", "
                out += "\n"
            out += "++++++++++++++++++++++++++++\n"

            f.write(out)
"""
        #self.print_hash(path + "/" + filename + '.log')

    def generate_freeblock_report(self, path, filename, freeblocks):
        if freeblocks is None:
            return

        if not os.path.exists(path):
            os.makedirs(path)

        with open(path+'.json', "a") as f:
            for solutions in freeblocks:
                for s in solutions:
                    if isinstance(s[0], list):
                        f.write(str(s) + ",")
                    else:
                        if self.is_text(s[0]):
                            f.write(str(s[1].decode('utf-8')) + ",")
                        else:
                            f.write(str(s[1]) + ",")
                f.write("\n" + "###################" + "\n")

        #self.print_hash(path + "/" + filename + '.log')

    def is_text(self, tester):
        return tester == 'TEXT'

    """def print_hash(self, filename):
        with open(filename, "rb") as f:
            d = f.read()
            tqdm.write("sha-256: " + filename +  => ' + str(hashlib.sha256(d).hexdigest()))"""