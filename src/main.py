#!../env/bin/python3
import sys
import pdb
import styles
from pkglib.GGProgressBar import ProgressBarIndeterminate

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QPushButton,
    QGridLayout,
)
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
        repoInputBox = QLineEdit()
        repoInputBox.setPlaceholderText("Git Repo (i.e. getgui/linux-installer)")
        repoInputBox.setStyleSheet(styles.inputTextStyle)
        self.layout.addWidget(repoInputBox, 1, 0, 1, 2)

        # Add progress bar
        progressBar = self.addPageWidget("pbar", ProgressBarIndeterminate())
        self.layout.addWidget(progressBar, 1, 0, 1, 2, Qt.AlignBottom)
        progressBar.setFixedHeight(4)
        progressBar.setMargin([5, 0, 10, 0])
        progressBar.setVisible(False)

        # Add Verify button button
        button = self.addPageWidget("verifyButton", QPushButton("Verify"))
        button.clicked.connect(lambda: progressBar.setState(True))
        button.setStyleSheet(styles.buttonStyle)
        self.layout.addWidget(button, 3, 1)
        self.setLayout(self.layout)
        self.show()

    def update(self, data=None):
        print("Updated : " + str(self.getName()))
        self.getPageWidget("verifyButton").setText(data["text"])


if __name__ == "__main__":
    app = MainWindow("Linux Installer", sys.argv)
    app.addPage(MainPage("home", app))
    app.show()
    # Create and show the form
    app.run()
