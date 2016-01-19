#!/usr/bin/python
# Python GUI module using Tkinter.

import os
import sys
import threading
import functools

import Tkinter
import ttk
import Tkconstants
import tkFileDialog
import tkMessageBox

class TkOpenFileDialog(Tkinter.Frame):
    def __init__(self, root, label_txt = 'Input file:', button_txt = 'Choose File', defaultextension = '.txt', filetypes = [('text files', '.txt')], initialdir = os.getcwd()):
        '''
        Sets up the widgets for this FileDialog and FileDialog options.
        '''
        
        Tkinter.Frame.__init__(self, root)
        # options for buttons
        common_opt = {'fill': Tkconstants.BOTH, 'padx': 40, 'pady': 5}
        
        # define widgets
        self.label = Tkinter.Label(root, text=label_txt)
        self.label.pack(common_opt)
        self.entry = Tkinter.Entry(root, bd =5)
        self.entry.pack(common_opt)
        self.button = Tkinter.Button(self, text=button_txt, command=self.askopenfilename).pack(**common_opt)

        # define options for opening or saving a file
        self.file_opt = options = {}
        options['defaultextension'] = defaultextension
        options['filetypes'] = filetypes
        options['initialdir'] = initialdir
        options['parent'] = root
        options['title'] = 'File Selection'

    def askopenfilename(self):
        '''        
        Dialog filename and the filename is set in the entry widget.
        '''

        # get filename
        filename = tkFileDialog.askopenfilename(**self.file_opt)

        # open file on your own
        if filename:      
            self.entry.delete(0, len(self.entry.get()))
            self.entry.insert(0, filename)
            
class SynchronizingProgressFrame(Tkinter.Frame):
    def __init__(self, root, max_progress_value, exit_function):
        '''
        Sets up options and widgets for this frame.
        '''
        Tkinter.Frame.__init__(self, root)
        self.max_value = max_progress_value
        
        common_opt = {'fill': Tkconstants.BOTH, 'padx': 40, 'pady': 5}
        
        # define widgets
        self.label_progress_global = Tkinter.Label(self, text= "Global Progress:")
        self.label_progress_global.pack(common_opt)
        
        self.progress_global = ttk.Progressbar(self, orient='horizontal', length=400, mode='determinate', maximum = self.max_value)
        self.progress_global.pack(common_opt)
        
        self.label_progress_current = Tkinter.Label(self, text= "Current Task Progress:")
        self.label_progress_current.pack(common_opt)
        
        self.progress_current = ttk.Progressbar(self, orient='horizontal', length=400, mode='determinate', maximum = self.max_value)
        self.progress_current.pack(common_opt)
        
        self.label_logs = Tkinter.Label(self, text= "Logs:")
        self.label_logs.pack()
        
        self.text_frame = Tkinter.Frame(self)
        self.text_frame.pack({'fill': Tkconstants.BOTH, 'padx': 0, 'pady': 5})
        
        self.scrollbar = Tkinter.Scrollbar(self.text_frame)
        self.scrollbar.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
        
        self.text_logs = Tkinter.Text(self.text_frame, yscrollcommand = self.scrollbar.set)
        self.text_logs.pack({'fill': Tkconstants.BOTH})
        self.text_logs.config(state=Tkinter.DISABLED)
        
        self.scrollbar.config(command=self.text_logs.yview)
        
        self.btn_cancel = Tkinter.Button(self, text ="Cancel", command = exit_function, bg = '#ffc2b3')
        self.btn_cancel.pack({'fill': Tkconstants.BOTH, 'padx': 100, 'pady': 25})
    
    def GetGlobalProgressBarValue(self):
        return self.progress_global["value"]
    
    def SetGlobalProgressBarToValue(self, value):        
        if value >= 0 and value <= self.max_value:
            self.progress_global["value"] = value
    
    def GetCurrentProgressBarValue(self):
        return self.progress_current["value"]
    
    def SetCurrentProgressBarToValue(self, value):        
        if value >= 0 and value <= self.max_value:
            self.progress_current["value"] = value
    
    def InsertToLogs(self, log_msg):        
        self.text_logs.config(state=Tkinter.NORMAL)
        self.text_logs.insert(Tkinter.END, log_msg)
        self.text_logs.config(state=Tkinter.DISABLED)
    
