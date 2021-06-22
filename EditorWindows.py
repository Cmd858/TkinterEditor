from tkinter import *


class EditorWindow:
    def __init__(self, root, manager, key):
        self.root = root  # root window
        self.manager = manager  # class for window management in main
        self.key = key  # key for dictionary value that is being edited
        self.window = Toplevel(root)
        self.window.title("Edit")
        self.window.geometry(f"200x70+{root.winfo_rootx()+50}+{root.winfo_rooty()+50}")
        # self.window.overrideredirect(1)
        Label(self.window, text=self.key).pack(side='top')
        self.entry = Entry(self.window, text='hello')
        self.entry.pack(side='top')
        self.enter = Button(self.window, text='Enter', command=self.returnValue).pack(side='top')

    def returnValue(self):
        self.manager.returnEditor(self.key, self.entry.get())
        self.destroySelf()

    def destroySelf(self):
        try:
            self.window.destroy()
        except:
            pass


class PropertyWindow:  # property selection for editor window
    def __init__(self, root, manager, widget):
        self.root = root  # root window
        self.manager = manager  # class for window management in main
        self.widget = widget[1]  # widget from which the properties are taken  # also [1] bc its list of [frame, widget]
        self.window = Toplevel(root, relief='ridge', bd=1)
        self.window.title("Edit")
        mx, my = self.window.winfo_pointerxy()
        self.window.geometry(f"200x400+{mx}+{my}")
        self.window.overrideredirect(1)
        self.buttons = Listbox(self.window, width=200, height=200)
        self.buttons.pack_propagate(1)
        self.buttons.bind('<ButtonRelease-1>', self.selected)
        self.destroyable = False  # ^ and destroyable to prevent new label being erroneously made on main window
        for item in dict(self.widget):
            self.buttons.insert(END, item)
        self.buttons.pack()


    def hoverColour(self, event):
        etype = str(event.type)
        if etype == 'Enter':
            event.widget['bg'] = 'grey'
        elif etype == 'Leave':
            event.widget['bg'] = 'white'

    def selected(self, event):
        selected = self.buttons.curselection()
        if not str(selected) == '()':
            item = self.buttons.get(selected)
            self.manager.returnProperties(item)
            self.destroySelf()

    def destroySelf(self):
        self.manager.propertyWindow = None
        self.window.destroy()

class EntryWindow:
    def __init__(self, root, manager, callback, text):
        self.root = root  # root window
        self.manager = manager  # class for window management in main
        self.callback = callback
        self.window = Toplevel(root)
        self.window.title("Edit")
        self.window.geometry(f"200x70+{root.winfo_rootx()+50}+{root.winfo_rooty()+50}")
        # self.window.overrideredirect(1)
        Label(self.window, text=text).pack(side='top')
        self.entry = Entry(self.window, text='hello')
        self.entry.pack(side='top')
        self.enter = Button(self.window, text='Enter', command=self.returnValue).pack(side='top')

    def returnValue(self):
        self.callback(self.entry.get())
        self.destroySelf()

    def destroySelf(self):
        try:
            self.window.destroy()
        except:
            pass