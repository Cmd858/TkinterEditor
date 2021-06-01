import tkinter as tk
from tkinter import *
#from main import widgetType

#wigtype = widgetType

class SideBar:
    def __init__(self, parent):
        self.parent = parent
        self.window = parent.window
        self.winW = self.window['width']
        self.winH = self.window['height']
        print(self.winW, self.winH)
        self.widgets = []
        self.sidebar = Label(self.window)
        self.barwidth = 150
        self.sidebar.place(x=self.winW - self.barwidth, y=0, width=self.barwidth, height=self.winH)
        self.sidebar['bg'] = 'grey'
        self.sidebar['relief'] = 'ridge'

    def create_widget(self, text, convtype):
        button = Button(self.sidebar, text=text, command=lambda: self.setType(convtype))
        button.pack(side='top', anchor='nw')

    def setType(self, convtype):
        #global wigtype
        self.parent.widgetType = convtype
        #self.wigtype = convtype  # func for setting type from widgets

    def populateBar(self):
        self.create_widget('Label', 'label')
        self.create_widget('Label2', 'label')
