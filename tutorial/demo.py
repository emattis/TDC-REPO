# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 10:50:03 2019

@author: cocapodanno
"""
import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time

class App:
   def __init__(self, window, window_title, video_source=0):
         self.window = window
         self.window.title(window_title)
         self.video_source = video_source
         self.pause = False
         #open video source
         self.vid = MyVideoCapture(video_source)

         #create canvas
         self.canvas = tkinter.Canvas(window, width = self.vid.width/1.25, height=self.vid.height/1.25)
         self.canvas.grid(column=0, row=0, columnspan=3, rowspan=2)

         #button that lets user pause the video
         self.btn_pause=tkinter.Button(window, text="Pause", width=15, command=self.pause)
         self.btn_pause.grid(column=0, row=3)
         # Button that lets the user take a snapshot
         self.btn_snapshot=tkinter.Button(window, text="Snapshot", width=15, command=self.snapshot)
         self.btn_snapshot.grid(column=1, row=3)
         #where we enter the information to complete the algorithm
         self.detail=tkinter.Frame(window,borderwidth=5, relief="sunken", width=500, height=300)
         self.detail.grid(column=4, row=0)
         #where we display the list of threats for a given mission
         self.threats=tkinter.Frame(window, width=500, height=300)
         self.threats.grid(column=4, row=3)
         #auto call until stopped
         self.delay = 15
         self.update()


         self.window.mainloop()

   def update(self):
      #get a frame from source
      ret, frame = self.vid.get_frame()

      if ret:
         if self.pause == False:
            
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

      self.window.after(self.delay, self.update)

   def snapshot(self):
     # Get a frame from the video source
     ret, frame = self.vid.get_frame()
     if ret:
        cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
   def pause(self):
      self.pause = true
class MyVideoCapture:
    def __init__(self, video_source=0):
      #open the video source
      self.vid = cv2.VideoCapture(video_source)
      if not self.vid.isOpened():
         raise ValueError("Unable to open video", video_source)

      #get video source width and height
      self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
      self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

   #release video source when destroyed
    def __del__(self):
      if self.vid.isOpened():
         self.vid.release()
         
      

    def get_frame(self):
      if self.vid.isOpened():
         ret, frame = self.vid.read()
         if ret:
            #return success and convert
            return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
         else:
            return (ret, None)
      else:
         return (ret, None)
      
 # Create a window and pass it to the Application object
 #this is where we call the video file
App(tkinter.Tk(), "R2D2", "puppy.mov")
