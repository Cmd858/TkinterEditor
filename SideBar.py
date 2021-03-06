from tkinter import *
from EditorWindows import EntryWindow

class SideBar:
    def __init__(self, parent):
        self.parent = parent  # get parent class for function references
        self.window = parent.window  # get parent window for widgets
        self.winW = self.window['width']  # get dimensions vars
        self.winH = self.window['height']
        self.widgets = []  # widgets list
        self.sidebar = Label(self.window)  # create sidebar area, should probs use frame but ah well
        self.barwidth = 150  # width of bar, hardcoded for some reason #TODO: make this reference main
        self.sidebar.place(x=self.winW - self.barwidth, y=0, width=self.barwidth, height=self.winH)  # place sidebar
        #self.sidebar.pack(side='right', anchor='ne')
        self.sidebar['bg'] = 'grey'  # set background colour and relief of sidebar
        self.sidebar['relief'] = 'ridge'

    def create_widget(self, btype, text, convtype):
        if btype == 'widget':
            button = Button(self.sidebar, text=text, command=lambda: self.setType(convtype))  # make command button
            button.pack(side='top', anchor='nw')  # pack the widget to north-west (top-left)
        elif btype == 'cursor':
            button = Button(self.sidebar, text=text, command=lambda: self.setCursor(convtype))  # make command button
            button.pack(side='bottom', anchor='sw')
        elif btype == 'write':
            button = Button(self.sidebar, text=text, command=lambda: self.parent.writeCode())  # make command button
            button.pack(side='bottom', anchor='se')
        elif btype == 'dependency':
            button = Button(self.sidebar, text=text, command=lambda: EntryWindow(self.window,
                                                                                 self.parent,
                                                                                 self.parent.addDependency,
                                                                                 'Add or remove dependency'))
            button.pack(side='bottom', anchor='ne')

    def setType(self, convtype):
        self.parent.widgetType = convtype  # change type of widget being deployed

    def setCursor(self, cursor):
        self.parent.window['cursor'] = cursor
        self.parent.cursor = cursor
        #  Cursors: https://www.tutorialspoint.com/python/tk_cursors.htm

    def populateBar(self):
        self.create_widget('widget', 'Label', 'label')  # populate the sidebar with function widgets
        self.create_widget('widget', 'Button', 'button')
        self.create_widget('widget', 'Checkbox', 'checkbox')
        self.create_widget('widget', 'Radio', 'radio')
        self.create_widget('widget', 'Entry', 'entry')
        self.create_widget('widget', 'Text', 'text')

        #self.create_widget('cursor', 'spray', 'spraycan')   #
        #self.create_widget('cursor', 'dotbox', 'dotbox')
        self.create_widget('cursor', 'clone', 'cross_reverse')
        self.create_widget('cursor', 'join', 'sizing')
        self.create_widget('cursor', 'delete', 'X_cursor')
        self.create_widget('cursor', 'move', 'fleur')  # no current plans for commented cursors, pls help, not limited
        #self.create_widget('cursor', 'cross', 'cross')  # to these cursors
        #self.create_widget('cursor', 'watch', 'watch')
        self.create_widget('cursor', 'draw', 'arrow')

        self.create_widget('write', 'write', 'arrow')

        self.create_widget('dependency', 'module', 'arrow')
