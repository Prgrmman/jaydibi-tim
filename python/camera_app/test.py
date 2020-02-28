#!/usr/bin/python3

import tkinter as tk
import sys
import threading
import datetime
import imutils
from PIL import Image
from PIL import ImageTk
import cv2
from imutils.video import VideoStream
import time
import pdb

# Most of the code is stolen from https://www.pyimagesearch.com/2016/05/30/displaying-a-video-feed-with-opencv-and-tkinter/

# Globals
DiceTypes = {'d4', 'd6', 'd8', 'd10', 'd12', 'd20'}

class DiceApp:
    def __init__(self, app_name, vs):
        """ Constructor 
        Atributes:
            @app_name (string): name of the app
            @root (tkinter.Tk): root windows
            @vs (video stream): video stream
            @frame: most recently read frame from the camera
            @panel: tk image panel to display the frame
            @thread: the thread handling the video stream
            @stop_event: stop event for the thread
            @dice_choice (tkinter.StringVar) selected dice type
        """
        self.app_name = app_name
        self.root = tk.Tk()
        self.panel = None

        self.vs = vs
        self.frame = None
        self.thread = None
        self.stopEvent = None

        self.root.title(self.app_name)
        self.dice_choice = tk.StringVar(self.root)
        self.dice_choice.set('d4') # default dice value
        

        # Add a Frame
        main_frame = tk.Frame(self.root)
        self.root.columnconfigure(0, weight = 1)
        #main_frame.pack(pady = 100, padx = 100)
        for i in range(4):
            self.root.columnconfigure(i, weight=1)
            self.root.rowconfigure(i, weight = 1)

        # Make a drop down list for dice types
        # default choice is d4
        dice_menu = tk.OptionMenu(self.root, self.dice_choice, *DiceTypes)
        tk.Label(self.root, text='Select dice type').grid(row = 2, column = 1, sticky = 's')
        dice_menu.grid(row=3, column = 1, sticky = 's')
        def dice_menu_on_change(*args):
            print (self.dice_choice.get())
        self.dice_choice.trace('w', dice_menu_on_change)

        #add a button
        b = tk.Button(self.root, text="OK", command=self.take_pic)
        b.grid(row=4, column = 1, sticky = 's')

        # Setup clean up when the app is closed
        self.root.wm_protocol("WM_DELETE_WINDOW", self.on_close)

    def video_loop(self):
        try:
            while not self.stopEvent.is_set():
                self.frame = self.vs.read()
                self.frame = imutils.resize(self.frame, width=600)

                time.sleep(5)
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)

                #if the panel is None we need to initilize it.
                if self.panel is None:
                    self.panel = tk.Label(image=image)
                    self.panel.image = image
                    self.panel.grid(row = 0, column = 1, sticky = 'n')
                else:
                    self.panel.configure(image = image)
                    self.panel.image = image
        except RuntimeError as e:
            print("[INFO] caught a RuntimeError")

    def take_pic(self):
        print("take pic")

    def run(self):
        """ Run the app """
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.video_loop, args=())
        self.thread.start()
        self.root.mainloop()

    def on_close(self):
        self.stopEvent.set()
        self.vs.stop()
        self.root.quit()


def main(args):
    print("hi")

    print("[INFO] warming up camera...")
    vs = VideoStream(-1).start()
    time.sleep(2.0)
    app = DiceApp('Camera app', vs)
    app.run()
    # main window
    print("App closed?")



    # Add radio button

if __name__ == '__main__':
    main(sys.argv)
