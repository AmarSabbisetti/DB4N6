
import sys
import os
from pathlib import Path
#statusbar
#GUI
import shutil

from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from tkinter import messagebox as mb
#from tqdm import tqdm
#own classes
from .sqlite_parser import SQLiteParser
from .WAL_parser import WALParser
from .journal_parser import JournalParser
from .visualizer import Visualizer
from .outjson import output_json

class GUI:
    gui_on = FALSE
    def __init__(self):
        #self.logger = logging.getLogger("parser.gui")
        self.sqlites = []
        self.sqlp = None
        self.wals = []
        self.walp = None
        self.journals = []
        self.journalp = None
        self.output = None
        self.format = 0

        #src_folder="/Users/amar/Desktop/SFT030"
        #out_folder="/Users/amar/Desktop/Output1"
        #for f in src_folder:
        self.top = Tk()
        self.top.geometry("500x500")
        self.top.title("DB4n6")
        # SELECTED FILE
        frame=Frame(self.top)
        frame.pack()
        bottomframe = Frame(self.top)
        bottomframe.pack(side=BOTTOM)
        btn1 = Button(frame, text="Database File", command=self.select_file)
        btn1.pack(side=LEFT)
        btn2 = Button(frame, text="Backup File", command=self.select_file)
        btn2.pack(side=LEFT)
        btn1 = Button(frame, text="WAL File", command=self.select_file)
        btn1.pack(side=LEFT)
        btn2 = Button(frame, text="Journal File", command=self.select_file)
        btn2.pack(side=LEFT)
        self.list = Listbox(self.top)
        self.list.config(width=80)
        self.list.pack(anchor=NW)
        # OUTPUT FOLDER
        self.output=os.path.abspath('/Users/amar/Desktop/DB3F')
        # OUTPUT
        file_button = Button(self.top, text="Start carving", command=self.process)
        file_button.pack()

        file_button = Button(self.top, text="Stop", command=self.top.destroy)
        file_button.pack()
        # self.sqlites.append('F:\\newOC\\MA\\SQLite-parser\\sqllite-parser\\db\\9main.db')
        # self.output = 'F:\\newOC\\MA\\SQLite-parser\\sqllite-parser\\result'

        self.top.mainloop()
        """if os.path.exists(os.path.abspath(src_folder)) and len(src_folder) > 0:
            for subdir, dirs, files in os.walk(os.path.abspath(src_folder)):
                for file in files:
                    filepath = subdir + os.sep + file
                    if filepath.endswith(".sqlite") or filepath.endswith(".db"):
                        self.sqlites.append(filepath)
                    elif filepath.endswith("-wal"):
                            self.wals.append(filepath)
                    elif filepath.endswith("-journal"):
                            self.journals.append(filepath)
"""
        """for f in args.filename:
            if (Path(os.path.abspath(f))).is_file():
                self.sqlites.append(os.path.abspath(f))

        for f in args.wal:
            if (Path(os.path.abspath(f))).is_file():
                self.wals.append(os.path.abspath(f))

        for f in args.journal:
            if (Path(os.path.abspath(f))).is_file():
                self.journals.append(os.path.abspath(f))
    
        if  (len(self.sqlites) <0):
            sys.exit("No files to parse")
    #or len(self.wals) > 0 or len(self.journals) > 0):


        if os.path.exists(os.path.abspath(out_folder)):
            self.output = os.path.abspath(out_folder)
        else:
            os.makedirs(os.path.abspath(out_folder))
            self.output = os.path.abspath(out_folder)
        
            #CSV = 0 | XML = 1 | JSON = 2
        if args.format== 'XML':
            self.format = 1
        elif args.format== 'JSON':
             self.format = 2

    def radio_select(self):
        self.format = self.var.get()
        #print(self.format)
"""

    def create_button(self, t="Select File"):
        btn2 = Button(self.top, text=t, command=self.select_file)
        btn2.pack(pady=20)

    def select_file(self):
        self.filename = askopenfilename()
        if os.path.abspath(self.filename).endswith(".sqlite") or os.path.abspath(self.filename).endswith(".db"):
            self.sqlites.append(os.path.abspath(self.filename))
        elif os.path.abspath(self.filename).endswith("-wal"):
            self.wals.append(os.path.abspath(self.filename))
        elif os.path.abspath(self.filename).endswith("-journal"):
            self.journals.append(os.path.abspath(self.filename))
        else: pass
        self.update_list()

    def select_out_file(self):
        filename = askdirectory()
        self.out1 = os.path.abspath(filename)
        #self.output = 'F:\\newOC\\MA\\SQLite-parser\\sqllite-parser\\result'
        self.output_text.config(text="OUTPUT FOLDER: " + self.out1)
        source_folder = self.output
        destination_folder = self.out1

        # fetch all files
        for file_name in os.listdir(source_folder):
            # construct full file path
            source = source_folder + file_name
            destination = destination_folder + file_name
            # copy only files
            if os.path.isfile(source):
                shutil.copy(source, destination)
        label1 = Label(self.top, text="succussefully Downloaded...", foreground="green3")
        label1.pack(pady=20,anchor=NW)



    def update_list(self):
        self.list.delete(0, END)
        for i in self.sqlites:
            self.list.insert(END, i)
        for i in self.wals:
            self.list.insert(END, i)
        for i in self.journals:
            self.list.insert(END, i)


    def process(self):
        self.start_processing_sqlite()
        self.start_processing_journal()
        self.start_processing_wal()
        label1 = Label(self.top, text="successfully carved...", foreground="green3")
        label1.pack(pady=20)
        self.fileyesorno()
        file_button = Button(self.top, text="View", command=self.top.destroy)
        file_button.pack()


    def fileyesorno(self):
        res = mb.askquestion('DB4n6',
                             'Do you really want carved files')

        if res == 'yes':
            file_button = Button(self.top, text="Output Folder", command=self.select_out_file)
            file_button.pack(anchor=NW)
            self.output_text = Label(self.top)
            self.output_text.pack(anchor=NW)


    def start_processing_sqlite(self):
        self.d = None
        if len(self.sqlites) > 0:
            print("Processing main files")
            self.sqlp = SQLiteParser()
            for i in self.sqlites:
                self.d = self.sqlp.parse(i, self.output, self.format)

    def start_processing_wal(self):
        if len(self.wals) > 0:
            self.walp = WALParser()

            for i in self.wals:
                if i[0:-4] in self.sqlites:
                    self.walp.parse(i, self.output, self.format, True)
                else:
                    self.walp.parse(i, self.output, self.format, False)

    def start_processing_journal(self):
        if len(self.journals) > 0:
            #tqdm.write("Processing journal files")
            self.sqlp = SQLiteParser()
            self.journalp = JournalParser()
            for i in self.journals:
                try:
                    if i[0:-8] in self.sqlites:
                        self.journalp.parse(i, self.output, self.format, self.sqlp.get_page_size(i[0:-8]))
                    else:
                        self.journalp.parse(i, self.output, self.format, 0)
                        #exit("No related sqlite file with this journal " + i)
                except ValueError:
                    print("No page size are available")
