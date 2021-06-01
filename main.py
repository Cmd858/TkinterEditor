import tkinter as tk
from tkinter import *
from SideBar import SideBar

class WindowManager:
    def __init__(self):
        self.widgetType = None
        self.x1, self.x2, self.y1, self.y2 = 0, 0, 0, 0  # drag box coordinate references
        self.scrW = 500
        self.scrH = 400  # might make these init params later for flexibility idk
        self.barW = 150  # width of sidebar
        self.window = Tk()  # initiate window
        self.window['width'] = self.scrW  # sets dimensions to set variables
        self.window['height'] = self.scrH
        self.window.geometry(f'{self.window["width"]}x{self.window["height"]}')  # set geometry
        self.window.title('Tkinter Editor')  # set title
        self.window['bg'] = 'black'  # set background colour
        self.widgets = []  # empty list for storing screen widgets
        self.coords = []  # coords of widgets as ((x1, y1), (x2, y2))

        self.sidebar = SideBar(self)  # initiate sidebar
        self.sidebar.populateBar()  # populate sidebar
        self.setBinds(self.window)  # set window keybinds for event callbacks

    def run(self):
        self.window.mainloop()  # run main window event loop

    def setBinds(self, window):
        window.bind('<Button-1>', self.clickDrag)  # bind tkinter events to callback functions
        window.bind('<ButtonRelease-1>', self.clickDrag)

    def clickDrag(self, event):
        #global x1, x2, y1, y2, scrH, scrW, barW, widgetType
        etype = str(event.type)  # get event type as string for comparison
        print(event.type)
        if etype == 'ButtonPress':
            self.x1 = event.x  # grab mousedown positions
            self.y1 = event.y
        elif etype == 'ButtonRelease':
            print('makingwidget')  # stating the obvious
            self.x2 = event.x  # grab mouseup positions
            self.y2 = event.y
            if 0 < self.x1 < self.scrW - self.barW and 0 < self.y1 < self.scrH and \
                    0 < self.x2 < self.scrW - self.barW and 0 < self.y2 < self.scrH:  # double line bc long
                self.placeWidget(self.widgetType, self.x1, self.y1, self.x2, self.y2)  # calls to place the widget

    def placeWidget(self, wigtype, x1, y1, x2, y2):
        if wigtype is None:  # no type so do nothing
            print(None)  # remind you you're an idiot for not picking an option
            return None  # literally just returns, probs don't need a comment here
        elif wigtype == 'label':
            label_frame = tk.Frame(self.window, width=abs(x2-x1), height=abs(y2-y1))  # create frame with abs dimensions
            label_frame.pack_propagate(0)  # prevent widgets resizing frame
            self.widgets.append((label_frame, Label(label_frame, text='label')))  # create references to label and frame
            self.widgets[-1][1].pack()  # make widgets with pixel lengths instead of chars and lines
            self.widgets[-1][0].place(x=x1 if x2-x1 >= 0 else x2, y=y1 if y2-y1 >= 0 else y2)  # allow for x1 > x1 etc.
            print(dict(self.widgets[-1][0])['width'], dict(self.widgets[-1][0])['height'])  # debug print
            self.coords.append(((x1, y1), (x2, y2)))  # coords for reference later

win = WindowManager()  # initiate class
win.run()  # run event loop
