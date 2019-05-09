# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 10:50:03 2019

@author: cocapodanno
"""
import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time

from imutils import paths
import numpy as np
import imutils

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

    # coutour image from snapshot image


    def find_marker(frame):
        # convert the image to grayscale, blur it, and detect edges
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(gray, 35, 125)

        # find the contours in the edged image and keep the largest one;
        # we'll assume that this is our piece of paper in the image
        cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        c = max(cnts, key=cv2.contourArea)

        # compute the bounding box of the of the paper region and return it
        return cv2.minAreaRect(c)

    def distance_to_camera(knownWidth, focalLength, perWidth):
        # compute and return the distance from the maker to the camera
        return (knownWidth * focalLength) / perWidth

    # initialize the known distance from the camera to the object, which
    # in this case is 24 inches
    KNOWN_DISTANCE = 24.0

    # initialize the known object width, which in this case, the piece of
    # paper is 12 inches wide
    KNOWN_WIDTH = 11.0

    # load the furst image that contains an object that is KNOWN TO BE 2 feet
    # from our camera, then find the paper marker in the image, and initialize
    # the focal length
    image = cv2.imread("images/2ft.png")
    marker = find_marker(image)
    focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH

    # loop over the images
    for imagePath in sorted(paths.list_images("images")):
        # load the image, find the marker in the image, then compute the
        # distance to the marker from the camera
        image = cv2.imread(imagePath)
        marker = find_marker(image)
        inches = distance_to_camera(KNOWN_WIDTH, focalLength, marker[1][0])

        # draw a bounding box around the image and display it
        box = cv2.cv.BoxPoints(marker) if imutils.is_cv2() else cv2.boxPoints(marker)
        box = np.int0(box)
        cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
        cv2.putText(image, "%.2fft" % (inches / 12),
                    (image.shape[1] - 200, image.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
                    2.0, (0, 255, 0), 3)
        cv2.imshow("image", image)
        cv2.waitKey(0)
        
 # Create a window and pass it to the Application object
 #this is where we call the video file
App(tkinter.Tk(), "R2D2", "puppy.mov")