class GuiManager():
    def __init__(self, syncBtnCallBack):
    
        # used for progress bars
        self.NUM_GLOBAL_TASKS = 7.0
        self.NUM_GLOBAL_TASKS_FINISHED = 0.0
        self.NUM_CURRENT_TASKS = 10.0
        self.NUM_CURRENT_TASKS_FINISHED = 0.0
        
        # creating root window
        self.root = Tkinter.Tk()
    
        # Properties
        self.root.geometry("400x300")
        self.root.title("SubSync - Automatic Subtitle Synchronizer")
        self.root.resizable(0,0)
                
        self.root.protocol("WM_DELETE_WINDOW", self.ExitProgram)
        
        # Code to add widgets will go here
        self.select_frame = Tkinter.Frame(self.root)
        self.video_file_dialog = TkOpenFileDialog(
            self.select_frame, 
            label_txt = "Video input file:", 
            defaultextension = '.avi', 
            filetypes = [('MPEG-4','.mp4'), ('Audio Video Interleave', '.avi')])
        self.video_file_dialog.pack()
        self.subtitle_file_dialog = TkOpenFileDialog(
            self.select_frame, 
            label_txt = "Subtitle input file:", 
            defaultextension = '.srt',
            filetypes = [('SubRip text file', '.srt')])

        self.subtitle_file_dialog.pack()
        self.btn_syn = Tkinter.Button(self.select_frame, text ="Synchronize subtitle", command = syncBtnCallBack, bg = '#ffc2b3')
        self.btn_syn.pack({'fill': Tkconstants.BOTH, 'padx': 100, 'pady': 25})
        self.select_frame.pack()
        self.GenerateMenuBar()
    
    def ExitProgram(self):
        self.root.destroy()
        sys.exit()
    
    def RunSubSyncGuiMainLoop(self):
        # Kick off the main loop
        self.root.mainloop()
        
    def DisplayPromptMsg(self, window_name = "Prompt", message_txt = "Message"):
        tkMessageBox.showinfo(window_name, message_txt)
    
    def LogProgress(self, msg):
        self.progress_lock.acquire()        
        self.progress_logs.append(msg)
        self.progress_lock.release()
    
    def IncrimentGlobalProgressBar(self):
        self.progress_lock.acquire()
        self.NUM_GLOBAL_TASKS_FINISHED += 1.0
        self.global_progress_value = int((self.max_progress_value * self.NUM_GLOBAL_TASKS_FINISHED / self.NUM_GLOBAL_TASKS))    
        self.progress_lock.release()
    
    def ResetCurrentProgressBarValue(self, NUM_CURRENT_TASKS, task_name):
        self.progress_lock.acquire()
        self.NUM_CURRENT_TASKS = float(NUM_CURRENT_TASKS)
        self.NUM_CURRENT_TASKS_FINISHED = 0.0
        self.current_progress_value = 0
        self.progress_frame.label_progress_current['text'] = "Current Task Progress: " + task_name
        self.progress_lock.release()
    
    def IncrimentCurrentProgressBar(self):
        self.progress_lock.acquire()
        self.NUM_CURRENT_TASKS_FINISHED += 1.0
        self.current_progress_value = int((self.max_progress_value * self.NUM_CURRENT_TASKS_FINISHED / self.NUM_CURRENT_TASKS))    
        self.progress_lock.release()
    
    def InitSynchronizingProgressFrame(self):
        self.root.geometry("700x610")
        self.root.resizable(0, 0)
        self.select_frame.destroy()
        
        # set shared variables
        self.global_progress_value = 0
        self.current_progress_value = 0
        self.max_progress_value = 1000
        self.progress_logs = []
        self.progress_lock = threading.Lock()
        
        # saved logs
        self.log_file_text = u""
        
        # create Frame to keep track of the progress of synchronization        
        self.progress_frame = SynchronizingProgressFrame(self.root, self.max_progress_value, self.ExitProgram)
        self.progress_frame.pack()
        
    def UpdateSynchronizingProgressFrame(self):
        self.progress_lock.acquire()
                
        for log in self.progress_logs:
            self.progress_frame.InsertToLogs(log)
            self.log_file_text += log
        self.progress_logs = []        
        self.progress_frame.SetGlobalProgressBarToValue(self.global_progress_value)
        self.progress_frame.SetCurrentProgressBarToValue(self.current_progress_value)
        
        if self.progress_frame.GetGlobalProgressBarValue() < self.progress_frame.max_value:
            self.progress_lock.release()
            self.progress_frame.after(200, self.UpdateSynchronizingProgressFrame)
        else:
            self.progress_frame.btn_cancel["text"] = "Close"            
            self.DisplayPromptMsg(
                window_name = "SubSync", 
                message_txt = "Successful synchronization.\nOutput file written")
            print self.progress_logs
            print self.log_file_text
            # TODO should exit?
            self.progress_lock.release()
        
    def GenerateMenuBar(self):
        def donothing():
            self.DisplayPromptMsg(message_txt = "Under Implementation")
            
        def ShowAbout():
            self.about_window = Tkinter.Toplevel()
            self.about_window.geometry("400x400")
            self.about_window.transient(self.root)
            self.about_window.grab_set()
            self.root.wait_window(self.about_window)
            
        menubar = Tkinter.Menu(self.root)
        
        filemenu = Tkinter.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New Synchronization", command=donothing)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.quit)
        
        menubar.add_cascade(label="File", menu=filemenu)
        
        editmenu = Tkinter.Menu(menubar, tearoff=0)        
        editmenu.add_command(label="Language Options", command=donothing)
        editmenu.add_command(label="Parameter Tuning", command=donothing)
        
        menubar.add_cascade(label="Configuration", menu=editmenu)
        
        helpmenu = Tkinter.Menu(menubar, tearoff=0)        
        helpmenu.add_command(label="User Manual", command=donothing)
        helpmenu.add_command(label="About SubSync", command=ShowAbout)
        
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.root.config(menu=menubar)