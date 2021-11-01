#!../env/bin/python

import tkinter as tk
from tkinter.ttk import *
import pdb

class MainWindow(object):
    def __init__(self, title="Linux Installer", size="600x400"):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(size)
        self.mainParent = tk.Frame(self.root,
                                   width=self.root.winfo_width(),
                                   height=self.root.winfo_height(),
                                   bg="brown")
        self.mainParent.pack(fill="both", expand=True)
        self.mainParent.pack_propagate(0)
        self.frames = {}

    def setFrames(self, frames=None):
        assert isinstance(frames, dict)
        self.frames = frames

    def switchToFrame(self, frameName: str, data=None):
        self.clearMainParent()
        assert frameName in self.frames
        self.frames[frameName].visible()
        if data:
            self.frames[frameName].update(data)

    def clearMainParent(self):
        for widget in self.mainParent.winfo_children():
            widget.pack_forget()

    def show(self):
        assert 'main' in self.frames, "'main' page not present "
        self.switchToFrame('main')
        self.root.mainloop()

class Page(object):
    def __init__(self, parent, **params):
        self.parent = parent
        self.frame = tk.Frame(parent, **params)

    def update(self, data):
        # this function is called when transition to
        # this page is made. Previous page can supply some
        # data to update this page
        raise NotImplementedError

    def visible(self):
        self.frame.pack(fill="both", expand=True)
        self.frame.pack_propagate(0)



class MainInstallPage(Page):
    def __init__(self, mainWindow: MainWindow):
        self.mainWindow = mainWindow
        Page.__init__(
            self, mainWindow.mainParent,
            width=mainWindow.mainParent.winfo_width(),
            height=mainWindow.mainParent.winfo_height(),
        )
        self.configure()

    def configure(self):
        self.frame.rowconfigure(5)
        self.frame.columnconfigure(3)
        self.frame.grid_rowconfigure(0, minsize=20 )
        self.frame.grid_rowconfigure(2, weight=4)
        self.frame.grid_rowconfigure(4, minsize=20 )
        self.frame.grid_columnconfigure(0, minsize=30)
        self.frame.grid_columnconfigure(1, weight=5)
        self.frame.grid_columnconfigure(2, minsize=30)

        # title frame
        titleFrame = tk.Frame(self.frame)
        titleFrame.grid(row=1, column=1, sticky="ew")
        titleLabel = tk.Label(
            titleFrame, text="Git Repository", font=(None, 14),
            justify='left'
        )
        entryCfg={ 'font': (None, 12)}
        titleText = tk.Entry(titleFrame, **entryCfg)
        titleLabel.pack(anchor='w', )
        titleText.pack(anchor='e', fill='both' )


        # progress bar frame
        progressBarFrame = tk.Frame(self.frame)
        progressBarFrame.grid(row=2, column=1, sticky="sew", pady=20)

        # progress bar
        def pgRunner(bar):
            def bb():
                bar['value']=(bar['value']+1) % 200
                bar.after( 10, bb )
            return bb

        pgbar = Progressbar(progressBarFrame, length=100, value=0,
                            mode='indeterminate')
        pgbar.pack(side='bottom')

        # buttons
        buttonFrame = tk.Frame(self.frame)
        buttonFrame.grid(row=3, column=1, sticky="ew")
        btnCfg = {"width": 30}


        # exit button
        exitButton = tk.Button(
            buttonFrame, text="Exit", command=self.mainWindow.root.destroy, **btnCfg
        )
        exitButton.pack(side='right')

        # verify button
        exitButton = tk.Button(
            buttonFrame, text="Verify", command=pgRunner(pgbar),  **btnCfg
        )
        exitButton.pack(side='right')

        titleFrame.grid_propagate(0)

if __name__ == '__main__':
    window = MainWindow()
    frames = {
        "main" : MainInstallPage(window)
    }
    window.setFrames(frames)
    window.show()
