from tkinter import *
import tkinter.filedialog

class MainWindow:
    def __init__(self):
        self.window = Tk()
        self.window.title('Tkinter Editor')
        self.scrW = 350
        self.scrH = 400
        self.window['bg'] = 'black'
        self.window['width'] = self.scrW
        self.window['height'] = self.scrH
        self.window.geometry(f'{self.window["width"]}x{self.window["height"]}')
        self.frames = []  # stores frames that hold widgets
        self.widgets = []

    def appendWidgets(self):
        self.frames.append(Frame(self.window, height="132", width="169"))
        self.frames[-1].place(x=96, y=85)
        self.frames[-1].pack_propagate(0)
        self.widgets.append(Button(self.frames[-1], command=tkinter.filedialog.askopenfilename, height="132", text="button", width="33"))
        self.widgets[-1].pack()

    def run(self):
        self.window.mainloop()


if __name__ == '__main__':
    root = MainWindow()
    root.appendWidgets()
    root.run()
