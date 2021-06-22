import _tkinter
import tkinter as tk
from tkinter import *
from Constructor import Constructor
from EditorWindows import EditorWindow, PropertyWindow
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
        self.selectedWidget = None
        self.selectedWidget2 = None  # used in linking widgets
        self.sidebar = SideBar(self)  # initiate sidebar
        self.sidebar.populateBar()  # populate sidebar
        self.setBinds(self.window)  # set window keybinds for event callbacks
        self.cursor = 'arrow'
        self.drawBox = None
        self.drawBoxCoords = (0, 0)
        self.mouseDown = False
        self.propertyWindow = None  # use one variable for property windows to prevent duplication
        self.hovered = None
        self.hoveredxy = (0, 0)
        self.hoveredindex = None
        self.dependencies = ['from tkinter import *']  # imports for writing file
        print(dict(Radiobutton()))

    def run(self):
        self.window.mainloop()  # run main window event loop

    def setBinds(self, window):
        window.bind('<Button-1>', self.clickDrag)  # bind tkinter events to callback functions
        window.bind('<ButtonRelease-1>', self.clickDrag)
        window.bind('<Button-3>', self.editWidget)  # right click is button 3 for some reason
        window.bind('<Motion>', self.drawMotion)

    def clickDrag(self, event):
        x, y = event.x_root - self.window.winfo_rootx(), event.y_root - self.window.winfo_rooty()
        etype = str(event.type)  # get event type as string for comparison
        if etype == 'ButtonPress':
            self.mouseDown = True
        elif etype == 'ButtonRelease':
            self.mouseDown = False
        if self.propertyWindow is not None:  # destroy property window if it exists
            self.propertyWindow.destroySelf()
        if self.cursor == 'arrow':
            if 0 < x < self.scrW - self.barW and 0 < y < self.scrH:
                if etype == 'ButtonPress':
                    self.x1 = event.x  # grab mousedown positions
                    self.y1 = event.y
                    if self.drawBox is not None:
                        self.drawBox.destroy()  # destroy drawbox if mouseup event didn't take care of it
                        self.drawBox = None
                    # ^ box to show where a widget will be drawn
                elif etype == 'ButtonRelease':
                    # print('makingwidget')  # stating the obvious
                    if self.drawBox is not None:
                        self.drawBox.destroy()
                        self.drawBox = None  # destroy and reset to stop calling motion events
                    self.x2 = event.x  # grab mouseup positions
                    self.y2 = event.y
                    if abs(self.x1 - self.x2) < 5 or abs(self.y1 - self.y2) < 5:
                        return  # prevent really small widgets from being created
                    elif 0 < self.x1 < self.scrW - self.barW and 0 < self.y1 < self.scrH and \
                            0 < self.x2 < self.scrW - self.barW and 0 < self.y2 < self.scrH:  # double line bc long
                        self.placeWidget(self.widgetType, self.x1, self.y1, self.x2, self.y2)  # place the widget
        elif self.cursor == 'fleur':  # the move cursor with weird name
            if etype == 'ButtonPress':
                try:
                    hovered = self.window.winfo_containing(event.x_root, event.y_root)  # get hovered widget
                    widgetindex = [i[1] for i in self.widgets].index(hovered)  # invalid target raises: s.hovered = None
                    widgetset = self.widgets[widgetindex]  # get index of widget w/ list
                    self.hoveredindex = widgetindex  # index used for replacing co-ords
                    self.hovered = widgetset[0]  # set hovered widget as frame not actual widget
                    self.hoveredxy = (event.x, event.y)  # set coords of x and y for relative positioning
                except ValueError:  # only move widgets that were placed by user
                    self.hovered = None  # set to none if no current moving object
                    self.hoveredxy = (0, 0)
            elif etype == 'ButtonRelease':
                if self.hovered is not None:
                    x1, y1 = self.hovered.winfo_x(), self.hovered.winfo_y()
                    x2, y2 = x1 + self.hovered.winfo_width(), y1 + self.hovered.winfo_height()
                    self.coords[self.hoveredindex] = ((x1, y1), (x2, y2))
        elif self.cursor == 'X_cursor':  # the move cursor with weird name
            if etype == 'ButtonPress':
                try:
                    hovered = self.window.winfo_containing(event.x_root, event.y_root)  # get hovered widget
                    widgetindex = [i[1] for i in self.widgets].index(hovered)  # invalid target raises: s.hovered = None
                    self.widgets[widgetindex][0].destroy()  # destroy widgets
                    self.widgets[widgetindex][0].destroy()
                    self.widgets.pop(widgetindex)
                except ValueError:  # only move widgets that were placed by user
                    self.hovered = None  # set to none if no current moving object
                    self.hoveredxy = (0, 0)
        elif self.cursor == 'sizing':
            if etype == 'ButtonPress':
                if self.selectedWidget is None:
                    self.selectedWidget = self.window.winfo_containing(event.x_root, event.y_root)
                else:
                    self.selectedWidget2 = self.window.winfo_containing(event.x_root, event.y_root)
                    oldframeindex = [i[1] for i in self.widgets].index(self.selectedWidget)
                    oldframe = self.widgets[oldframeindex]
                    framex, framey = oldframe.winfo_rootx()  # this isn't going to work
                    # TODO: create widget groups to have master frames with containing frames and then the widgets
                    # TODO: create radiobutton functionality using the join function etc
                    # hmm do i want two frames?
                    # maybe replace with align to replicate size and pack into position , with extra settings panel to
                    # config currently selected cursor, possibly in new window
                    # TODO: review above and decide what to do

                    # do stuff here like delete 2nd frame and extend first to pack together, tho might not be viable
                    # bc of sizing difference so just pack the two frames together maybe idk
        elif self.cursor == 'cross_reverse':
            if etype == 'ButtonPress':
                self.selectedWidget = self.window.winfo_containing(event.x_root, event.y_root)
                print(self.selectedWidget)
            elif etype == 'ButtonRelease':
                newWidget = self.selectedWidget.__class__()
                for key in self.selectedWidget.configure():
                    newWidget.configure({key: self.selectedWidget.cget(key)})
                self.widgets.append(newWidget)
                x1, y1 = event.x_root - self.window.winfo_rootx(), event.y_root - self.window.winfo_rooty()
                x2, y2 = x1 + self.selectedWidget['width'], y1 + self.selectedWidget['height']
                self.coords.append(((x1, y1), (x2, y2)))
                newWidget.place(x1, y1)
                # TODO: make this actually work

    def editWidget(self, event):
        x, y = event.x_root - self.window.winfo_rootx(), event.y_root - self.window.winfo_rooty()
        # ^ absolute value on screen - absolute value of main = mouse pos relative to main window bc it can't be easy
        for coords in self.coords:
            if (coords[0][0] >= x >= coords[1][0] or coords[0][0] <= x <= coords[1][0]) \
                    and (coords[0][1] >= y >= coords[1][1] or coords[0][1] <= y <= coords[1][1]):  # if x2 > x1 etc
                self.selectedWidget = self.widgets[self.coords.index(coords)]  # set the currently selected widget
                if self.propertyWindow is not None:
                    self.propertyWindow.destroySelf()
                self.propertyWindow = PropertyWindow(self.window, self,
                                                     self.selectedWidget)  # open property editor window

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
        elif wigtype == 'checkbox':
            self.widgets.append((label_frame, Checkbutton(label_frame,
                                                          text='checkbox', width=int(abs(x2 - x1) / 5),
                                                          height=int(abs(y2 - y1)))))
        elif wigtype == 'radio':
            self.widgets.append((label_frame, Radiobutton(label_frame,
                                                          text='radioButton', width=int(abs(x2 - x1) / 5),
                                                          height=int(abs(y2 - y1)))))
        elif wigtype == 'entry':
            self.widgets.append((label_frame, Entry(label_frame,
                                                    text='entry', width=int(abs(x2 - x1) / 5))))
        elif wigtype == 'text':
            self.widgets.append((label_frame, Text(label_frame,
                                                   width=int(abs(x2 - x1) / 5),
                                                   height=int(abs(y2 - y1)))))
        self.widgets[-1][1].pack()  # make widgets with pixel lengths instead of chars and lines
        self.widgets[-1][0].place(x=x1 if x2 - x1 >= 0 else x2,
                                  y=y1 if y2 - y1 >= 0 else y2)  # allow for x1 > x2 etc.
        self.coords.append(((x1, y1), (x2, y2)))  # co-ords for reference later

    def returnEditor(self, key, value):
        print(key, value)
        print(dir(self.selectedWidget[1]))
        print(self.selectedWidget[1].__class__)
        try:
            print('changing')
            self.selectedWidget[1][key] = value  # [1] for widget out of (frame, widget) tuple  # change keyed value
        except _tkinter.TclError as e:  # create an alert that shows why what you put can't be done
            print(e)
            alert = Tk()
            alert.title('Error')
            Label(alert, text=e).pack()
            alert.mainloop()
        try:
            self.selectedWidget[0][key] = value
        except _tkinter.TclError:  # don't need to print exception for this method
            pass

    def returnProperties(self, value):
        # print(value)
        EditorWindow(self.window, self, value)

    def drawMotion(self, event):
        x, y = event.x_root - self.window.winfo_rootx(), event.y_root - self.window.winfo_rooty()
        if self.cursor == 'arrow':
            if 0 < x < self.scrW - self.barW and 0 < y < self.scrH:
                if self.drawBox is None and self.mouseDown == True:
                    ax, ay = event.x_root - self.window.winfo_rootx(), event.y_root - self.window.winfo_rooty()
                    self.drawBox = Frame(bd=2, bg='black', width=0, height=0, relief='raised')
                    self.drawBox.place(x=ax, y=ay)
                    self.drawBoxCoords = (ax, ay)
                if self.drawBox is not None and self.mouseDown == True:
                    dx = self.drawBoxCoords[0]
                    dy = self.drawBoxCoords[1]  # definitive co-ords, where the mouse started
                    mx = event.x
                    my = event.y  # current mouse co-ords
                    sx = dx  # cover for .place() re-requiring x coord in y check, idk why tho
                    if mx > dx:  # positive x
                        self.drawBox['width'] = mx - dx  # dist between mx and dx is width
                    else:
                        sx = mx
                        self.drawBox.place(x=sx, y=dy)
                        self.drawBox['width'] = dx - mx  # same as ^ but with negatives so reversed equation
                    if my > dy:  # positive y
                        self.drawBox['height'] = my - dy
                    else:
                        self.drawBox.place(x=sx, y=my)  # final place if necessary
                        self.drawBox['height'] = dy - my
        elif self.cursor == 'fleur' and self.mouseDown is True:
            x, y = event.x_root - self.window.winfo_rootx(), event.y_root - self.window.winfo_rooty()
            if self.hovered is not None:
                self.hovered.place(x=x - self.hoveredxy[0], y=y - self.hoveredxy[1])  # move smoothly

    def writeCode(self):
        print('writing')
        constructor = Constructor(self.window, self)
        constructor.build()

    def addDependency(self, text):
        if text in self.dependencies:
            del self.dependencies[self.dependencies.index(text)]
        else:
            self.dependencies.append(text)


win = WindowManager()  # initiate class
win.run()  # run event loop

# TODO: if drawing on another label, it displaces the next label
