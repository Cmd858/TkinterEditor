import tkinter as tk
from tkinter import *
from SideBar import SideBar

def tempsetup():

    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0

    scrW = 500
    scrH = 400
    barW = 150

    type = None

    widgets = []
    widgetType = None

    window = Tk()


def main():
    global scrH, scrW, widgetType
    window['width'] = 500
    window['height'] = 400
    window.geometry(f'{window["width"]}x{window["height"]}')
    window.title('Tkinter Editor')
    window['bg'] = 'black'

    sidebar = SideBar(window)#, widgetType) # fixed to prevent warning
    sidebar.populateBar()
    setBinds(window)

    window.mainloop()


def setBinds(window):
    window.bind('<Button-1>', clickDrag)
    window.bind('<ButtonRelease-1>', clickDrag)


def clickDrag(event):
    global x1, x2, y1, y2, scrH, scrW, barW, widgetType
    etype = str(event.type)
    print(event.type)
    if etype == 'ButtonPress':
        x1 = event.x
        y1 = event.y
    elif etype == 'ButtonRelease':
        print('makingwidget')
        x2 = event.x
        y2 = event.y
        if 0 < x1 < scrW - barW and 0 < y1 < scrH and \
                0 < x2 < scrW - barW and 0 < y2 < scrH:
            placeWidget(widgetType, x1, y1, x2, y2)

def placeWidget(wigtype, x1, y1, x2, y2):
    global widgets, window
    wigtype = 'label'
    if wigtype is None:
        print(None)
        return None
    elif wigtype == 'label':
        print('label')
        widgets.append(Label(window))#, x=x1, y=y1, width=x2-x1, height=y2-y1))
        widgets[-1].pack('top')

#########################################################################


class WindowManager:
    def __init__(self):
        self.widgetType = None
        self.x1, self.x2, self.y1, self.y2 = 0, 0, 0, 0  # drag box coordinate references
        self.scrW = 500
        self.scrH = 400
        self.barW = 150
        self.window = Tk()
        self.window['width'] = 500
        self.window['height'] = 400
        self.window.geometry(f'{self.window["width"]}x{self.window["height"]}')
        self.window.title('Tkinter Editor')
        self.window['bg'] = 'black'
        self.widgets = []
        self.coords = []  # coords of widgets as ((x1, y1), (x2, y2))

        self.sidebar = SideBar(self)
        self.sidebar.populateBar()
        self.setBinds(self.window)

    def run(self):
        self.window.mainloop()

    def setBinds(self, window):
        window.bind('<Button-1>', self.clickDrag)
        window.bind('<ButtonRelease-1>', self.clickDrag)

    def clickDrag(self, event):
        #global x1, x2, y1, y2, scrH, scrW, barW, widgetType
        etype = str(event.type)
        print(event.type)
        if etype == 'ButtonPress':
            self.x1 = event.x
            self.y1 = event.y
        elif etype == 'ButtonRelease':
            print('makingwidget')
            self.x2 = event.x
            self.y2 = event.y
            if 0 < self.x1 < self.scrW - self.barW and 0 < self.y1 < self.scrH and \
                    0 < self.x2 < self.scrW - self.barW and 0 < self.y2 < self.scrH:  # double line bc long
                self.placeWidget(self.widgetType, self.x1, self.y1, self.x2, self.y2)

    def placeWidget(self, wigtype, x1, y1, x2, y2):
        #global widgets, window
        #wigtype = 'label'
        if wigtype is None:
            print(None)
            return None
        elif wigtype == 'label':
            #print('label')
            label_frame = tk.Frame(self.window, width=abs(x2-x1), height=abs(y2-y1))
            label_frame.pack_propagate(0)
            self.widgets.append((label_frame, Label(label_frame, text='label')))
            self.widgets[-1][1].pack() # make widgets with pixel lengths
            # , x=x1, y=y1, width=x2-x1, height=y2-y1))
            #Label().place()
            #print(self.widgets)

            self.widgets[-1][0].place(x=x1 if x2-x1 >= 0 else x2, y=y1 if y2-y1 >= 0 else y2)
            #print(self.widgets[-1].x, self.widgets[-1]['y'], self.widgets[-1]['width'], self.widgets[-1]['height'])
            print(dict(self.widgets[-1][0])['width'], dict(self.widgets[-1][0])['height'])
            ## think it defines size in chars and cols
            self.coords.append(((x1, y1), (x2, y2)))

#main()
win = WindowManager()
win.run()
