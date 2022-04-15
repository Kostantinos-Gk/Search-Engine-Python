# -*- coding: utf-8 -*-
"""
Title : Search Engine, Information Retrieval LAB

Created on Tue Jan 4 23:14:27 2022

@author: Konstantinos Gkousaris
"""

import spacy
from rank_bm25 import BM25Okapi
from tqdm import tqdm
import time
import pandas as pd
import nltk
from tkinter import *
import os.path
import sys
import datetime 
from tkinter.filedialog import askdirectory

# --------------------------Functions-------------------------------------- #
#nlp = spacy.load("en_core_web_sm")

# returns a nltk tokensize form of the input string
def transform_to_nltk(text):
    return nltk.word_tokenize(text)

# ------------------------GUI Classes-------------------------------------- #
class MySearchEngineWindow:
    
    def __init__(self, win):
        # load files components
        self.inputpath = Label(win, text="Input File Path:")
        self.load_btn = Button(win, text='Load', command=self.loadFilesBtn)
        self.browse_btn = Button(win, text='Browse', command=self.browseDirectoryBtn)
        self.pathfile_field = Entry(win, text="", width=60)
        self.clear_btn = Button(win, text='Clear', command=self.clearWidgetBtn)
        
        
        # Loading Results
        self.loadfile_results_title = Label(win, text = "Loading Results :")
        self.loadfile_results = Label(win, text = "")
        
        self.inputpath.place(x =10, y = 20)
        self.pathfile_field .place(x =150, y = 20)
        self.browse_btn.place(x =650, y = 20)
        self.load_btn.place(x =720, y = 20)
        self.loadfile_results_title.place(x =10, y = 70)
        self.loadfile_results.place(x =150, y = 70)
        self.clear_btn.place(x = 780, y = 20)
        
        # Query 
        self.query = Label(win, text="Query:")
        self.search_btn = Button(win, text='Search',command=self.SearchBtn)
        self.query_field = Entry(win, text="", width=60)   
        self.query.place(x =10, y = 130)
        self.query_field.place(x =150, y = 130)
        self.search_btn.place(x =650, y = 130)
        
        # Algorithm option
        self.algorithm = Label(win, text="Choose Algorithm:")
        self.v0=IntVar()
        self.v0.set(1)
        self.r1=Radiobutton(window, text="BM25", variable=self.v0, value=1)
        self.r2=Radiobutton(window, text="PageRank", variable=self.v0, value=2)
        self.r1.place(x=300,y=180)
        self.r2.place(x=380, y=180)
        self.algorithm.place(x =10, y = 180)
        
        
        # Search Results 
        self.results = Label(win, text="Search Results:")
        self.results.place(x =10, y = 230)
        # To DO Scroll Bar
        
        self.result_textbox = Text(win, width=80, height=20, yscrollcommand=True , xscrollcommand=False ,padx= 2, pady=2 )
        self.result_textbox.place(x= 150, y=230)

      
        # variables
        self.cnt = 0
        self.flist = []
        self.list_of_docs = []
        self.normalization_docs = []
        self.load_flag = False
        
        
 # ------------------------------------------------------------------------ #       
    # Clear Text Widgets
    def clearWidgetBtn(self):
        self.pathfile_field.delete(0, 'end')
        self.loadfile_results.configure(text = "")
        self.query_field.delete(0, 'end')
        self.result_textbox.delete(1.0, 'end')
        
        
# ------------------------------------------------------------------------ #
    # Browse Button listener, print in Textfield the string of the path
    def browseDirectoryBtn(self):
        filename = askdirectory()
        self.pathfile_field.insert(END,filename)

# ------------------------------------------------------------------------ #
    # Load files from a specific directory, also normalize and tokenize the 
    # loaded txt files.
    def loadFilesBtn(self):
        if self.pathfile_field.get() == "":
            self.loadfile_results.configure(text = "Broswe a file First")
            print("Broswe a file First")
            self.load_flag = False
        else:    
            path=self.pathfile_field.get()
            print(path)
            self.load_flag = True
            
            if os.path.isdir(path):
                self.files=os.listdir(path)
                for i in self.files:
                   if i.endswith('.txt'):
                       file=open(path + "\\" + i , encoding="utf8")
                       self.flist.append(path + "\\" +  i)
                       self.cnt = self.cnt + 1
                       document_text=file.read()
                       # normalization and tokenization
                       # dummy way, but i need next both
                       self.normalization_docs.append(document_text.lower())
                       self.list_of_docs.append(transform_to_nltk(document_text.lower()))
                       file.close()
                #Insert Load Results       
                self.loadfile_results.configure(text = f"Number of files : {self.cnt}")
                        
                self.result_textbox.insert(END, f"UPLOAD FILES :\n")
                for i in self.flist:
                   self.result_textbox.insert(END,f"{i}\n")       
                           
            else:
                self.loadfile_results.configure(text = "Loading again")
                print("Load False")
    
            
