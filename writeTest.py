from tkinter import *


class MainWindow:
    def __init__(self):
        self.window = Tk()
        self.window.title('Tkinter Editor')
        self.scrW = 500
        self.scrH = 400
        self.window['bg'] = 'black'
        self.window['width'] = self.scrW
        self.window['height'] = self.scrH
        self.window.geometry(f'{self.window["width"]}x{self.window["height"]}')
        self.frames = []  # stores frames that hold widgets
        self.widgets = []

    def appendWidgets(self):
        self.frames.append(Frame(self.window, bg="green", height="150", width="202"))
        self.frames[-1].place(x=102, y=45)
        self.frames[-1].pack_propagate(0)
        self.widgets.append(Label(self.frames[-1], bg="green", height="150", text="label", width="40"))
        self.widgets[-1].pack()

    def run(self):
        self.window.mainloop()


if __name__ == '__main__':
    root = MainWindow()
    root.appendWidgets()
    root.run()
