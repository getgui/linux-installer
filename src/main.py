#!../env/bin/python3
import sys
import pdb
import styles
from pkglib.GGProgressBar import ProgressBarIndeterminate

from PySide6.QtCore import QThread, Qt, Signal, SignalInstance
from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QPushButton,
    QGridLayout,
)

from pkglib.AsyncTask import AsyncTask
from helpers import fetchRepo
from pkglib.GUIMain import Page, Window, MainWindow


class MainPage(Page):
    def __init__(self, name: str, parent: Window, data=None):
        Page.__init__(self, name, parent, data)
        self.configure()

    def configure(self):
        self.layout = QGridLayout()
        self.layout.cellRect(4, 2)
        self.layout.setRowStretch(0, 0)
        self.layout.setRowStretch(2, 1)
        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(1, 0)

        # Add title text
        titleLabel = QLabel("Git Repository")
        titleLabel.setStyleSheet(styles.titleTextStyle)
        self.layout.addWidget(titleLabel, 0, 0)

        # Add Git repo input field
        repoInputBox = self.addPageWidget("repoInputBox", QLineEdit())
        repoInputBox.setPlaceholderText("Git Repo (i.e. getgui/linux-installer)")
        repoInputBox.setStyleSheet(styles.inputTextStyle)
        self.layout.addWidget(repoInputBox, 1, 0, 1, 2)
        repoInputBox.setText("getgui/download-ram")

        # Add progress bar
        progressBar = self.addPageWidget("pbar", ProgressBarIndeterminate())
        self.layout.addWidget(progressBar, 1, 0, 1, 2, Qt.AlignBottom)
        progressBar.setFixedHeight(4)
        progressBar.setMargin([5, 0, 10, 0])
        progressBar.setVisible(False)

        # Add Verify button button
        button = self.addPageWidget("verifyButton", QPushButton("Verify"))
        button.clicked.connect(lambda: self.verifyRepo())
        button.setStyleSheet(styles.buttonStyle)
        self.layout.addWidget(button, 3, 1)
        self.setLayout(self.layout)
        self.show()

    def verifyRepo(self):
        self.getPageWidget("pbar").setState(True)
        print("Verifying")
        def finish(result):
            if result['result' ]:
                verifyButton = self.getPageWidget("verifyButton")
                verifyButton.setText("Install")
                self.counter = 1
                print("Reassigned")
                verifyButton.clicked.disconnect()
                verifyButton.clicked.connect(lambda: self.installRepo())
                verifyButton.setStyleSheet(styles.installButtonStyle)
            self.getPageWidget("pbar").setState(False)
            # self.task = None
            
        # assign to a variable to avoid garbage collection
        repoName = self.getPageWidget("repoInputBox").text()
        self.task = AsyncTask(finish, lambda: fetchRepo(repoName))

    def installRepo(self):
        self.getPageWidget("pbar").setState(True)
        self.getPageWidget("verifyButton").setText("Installing...")
        # self.task = None


if __name__ == "__main__":
    app = MainWindow("Linux Installer", sys.argv)
    app.addPage(MainPage("home", app))
    app.show()
    # Create and show the form
    app.run()