# ------------------------------------------------------------------------ #
    # Search Button, in this fuction take place all the search functionality 
    # Starts with indexing, ranking and searching. Also creates messages to 
    # user and create a Log.txt file that user can extract info.
 
    def SearchBtn(self):
        if not self.load_flag:
            self.loadfile_results.configure(text = "Broswe a file First")
        else:
            if self.v0.get() == 1:
                # Indexing of documents
                bm25 = BM25Okapi(self.list_of_docs)
                
                if self.query_field.get() == "":
                    self.result_textbox.delete(1.0,'end')
                    self.result_textbox.insert(END,"Add a query First")  
                else:    
                    query = self.query_field.get()        
                    t0 = time.time()
                    # we also need to tokenize our query, and apply the same 
                    # preprocessing steps we did to the documents in order to have 
                    # an apples-to-apples comparison
                    tokenized_query = query.lower().split(" ")
                
                    # Ranking of documents
                    found_flag = False
                    cnt = 0
                    # getting the document scores
                    numberofViews = bm25.get_scores(tokenized_query)
                
                    # check inside the list if query exists in loaded docs
                    # if not, program inform the user
                    for k in numberofViews:
                        if k!= 0:
                            cnt = cnt + 1
                            found_flag = True
                    print(numberofViews)
                    print(found_flag)
                    
                    # retrieve the best two documents, because of the small amount 
                    # of uploaded documents 
                    results = bm25.get_top_n(tokenized_query,self.normalization_docs,n=2)        
                    t1 = time.time()
                    
                    # add date fuctionality for statistics, use usually for logs
                    current_date = datetime.datetime.now()
                
                    # Print Rankings 
                    self.result_textbox.delete(1.0,'end')
                    if not found_flag:
                        self.result_textbox.insert(END,f"Date : {current_date}\n")
                        self.result_textbox.insert(END,f"Query : {tokenized_query}\n")
                        self.result_textbox.insert(END,"No results for this search.\n")
                        self.result_textbox.insert(END,f"Searching time : {round(t1-t0,5)}sec.\n")
                        self.result_textbox.insert(END,f"----------------------------------------\n")
                        
                        # add search results to log file, for further invstigation
                        log_file = open("Logs.txt","a")
                        log_file.write(f"Date : {current_date}\n")
                        log_file.write(f"Query : {tokenized_query}\n")
                        log_file.write("No results for this search.\n")
                        log_file.write(f"Searching time : {round(t1-t0,5)}sec.\n")
                        log_file.write(f"---------------------------------------------------\n")
                        log_file.close()
                        
                        
                    else:    
                        self.result_textbox.insert(END,f"Date : {current_date}\n")
                        self.result_textbox.insert(END,f"Query : {tokenized_query}\n")
                        self.result_textbox.insert(END,"Find in searching.\n")
                        self.result_textbox.insert(END,f"Query find in {cnt} documents.\n")
                        for i,item in enumerate(numberofViews):     
                            if item != 0:
                                self.result_textbox.insert(END,f"Score  Doc[{i+1}] :{round(item,4)} \n")
                                
                        self.result_textbox.insert(END,f"Searching time : {round(t1-t0,5)}sec.\n")
                        self.result_textbox.insert(END,f"----------------------------------------\n")
                        
                         # add search results to log file, for further invstigation
                        log_file = open("Logs.txt","a")
                        log_file.write(f"Date : {current_date}\n")
                        log_file.write(f"Query : {tokenized_query}\n")
                        log_file.write("Find in searching.\n")
                        log_file.write(f"Query find in {cnt} documents.\n")
                        for i,item in enumerate(numberofViews):     
                            if item != 0:
                                log_file.write(f"Score  Doc[{i+1}] :{round(item,4)} \n")
                        log_file.write(f"Searching time : {round(t1-t0,5)}sec.\n")
                        log_file.write(f"---------------------------------------------------\n")
                        log_file.close()
                        
                        # Print the results from searching in Results Text Box
                        for i in results:
                            self.result_textbox.insert(END,f"{i}")
            else:    
                self.result_textbox.delete(1.0,'end')
                self.result_textbox.insert(END,"PageRang is not Available yet")  
                
    
            
    
# -------------------Start User Interfase------------------------------------#
    
window = Tk()
mywi = MySearchEngineWindow(window)


# main window
window.title('Search Engine')
window.geometry("1000x750+10+20")
window.resizable(False,False)
window.mainloop()
