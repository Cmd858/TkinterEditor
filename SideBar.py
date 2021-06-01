from tkinter import *

class SideBar:
    def __init__(self, parent):
        self.parent = parent  # get parent class for function references
        self.window = parent.window  # get parent window for widgets
        self.winW = self.window['width']  # get dimensions vars
        self.winH = self.window['height']
        print(self.winW, self.winH)
        self.widgets = []  # widgets list
        self.sidebar = Label(self.window)  # create sidebar area, should probs use frame but ah well
        self.barwidth = 150  # width of bar, hardcoded for some reason #TODO: make this reference main
        self.sidebar.place(x=self.winW - self.barwidth, y=0, width=self.barwidth, height=self.winH)  # place sidebar
        self.sidebar['bg'] = 'grey'  # set background colour and relief of sidebar
        self.sidebar['relief'] = 'ridge'

    def create_widget(self, text, convtype):
        button = Button(self.sidebar, text=text, command=lambda: self.setType(convtype))  # make command button
        button.pack(side='top', anchor='nw')  # pack the widget to north-west (top-left)

    def setType(self, convtype):
        self.parent.widgetType = convtype  # change type of widget being deployed

    def populateBar(self):
        self.create_widget('Label', 'label')  # populate the sidebar with function widgets
        self.create_widget('Label2', 'label')
