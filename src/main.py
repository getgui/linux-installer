#!../env/bin/python3
import sys
import yaml
import styles
from pkglib.GGProgressBar import ProgressBarIndeterminate

from PySide6.QtCore import QThread, Qt, Signal, SignalInstance
from PySide6.QtWidgets import QLabel, QLineEdit, QPushButton, QGridLayout, QSizePolicy
from PySide6.QtGui import QImage, QPixmap

from pkglib.AsyncTask import AsyncTask
from helpers import fetchRepo, fetchImage
from pkglib.GUIMain import Page, Window, MainWindow


class MainPage(Page):
    def __init__(self, name: str, parent: Window, data=None):
        Page.__init__(self, name, parent, data)
        self.repoName = ""
        self.configure()

    def resetVerifyButton(self, state="unverified"):
        # TODO: Make state an Enum
        if state == "verified":
            self.getPageWidget("verifyButton").setText("Install")
            self.getPageWidget("verifyButton").setStyleSheet(styles.installButtonStyle)
            self.getPageWidget("verifyButton").clicked.disconnect()
            self.getPageWidget("verifyButton").clicked.connect(
                lambda: self.installRepo()
            )
        elif state == "unverified":
            self.getPageWidget("verifyButton").setText("Verify")
            self.getPageWidget("verifyButton").setStyleSheet(styles.buttonStyle)
            self.getPageWidget("verifyButton").clicked.disconnect()
            self.getPageWidget("verifyButton").clicked.connect(
                lambda: self.verifyRepo()
            )

    def displayRepoInfo(self, data=None, hide=False):
        repoLayout = self.getPageWidget("repoInfoContainer")
        if not hide:
            assert data
            content = yaml.safe_load(data)
            repoLabel = QLabel(f"{content['AppName']}")
            repoLabel.setStyleSheet(styles.normalTextStyle)

            repoAuthor = QLabel(f"{content['Author']}")
            repoAuthor.setStyleSheet(styles.subtextStyle)

            repoDesc = QLabel(f"{content['Description']}")
            repoDesc.setStyleSheet(styles.mediumTextStyle)
            repoDesc.setWordWrap(True)

            imageUrl = content["IconPath"]
            appImage = QImage()
            result, remoteImage = fetchImage(self.repoName, imageUrl)
            if result:
                # TODO: make remote image load an async task, default octocat
                appImage.loadFromData(remoteImage)
            else:
                appImage.load("./src/assets/octocat.png")
                
            imageLabel = QLabel()
            pixMap = QPixmap.fromImage(appImage.scaledToHeight(75))
            imageLabel.setPixmap(pixMap)
            imageLabel.setStyleSheet("border: 1px solid black;border-radius: 5px;")

            repoLayout.addWidget(imageLabel, 0, 0, 3, 1)
            repoLayout.addWidget(repoLabel, 0, 1)
            repoLayout.addWidget(repoAuthor, 1, 1)
            repoLayout.addWidget(repoDesc, 3, 0, 1, 2)
        else:
            for i in reversed(range(repoLayout.count())):
                repoLayout.itemAt(i).widget().deleteLater()

    def repoTextChanged(self):
        self.repoName = self.getPageWidget("repoInputBox").text()
        self.displayRepoInfo(self, hide=True)

    def configure(self):
        self.layout = QGridLayout()
        self.layout.cellRect(5, 2)
        self.layout.setRowStretch(0, 0)
        self.layout.setRowStretch(3, 1)
        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(1, 0)

        # Add title text
        titleLabel = QLabel("Git Repository")
        titleLabel.setStyleSheet(styles.titleTextStyle)
        self.layout.addWidget(titleLabel, 0, 0)

        # repo info
        repoLayout = self.addPageWidget("repoInfoContainer", QGridLayout())
        repoLayout.cellRect(4, 2)
        repoLayout.setRowStretch(0, 0)
        repoLayout.setRowStretch(1, 0)
        repoLayout.setRowStretch(2, 0)
        repoLayout.setRowStretch(3, 1)
        repoLayout.setVerticalSpacing(0)
        repoLayout.setColumnStretch(1, 1)
        repoLayout.setContentsMargins(5, 0, 0, 0)
        self.layout.addLayout(repoLayout, 2, 0, 1, 2)

        # Add Git repo input field
        repoInputBox = self.addPageWidget("repoInputBox", QLineEdit())
        repoInputBox.setPlaceholderText("Git Repo (i.e. getgui/linux-installer)")
        repoInputBox.setStyleSheet(styles.inputTextStyle)
        self.layout.addWidget(repoInputBox, 1, 0, 1, 2)
        repoInputBox.setText("getgui/download-ram")
        repoInputBox.textChanged.connect(self.repoTextChanged)

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
        self.layout.addWidget(button, 4, 1)
        self.setLayout(self.layout)
        self.show()

    def verifyRepo(self):
        self.getPageWidget("pbar").setState(True)
        print("Verifying")

        def finish(result):
            if result["result"]:
                self.resetVerifyButton("verified")
                self.displayRepoInfo(result["content"])
            self.getPageWidget("pbar").setState(False)

        self.task = AsyncTask(finish, lambda: fetchRepo(self.repoName))

    def installRepo(self):
        self.getPageWidget("pbar").setState(True)
        self.getPageWidget("verifyButton").setText("Installing...")


if __name__ == "__main__":
    app = MainWindow("Linux Installer", sys.argv)
    app.addPage(MainPage("home", app))
    app.show()
    # Create and show the form
    app.run()
