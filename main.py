import _tkinter
import tkinter as tk
from tkinter import *
from SideBar import SideBar
from EditorWindows import EditorWindow, PropertyWindow


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
        self.selectedWidget = None
        self.sidebar = SideBar(self)  # initiate sidebar
        self.sidebar.populateBar()  # populate sidebar
        self.setBinds(self.window)  # set window keybinds for event callbacks
        self.cursor = 'mouse'

    def run(self):
        self.window.mainloop()  # run main window event loop

    def setBinds(self, window):
        window.bind('<Button-1>', self.clickDrag)  # bind tkinter events to callback functions
        window.bind('<ButtonRelease-1>', self.clickDrag)
        window.bind('<Button-3>', self.editWidget)  # right click is button 3 for some reason

    def clickDrag(self, event):
        x, y = event.x_root - self.window.winfo_rootx(), event.y_root - self.window.winfo_rooty()
        #print(x, y, event.x, event.y)
        if 0 < x < self.scrW - self.barW and 0 < y < self.scrH:
            etype = str(event.type)  # get event type as string for comparison
            if etype == 'ButtonPress':
                self.x1 = event.x  # grab mousedown positions
                self.y1 = event.y
            elif etype == 'ButtonRelease':
                # print('makingwidget')  # stating the obvious
                self.x2 = event.x  # grab mouseup positions
                self.y2 = event.y
                if abs(self.x1 - self.x2) < 5 or abs(self.y1 - self.y2) < 5:
                    return  # prevent really small widgets from being created
                elif 0 < self.x1 < self.scrW - self.barW and 0 < self.y1 < self.scrH and \
                        0 < self.x2 < self.scrW - self.barW and 0 < self.y2 < self.scrH:  # double line bc long
                    self.placeWidget(self.widgetType, self.x1, self.y1, self.x2, self.y2)  # calls to place the widget

    def editWidget(self, event):
        # print(dir(event))
        x, y = event.x_root - self.window.winfo_rootx(), event.y_root - self.window.winfo_rooty()
        # ^ absolute value on screen - absolute value of main = mouse pos relative to main window bc it can't be easy
        for coords in self.coords:
            if (coords[0][0] >= x >= coords[1][0] or coords[0][0] <= x <= coords[1][0]) \
                    and (coords[0][1] >= y >= coords[1][1] or coords[0][1] <= y <= coords[1][1]):  # if x2 > x1 etc
                self.selectedWidget = self.widgets[self.coords.index(coords)]  # set the currently selected widget
                PropertyWindow(self.window, self, self.selectedWidget)  # open property editor window

    def placeWidget(self, wigtype, x1, y1, x2, y2):
        if wigtype is None:  # no type so do nothing
            print(None)  # remind you you're an idiot for not picking an option
            return None  # literally just returns, probs don't need a comment here
        label_frame = tk.Frame(self.window, width=abs(x2 - x1),
                               height=abs(y2 - y1))  # create frame with abs dimensions
        label_frame.pack_propagate(0)  # prevent widgets resizing frame
        if wigtype == 'label':
            self.widgets.append((label_frame, Label(label_frame,
                                                    text='label', width=int(abs(x2 - x1) / 5),
                                                    height=int(abs(y2 - y1)))))
            # ^ create references to label and frame with relative sizes based on font size and guessing
        elif wigtype == 'button':
            self.widgets.append((label_frame, Button(label_frame,
                                                     text='button', width=int(abs(x2 - x1) / 5),
                                                     height=int(abs(y2 - y1)))))
        self.widgets[-1][1].pack()  # make widgets with pixel lengths instead of chars and lines
        self.widgets[-1][0].place(x=x1 if x2 - x1 >= 0 else x2,
                                  y=y1 if y2 - y1 >= 0 else y2)  # allow for x1 > x1 etc.
        self.coords.append(((x1, y1), (x2, y2)))  # coords for reference later

    def newWindow(self):
        newWindow = EditorWindow(self.window, self, 'height')

    def returnEditor(self, key, value):
        print(key, value)
        #print(self.selectedWidget)
        try:
            print('changing')
            self.selectedWidget[1][key] = value  # [1] for widget out of (frame, widget) tuple  # change keyed value
            self.selectedWidget[0][key] = value
        except _tkinter.TclError as e:
            print(e)
            alert = Tk()
            alert.title('Error')
            Label(alert, text=e).pack()
            alert.mainloop()

    def returnProperties(self, value):
        #print(value)
        EditorWindow(self.window, self, value)


win = WindowManager()  # initiate class
win.run()  # run event loop

# TODO: if drawing on another label, it displaces the next label
