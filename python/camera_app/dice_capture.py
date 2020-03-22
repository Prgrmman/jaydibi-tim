#!/usr/bin/python3

import tkinter as tk
from tkinter import messagebox
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
import os

# Most of the code is stolen from https://www.pyimagesearch.com/2016/05/30/displaying-a-video-feed-with-opencv-and-tkinter/

# Globals
DiceTypes = {'d4', 'd6', 'd8', 'd10', 'd12', 'd20'}
DEFAULT_PATH = '/tmp/dice_photos'

def get_dice_max(dice_key):
    ''' Return the max int value of a dice key (e.g d4 is 4) '''
    return int(dice_key[1:])

class DiceApp:
    def __init__(self, app_name, vs):
        """ Constructor 
        Atributes:
            @app_name (string): name of the app
            @root (tkinter.Tk): root windows
            @vs (video stream): video stream
            @frame: most recently read frame from the camera
            @panel: tk image panel to display the frame
            @dice_entry: tk text entry field for dice value
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
        self.folder_path = DEFAULT_PATH

        # Count the number of photos taken of each dice at a given value
        self.dice_counts = {}
        for dice in DiceTypes:
            value_dict = {}
            for value in range(1, get_dice_max(dice) + 1):
                value_dict[value] = 0
            self.dice_counts[dice] = value_dict

        self.root.title(self.app_name)
        self.dice_choice = tk.StringVar(self.root)
        self.dice_choice.set('d4') # default dice value
        

        # Add a Frame
        main_frame = tk.Frame(self.root)
        self.root.columnconfigure(0, weight = 1)
        #main_frame.pack(pady = 100, padx = 100)
        for i in range(6):
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

        # Add a label and a dice value entry field.
        tk.Label(self.root, text="Dice value").grid(row=4, column = 1)
        self.dice_entry = tk.Entry(self.root, text="1")
        self.dice_entry.grid(row=5, column = 1)

        #add a button to take the picture
        capure_button = tk.Button(self.root, text="Capture", command=self.take_pic)
        capure_button.grid(row=6, column = 1, sticky = 's')

        # Setup clean up when the app is closed
        self.root.wm_protocol("WM_DELETE_WINDOW", self.on_close)

    def init_pic_directory(self):
        """ Create the tree folder structure if it doesn't already exist """
        def mkdir_p(path):
            if not os.path.exists(path):
                os.makedirs(path)

        my_path = self.folder_path
        mkdir_p(my_path)

        for dice in DiceTypes:
            dice_path = os.path.join(my_path, dice)
            mkdir_p(dice_path)
            for value in range(1, get_dice_max(dice) + 1):
                value_path = os.path.join(dice_path, str(value))
                mkdir_p(value_path)


    def video_loop(self):
        ''' Internal method designed to update the image preview '''
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
        ''' Capture and store the current picture in the preview '''

        my_path = self.folder_path
        dice_choice = self.dice_choice.get()
        dice_value = self.dice_entry.get()
        try:
            dice_value = int(dice_value)
        except ValueError:
            messagebox.showerror(title="Dice value error", message="please enter the number shown on the dice")
            return

        if not (0 < dice_value and dice_value <= get_dice_max(dice_choice)):
            messagebox.showerror(title="Dice value error", message="Dice value is out or range for dice type")
            return

        dice_dir = os.path.join(my_path, dice_choice)
        dice_dir = os.path.join(dice_dir, str(dice_value))


        # looks at an already populated directory of dice images
        # and finds the next file name. Do this only once for each
        # dice directory
        if self.dice_counts[dice_choice][dice_value] == 0:
            files = next(os.walk(dice_dir))[2]
            self.dice_counts[dice_choice][dice_value] = len(files)

        file_name = str(self.dice_counts[dice_choice][dice_value]) + '.jpg'
        file_name = os.path.join(dice_dir, file_name)
        cv2.imwrite(file_name, self.frame.copy())
        print("saved {}".format(file_name))
        # TODO could have error checking here to see if I wrote the file
        self.dice_counts[dice_choice][dice_value] += 1

        

    def run(self):
        """ Run the app """
        self.init_pic_directory()
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


if __name__ == '__main__':
    main(sys.argv)
