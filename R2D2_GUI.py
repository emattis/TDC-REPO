#!/usr/bin/env python
import tkinter as tk

class VideoControls(tk.Frame):
    
    def __init__(self):
        super().__init__()
        self.loadVideo()
        self.loadButtons()
        
    def loadVideo(self):
        frame = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        frame.pack(fill=tk.BOTH, expand=True)
        #TODO Add video here
        
        
    def loadButtons(self):    
       frame = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
       frame.pack(fill=tk.BOTH, expand=True)

       self.pack(fill=tk.BOTH, expand=True)
       def save():
           print("Saving")
       
       def draw():
           print("Drawing")
       
       def goToBeginning():
           print("Begin")
       def backFiveSeconds():
           print("Reverse 5 seconds")
       def pauseVideo():
           print("Pause")
       def playVideo():
           print("Play")
       def forwardFiveSeconds():
           print("Forward 5 Seconds")
       def goToCurrent():
           print("Playing Current Time")
        
        
       begin = tk.Button(self,
                           text="<<",
                           command=goToBeginning)
       begin.pack(side=tk.LEFT,padx=10,ipadx=5)
       back = tk.Button(self,
                          text="<",
                          command=backFiveSeconds)
       back.pack(side=tk.LEFT,padx=10,ipadx=5)
       pause = tk.Button(self,
                          text="||",
                          command=pauseVideo)
       pause.pack(side=tk.LEFT,padx=10,ipadx=5)
       play = tk.Button(self,
                          text="Play",
                          command=playVideo)
       play.pack(side=tk.LEFT,padx=10,ipadx=5)
       forward = tk.Button(self,
                          text=">",
                          command=forwardFiveSeconds)
       forward.pack(side=tk.LEFT,padx=10,ipadx=5)
       current = tk.Button(self,
                          text=">>",
                          command=goToCurrent)
       current.pack(side=tk.LEFT,padx=10,ipadx=5)
       draw = tk.Button(self,
                          text="Draw",
                          command=draw)
       draw.pack(side=tk.LEFT,padx=10,ipadx=5)
       button = tk.Button(self, 
                          text="Quit", 
                          command=quit)
       button.pack(side=tk.LEFT, padx=10,ipadx=5)

#class Threats:
    
    #TODO change to for loop when threats are stored
    #tk.Label(text="Name",relief=tk.RIDGE, width=15).grid(row=0, column=0)
    #tk.Entry("Threat1", relief=tk.RIDGE, width=15).grid(row=0, column = 1)


root = tk.Tk()
root.geometry("500x200+300+300")
app= VideoControls()
root.mainloop()