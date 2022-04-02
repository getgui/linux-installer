#!../../../env/bin/python
from PySide6.QtWidgets import (
    QStackedWidget,
    QApplication,
    QWidget,
)
import sys
# Base class from which all other windows inherit
# A window has a title and a stacked widget.
# It can add pages to the page stack and switch between them.
class Window(object):
    def __init__(self, name: str, app: QApplication):
        self.app = app
        self.pageStack = QStackedWidget()
        self.pageStack.setWindowTitle(name)
        self.pageStackSize = 0
        self.pageInfo = {}
        self.setMinSize()

    def addPage(self, page):
        self.pageStack.addWidget(page)
        self.pageInfo.update({page.getName(): self.pageStackSize})
        self.pageStackSize += 1

    def gotoPage(self, pageName: str, data=None):
        # data is a dict of data to be passed to the page from the previous page
        self.pageStack.widget(self.pageInfo[pageName]).update(data)
        self.pageStack.setCurrentIndex(self.pageInfo[pageName])

    def setWindowSize(self, width, height):
        self.pageStack.resize(width, height)

    def setMinSize(self):
        self.pageStack.resize(640, 140)

    def show(self):
        self.pageStack.show()

    def close(self):
        self.app.quit()

    def run(self):
        sys.exit(self.app.exec())


# MainWindow is actual window in the application that is created
# and displayed.
class MainWindow(Window):
    def __init__(self, name="", args=None):
        args = [] if args is None else args
        self.app = QApplication(args)
        Window.__init__(self, name, self.app)


# Page is the base class that all pages inherit from.
# It can be added to the window's page stack.
# Data can be passed to the page from the previous page.
class Page(QWidget):
    def __init__(self, name: str, parent: Window, data=None):
        QWidget.__init__(self, parent.pageStack)
        self.parentWindow = parent
        self.parentWindow.pageStack.addWidget(self)
        self.name = name
        self.layout = None
        self.pageWidgets = {}

    def configure(self):
        # configure page specific stuff i.e. buttons, labels, etc.
        raise NotImplementedError("configure method not implemented")

    def update(self, data=None):
        # implement update method to update page with data from previous page
        if data is not None:
            return data

    def addPageWidget(self, name, widget):
        self.pageWidgets.update({name: widget})
        return widget

    def getPageWidget(self, name):
        return self.pageWidgets[name]

    def getName(self):
        return self.name
