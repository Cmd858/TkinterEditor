class Constructor:
    def __init__(self, window, parent):
        self.window = window
        self.parent = parent
        self.fulltext = ''  # will be appended to, constructing the code object into one string
        self.commandtext = ''
        self.importtext = '\nimport '.join(self.parent.dependencies)
        self.basetext = '''

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

'''  # basetext acts as the starting point for the program to build on
        self.runtext = '''\n\nif __name__ == '__main__':
    root = MainWindow()
    root.appendWidgets()
    root.run()
'''
        self.runfunc = '''\n    def run(self):
        self.window.mainloop()
'''

    def appendWidgets(self):
        widgetText = '    def appendWidgets(self):\n'
        for widget in self.parent.widgets:
            _, frameArgs = formatArgs(widget[0])
            widgetType, widgetArgs = formatArgs(widget[1])
            widgetText += f'        self.frames.append(Frame(self.window, {frameArgs}))\n'
            widgetText += f'        self.frames[-1].place(x={widget[0].winfo_x()}, y={widget[0].winfo_y()})\n'
            widgetText += f'        self.frames[-1].pack_propagate(0)\n'
            widgetText += f'        self.widgets.append({widgetType}(self.frames[-1], {widgetArgs}))\n'
            widgetText += f'        self.widgets[-1].pack()\n'
        return widgetText

    def build(self):  # construct the program string
        self.fulltext += self.importtext
        self.fulltext += self.basetext
        self.fulltext += self.appendWidgets()
        self.fulltext += self.runfunc
        self.fulltext += self.runtext
        print(self.fulltext)


def formatArgs(widget):  # format non-default args into input  # pretty smart lol
    classtype = widget.__class__
    normdict = dict(classtype())
    compdict = dict(widget)
    print('dict')
    print(normdict)
    print(compdict)
    keys = [i for i in normdict if normdict[i] != compdict[i] and i != 'background']  # last one > stopping dupe
    values = [compdict[i] for i in keys]
    args = ', '.join([f'{i}="{j}"' if i != 'command' else f'{i}={j}' for (i, j) in zip(keys, values)])
    # arguments for widgets
    print(keys)
    print(values)
    print(args)
    return classtype.__name__, args
