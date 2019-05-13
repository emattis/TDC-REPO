# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 10:50:03 2019

@author: cocapodanno
"""
import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
import csv
import numpy
import math 

out_title="Mission_Film-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".avi"

cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(out_title,fourcc, 20.0, (640,480))

max_buffer=50

class App:
   def __init__(self, window, window_title, video_source=0):
         self.window = window
         self.window.title(window_title)
         self.video_source = video_source
         self.pause = True
         self.refPt = []
         self.frame = 1
         self.frame_list = []
         self.sub_frame = 1
         self.clean_frame=1
         cropping = False
         self.bypass_pause=False
         self.framelist_idx=max_buffer-1

         self.dist_to_targ=0
         self.ground_distance=0
         self.targ_lat=0
         self.targ_long=0  
         
         self.target_size=4 #four foot target in meters
         self.focal= 256  #figure this out



      

         rows = 0
         while rows <10:
            window.columnconfigure(rows,weight = 1)
            window.rowconfigure(rows,weight = 1)
            rows +=1

         #open video source
         self.cam = MyVideoCapture(video_source)
         self.vid = MyVideoCapture(video_source)
         #create canvas

           
         self.canvas = tkinter.Canvas(window, width=self.vid.width, height=self.vid.height)

         self.canvas.grid(column=0, row=0, columnspan=7)
         self.canvas.bind("<ButtonPress-1>", self.click_and_crop1)
         self.canvas.bind("<ButtonRelease-1>", self.click_and_crop2)

         #button that lets user pause the video
         self.btn_pause=tkinter.Button(window, text="Pause", width=10, command=self.stop)
         self.btn_pause.grid(column=1, row=3)
         #button that lets user play the video
         self.btn_play=tkinter.Button(window, text="Play", width=10, command=self.play)
         self.btn_play.grid(column=2, row=3)
         self.btn_play=tkinter.Button(window, text="Step_F", width=10, command=self.stepF)
         self.btn_play.grid(column=3, row=3)
         self.btn_play=tkinter.Button(window, text="Step_B", width=10, command=self.stepB)
         self.btn_play.grid(column=0, row=3)
         self.btn_play=tkinter.Button(window, text="Clean", width=10, command=self.clean)
         self.btn_play.grid(column=4, row=3)
         # Button that lets the user take a snapshot
         self.btn_snapshot=tkinter.Button(window, text="Snapshot", width=10, command=self.snapshot)
         self.btn_snapshot.grid(column=5, row=3)
         
         self.latitude_label=tkinter.Label(window, text="Latitude")
         self.latitude_label.grid(column=0, row=4)
         self.latitude=tkinter.Entry(window)
         self.latitude.grid(column=1, row=4)

         self.longitude_label=tkinter.Label(window, text="Longitude")
         self.longitude_label.grid(column=2, row=4)
         self.longitude=tkinter.Entry(window)
         self.longitude.grid(column=3, row=4)

         self.altitude_label=tkinter.Label(window, text="Altitude")
         self.altitude_label.grid(column=4, row=4)
         self.altitude=tkinter.Entry(window)
         self.altitude.grid(column=5, row=4)

         self.compass_label=tkinter.Label(window, text="Compass Heading")
         self.compass_label.grid(column=6, row=4)
         self.compass=tkinter.Entry(window)
         self.compass.grid(column=7, row=4)


         #where we enter the information to complete the algorithm
         self.detail=tkinter.Frame(window,borderwidth=5, relief="sunken")
         self.detail.grid(column=8, row=0)
         self.mission_name_Label = tkinter.Label(self.detail, text='Mission Name')
         self.mission_name_Label.grid(row=0, column=9)
         self.mission_name = tkinter.Entry(self.detail)
         self.mission_name.insert(10,"Mission-" + time.strftime("%d-%m-%Y-%H-%M-%S"))

         self.mission_name.grid(row=1, column=9)   
         self.lsum = tkinter.Label(self.detail, text = 'AV->Targ:')
         self.lsum.grid(row=5, column=0, pady=4)
         self.threat_name_Label = tkinter.Label(self.detail, text='Threat Name')
         self.threat_name_Label.grid(row=4, column=1)
         self.threat_name = tkinter.Entry(self.detail)
         self.threat_name.insert(10,"New_Threat")
         self.threat_name.grid(row=5, column=1)
         self.threat_desc_Label = tkinter.Label(self.detail, text='Threat Description')

         self.threat_desc_Label.grid(row=4, column=2)
         self.threat_desc = tkinter.Entry(self.detail)
         self.threat_desc.insert(10,"New_Threat")
         self.threat_desc.grid(row=5, column=2)                                       

         self.btn_save = tkinter.Button(self.detail, text="Calculate", width=10, command=self.save)
         self.btn_save.config(state="disabled")
         self.btn_save.grid(row=4, column=3)
         self.btn_clear = tkinter.Button(self.detail, text="Clear", width=10, command=self.clear)
         self.btn_clear.grid(row=5, column=3)

         self.snap_canvas = tkinter.Canvas(self.detail, width=self.vid.width, height=self.vid.height)
         self.snap_canvas.grid(column=0, row=0, columnspan=3, rowspan=2)
         #where we display the list of threats for a given mission
         self.threats=tkinter.Frame(window, height=100)
         self.threats.grid(column=8, row=2)


         self.threat_label = tkinter.Label(self.threats, text = "Threat List")
         self.threat_label.grid(column=0, row=0, pady=4)
         
                
         #auto call until stopped
         self.delay = 15

         self.update()
         self.window.mainloop()

   def update(self):
      ret, frame = cap.read()
      out.write(frame)
      if (self.pause == False) or (self.bypass_pause):
         if(self.framelist_idx == max_buffer-1):
            #get a frame from source
            self.bypass_pause=False
            ret, self.frame = self.vid.get_frame()
            #line marking center of feed
            cv2.line(self.frame,(int(self.vid.width/2),0),(int(self.vid.width/2),int(self.vid.height)),(0,0,0),1)
            if ret:
               self.frame_list.append(self.frame.copy())
               self.clean_frame=self.frame.copy()
               self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.frame))
               self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
         else:
            self.stepF()
      else:
         time.sleep(.02)
      if len(self.frame_list)>max_buffer:
         self.frame_list.pop(0)

      self.window.after(self.delay, self.update)

   def snapshot(self, sub_frame_ctrl=0):
     # Get a frame from the video source
     if sub_frame_ctrl == 1:
       sub_frame = self.clean_frame[self.refPt[0][1]:self.refPt[1][1], self.refPt[0][0]:self.refPt[1][0]]
       imgScale = 600/sub_frame.shape[1]
       sub_frame = cv2.resize(sub_frame,(int(sub_frame.shape[1]*imgScale),int(sub_frame.shape[0]*imgScale)))
     else:
       sub_frame=self.frame
     self.photo2 = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(sub_frame))
     self.snap_canvas.create_image(0, 0, image = self.photo2, anchor = tkinter.NW)
     cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(sub_frame, cv2.COLOR_RGB2BGR))


   def stop(self):
      #print("pause")
      self.pause = True
   def play(self):
      self.pause = False
      #print("play")
   def stepF(self):
      if self.framelist_idx != max_buffer-1:
         self.framelist_idx+=1
         self.frame=self.frame_list[self.framelist_idx].copy()
         self.clean_frame=self.frame.copy()
         cv2.line(self.frame,(int(self.vid.width/2),0),(int(self.vid.width/2),int(self.vid.height)),(0,0,0),1)
         self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.frame))
         self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
      else:
         self.bypass_pause=True
   def stepB(self):
      if self.framelist_idx > 0:
         self.framelist_idx-=1
         self.frame=self.frame_list[self.framelist_idx].copy()
         self.clean_frame=self.frame.copy()
         cv2.line(self.frame,(int(self.vid.width/2),0),(int(self.vid.width/2),int(self.vid.height)),(0,0,0),1)
         self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.frame))
         self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

      
   def clean(self):
      self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.clean_frame))
      self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
      
      
   def click_and_crop1(self, event):
      # grab references to the global variables
      self.frame=self.clean_frame.copy()
      self.pause = True
      self.refPt.clear()
      self.refPt = [(event.x, event.y)]
      cropping = True

   def click_and_crop2(self, event):
      # grab references to the global variables
      self.refPt.append((event.x, event.y))
      cropping = False
      cv2.rectangle(self.frame, self.refPt[0], self.refPt[1], (0, 255, 0), 2)
      cv2.line(self.frame,(int(self.vid.width/2),0),(int(self.vid.width/2),int(self.vid.height)),(0,0,0),1)
      self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.frame))
      self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
      self.snapshot(1)
      self.dist_to_targ = str(self.target_size*self.focal/(self.refPt[1][1]-self.refPt[0][1]))
      self.lsum["text"] = "AV->Targ: " + self.dist_to_targ
      print(self.refPt[1][1]-self.refPt[0][1])
      self.btn_save.config(state="normal")

   def save(self):
      file_name=self.mission_name.get()
      self.ground_distance=math.sqrt(pow(float(self.dist_to_targ),2)-pow(float(self.altitude.get()),2))
      compass=math.radians(float(self.compass.get()))
      lat_mask=1
      long_mask=1
      if compass>90 and compass<=180:
         long_mask=-1
      elif compass>180 and compass<=270:
         long_mask=-1
         lat_mask=-1
      elif compass>270 and compass<360:
         lat_mask=-1
      self.targ_lat=float(self.latitude.get())+((lat_mask*float(self.ground_distance)*math.sin(float(compass)))/364000)
      self.targ_long=float(self.longitude.get())+((long_mask*float(self.ground_distance)*math.cos(float(compass)))/288200)
      with open(file_name+".csv", 'a+') as file_object:
         file_object = csv.writer(file_object, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
         file_object.writerow([self.threat_name.get(), self.threat_desc.get(), self.targ_lat,self.targ_long ])

      self.clear()
      self.loadFile()

   def clear(self):
      self.threat_name.delete(0,'end')
      self.threat_desc.delete(0, 'end')
      
   def loadFile(self):
      file_name=self.mission_name.get()
      if file_name != "":
         with open(file_name+".csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            r=1
            for col in csv_reader:
               c=0
               for row in col:
                  label = tkinter.Label(self.threats, text = row, relief = tkinter.RIDGE)
                  label.grid(row=r, column =c)
                  c += 1
               r += 1
   
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
         cap.release()
         out.release()
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

App(tkinter.Tk(), "R2D2",out_title)

