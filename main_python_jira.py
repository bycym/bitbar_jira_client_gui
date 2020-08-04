######################################################################
# Author : Aaron Benkoczy
# Date : 2018.01.04.
######################################################################

import fnmatch
import os
import re
import xml.etree.ElementTree as ET
import sys
from tkinter import font
from tkinter import ttk
import tkinter as tk
import bitbar_jira_client.jira_noti as jira_noti

import time
import threading
import queue
import webbrowser       
import datetime

class GuiPart:
  def __init__(self, master, queue, endCommand):
    self.queue = queue
    
    # Set up the GUI        
    master.protocol("WM_DELETE_WINDOW", endCommand)
    master.title("Jira issues GUI")
    master.geometry('10x10+0+0')
    self.dFont=font.Font(family="Arial", size=14)

    # Menu elements
    self.menu = tk.Menu(master)
    master.config(menu=self.menu)
    self.fileMenu = tk.Menu(self.menu)
    self.menu.add_cascade(label="File", menu=self.fileMenu)
    # self.fileMenu.add_command(label="Refresh", command=self.RefreshMenu)
    master.geometry('600x600+0+0')

    # init tree
    self._tree = ttk.Treeview(master)
    self._tree["columns"]=("one","two")
    self._tree.heading("#0", text="Issues")
    self._tree.heading("one", text="Link")
    self._tree.heading("two", text="Place")
    self._tree.column("#0", minwidth=600, stretch=True)        
    self._tree.column("one", minwidth=60, stretch=False)
    self._tree.column("two", minwidth=45, stretch=False)

    # event listener double click
    self._tree.bind("<Double-1>", self.OnDoubleClick)
    #ttk.Style().configure('Treeview', rowheight=50)
    
    # scroll bar to root
    self.yscrollbar=tk.Scrollbar(master, orient=tk.VERTICAL, command=self._tree.yview)
    self.yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    self.xscrollbar=tk.Scrollbar(master, orient=tk.HORIZONTAL, command=self._tree.xview)
    self.xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)

    self._tree.configure(yscrollcommand=self.yscrollbar.set, xscrollcommand=self.xscrollbar.set)

    self._tree.pack(side=tk.LEFT, fill=tk.BOTH, expand = tk.YES)
    
    content = jira_noti.getParsedIssues()
    self.RefreshTree(content)
    # self.GetData(content)
    # master.after(15000, self.RefreshTree)
    # master.mainloop();


  def processIncoming(self):
    """Handle all messages currently in the queue, if any."""
    while self.queue.qsize(  ):
      try:
        issues = self.queue.get(0)
        self.RefreshTree(issues)
      except queue.Empty:
        pass

    logFile = ""

  # refresh menu
  # def RefreshMenu(self):
  #   self.RefreshTree()

  # double click on a node
  def OnDoubleClick(self, event):
    selected_item = self._tree.focus()
    value = self._tree.item(selected_item, "values")
    if (len(value) > 0):
      print ("===============================================================")
      print (value)
      if re.search("http", value[0]):
        url = value[0]
        print(url)
        webbrowser.open_new(url)
    print ("===============================================================")

  def RefreshTree(self,content):
    self._tree.delete(*self._tree.get_children())
    self.GetData(content)

  def GetData(self, content):
    contentList = content.split("\n")
    # tagTypes = set()
    # the first root tag what shows "All Warnings"
    # tagMap = {"[root]": 0}
    # tagMap["[root]"] = self._tree.insert("", 0, "[root]", text="[All Warnings: 0]")
    # tagIndex = 1

    tagMap = {}
    # tagMap["[root]"] = self._tree.insert("", 0, "[root]", text="[All Warnings: 0]")

    tagIndex = 0

    # iterate throu the splitted elements
    for i, line in enumerate(contentList):
      
      if (re.search("href=", line)):
        issue_text = line[0:line.find("|")]
        link = line[line.find("=")+1:len(line)]
        tagMap[tagIndex] = self._tree.insert("", tagIndex, i, text=issue_text,
          values=(link, "placeColumn"));

      else:
        issue_text = line
        link = "--"
        tagMap[tagIndex] = self._tree.insert("", tagIndex, i, text=issue_text,
          values=(link, "placeColumn"));

      tagIndex = tagIndex + 1



class ThreadedClient:
  def __init__(self, master):
    self.master = master

    # Create the queue
    self.queue = queue.Queue(  )

    # Set up the GUI part
    self.gui = GuiPart(master, self.queue, self.endApplication)

    # Set up the thread to do asynchronous I/O
    # More threads can also be created and used, if necessary
    self.running = 1
    self.thread1 = threading.Thread(target=self.workerThread1)
    self.thread1.start(  )

    # Start the periodic call in the GUI to check if the queue contains
    # anything
    self.periodicCall(  )

  def periodicCall(self):
    self.gui.processIncoming(  )
    if not self.running:
      import sys
      sys.exit(1)
      self.thread1.exit()

    self.master.after(10000, self.periodicCall)

  def workerThread1(self):
    while self.running:
      print(datetime.datetime.now())
      issues = jira_noti.getParsedIssues()
      self.queue.put(issues)

  def endApplication(self):
    self.running = 0
    import sys
    sys.exit(1)

root = tk.Tk()
# master=tk.Tk()
client = ThreadedClient(root)
root.mainloop(  )