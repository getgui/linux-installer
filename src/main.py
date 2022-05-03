#!../env/bin/python3
import sys
import os
from pkglib.ScriptRunner import Runner
import styles
from pkglib.GGProgressBar import ProgressBarIndeterminate
from pkglib.Response import Response

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QPushButton,
    QGridLayout,
    QScrollArea,
    QHBoxLayout,
)
from PySide6.QtGui import QPixmap, QFontDatabase

import enum
from pkglib.AsyncTask import AsyncTask
from pkglib.GUIMain import Page, Window, MainWindow
from helpers import buildLicenseUrl, buildUrl, fetchRepo, fetchContent
from Repository import Repo

ROOT = os.getcwd()


class VerifyState(enum.Enum):
    VERIFIED = 0
    UNVERIFIED = 1


class MainPage(Page):
    def __init__(self, name: str, parent: Window, data=None):
        Page.__init__(self, name, parent, data)
        self.repoName = ""
        self.repoInfo = None
        self.configure()

    def resetVerifyButton(self, state: VerifyState):
        # TODO: Make state an Enum
        if state == VerifyState.VERIFIED:
            self.getPageWidget("verifyButton").setText("Install")
            self.getPageWidget("verifyButton").setStyleSheet(styles.installButtonStyle)
            self.getPageWidget("verifyButton").clicked.disconnect()
            self.getPageWidget("verifyButton").clicked.connect(self.installRepo)
        elif state == VerifyState.UNVERIFIED:
            self.getPageWidget("verifyButton").setText("Verify")
            self.getPageWidget("verifyButton").setStyleSheet(styles.buttonStyle)
            self.getPageWidget("verifyButton").clicked.disconnect()
            self.getPageWidget("verifyButton").clicked.connect(self.verifyRepo)

    def displayMessage(self, message=None):
        messageBox = self.getPageWidget("messageBox")
        messageIcon = self.getPageWidget("messageIcon")
        if message:
            messageBox.setText(message)
            messageBox.setStyleSheet(styles.errorTextStyle)
            messageIcon.setStyleSheet(styles.errorIconStyle)
            messageIcon.setText("\uEA6C")
        else:
            messageBox.setText("")
            messageIcon.setText("")

    def displayRepoInfo(self, data=None, hide=False):
        repoLayout = self.getPageWidget("repoInfoContainer")
        if not hide:
            assert data
            self.repoInfo = Repo()
            self.repoInfo.loadRepo(self.repoName, data)
            repoLabel = QLabel(self.repoInfo.appName)
            repoLabel.setStyleSheet(styles.normalTextStyle)

            repoAuthor = QLabel(self.repoInfo.author)
            repoAuthor.setStyleSheet(styles.subtextStyle)

            scrollableDesc = QScrollArea()
            scrollableDesc.setFrameShape(QScrollArea.NoFrame)
            scrollableDesc.setStyleSheet("padding: 0 10px 0 0;")
            scrollableDesc.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            # Will expand content inside scroll area to fill available space
            scrollableDesc.setWidgetResizable(True)
            repoDesc = QLabel(self.repoInfo.repoDescription)
            repoDesc.setStyleSheet(styles.mediumTextStyle)
            repoDesc.setWordWrap(True)
            scrollableDesc.setWidget(repoDesc)

            imageLabel = QLabel()
            pixMap = QPixmap.fromImage(self.repoInfo.repoImage.scaledToHeight(75))
            imageLabel.setPixmap(pixMap)

            repoLayout.addWidget(imageLabel, 0, 0, 3, 1)
            repoLayout.addWidget(repoLabel, 0, 1)
            repoLayout.addWidget(repoAuthor, 1, 1)
            repoLayout.addWidget(scrollableDesc, 3, 0, 1, 2)
        else:
            for i in reversed(range(repoLayout.count())):
                repoLayout.itemAt(i).widget().deleteLater()

    def repoTextChanged(self):
        self.repoName = self.getPageWidget("repoInputBox").text()
        self.displayRepoInfo(self, hide=True)
        self.resetVerifyButton(VerifyState.UNVERIFIED)
        self.displayMessage(None)

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
        button.clicked.connect(self.verifyRepo)
        button.setStyleSheet(styles.buttonStyle)
        self.layout.addWidget(button, 4, 1)

        # Add message box (for error messages)
        messageContainer = QHBoxLayout()
        messageContainer.addWidget(self.addPageWidget("messageIcon", QLabel()))
        messageContainer.addWidget(self.addPageWidget("messageBox", QLabel()))
        messageContainer.insertStretch(2, 1)
        self.layout.addLayout(messageContainer, 4, 0)

        self.setLayout(self.layout)
        self.show()

    def verifyRepo(self):
        self.getPageWidget("pbar").setState(True)

        def finish(result):
            if result["result"]:
                self.resetVerifyButton(VerifyState.VERIFIED)
                self.displayRepoInfo(result["content"])
            else:
                self.displayMessage(f"Unsupported Repository <b>{self.repoName}</b>")
            self.getPageWidget("pbar").setState(False)

        self.task = AsyncTask(finish, lambda: fetchRepo(self.repoName))

    def installRepo(self):
        # fetch LICENSE and set the license content in repo
        def setLicenseContent(result: Response):
            if result.success:
                self.repoInfo.license = result.content.decode("UTF-8")
            self.getPageWidget("pbar").setState(False)
            self.parentWindow.gotoPage("license", self.repoInfo)

        self.getPageWidget("pbar").setState(True)
        licenseUrl = buildLicenseUrl(self.repoName)
        self.task = AsyncTask(setLicenseContent, lambda: fetchContent(licenseUrl))


class LicensePage(Page):
    def __init__(self, name: str, parent: Window, data=None):
        Page.__init__(self, name, parent, data)
        self.configure()
        self.repoInfo: Repo = None

    def update(self, data: Repo = None):
        if data:
            self.repoInfo = data
            repoLabel = self.getPageWidget("repoLabel")
            repoLabel.setText(data.appName)
            licenseLabel = self.getPageWidget("licenseLabel")
            licenseLabel.setText(data.license.replace(r"\n", "<br>"))

    def configure(self):
        self.layout = QGridLayout()
        self.layout.cellRect(5, 3)
        self.layout.setRowStretch(0, 0)
        self.layout.setRowStretch(3, 1)
        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(1, 0)
        self.layout.setColumnStretch(2, 0)

        # Add title text
        titleLabel = QLabel("License Agreement")
        titleLabel.setStyleSheet(styles.titleTextStyle)
        self.layout.addWidget(titleLabel, 0, 0)

        # Repo Name
        repoLabel = self.addPageWidget("repoLabel", QLabel())
        repoLabel.setStyleSheet(styles.normalTextStyle)
        self.layout.addWidget(repoLabel, 1, 0)

        # license container
        scrollableDesc = QScrollArea()
        scrollableDesc.setFrameShape(QScrollArea.NoFrame)
        scrollableDesc.setStyleSheet("padding: 10px 10px 0 0;")
        scrollableDesc.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # Will expand content inside scroll area to fill available space
        scrollableDesc.setWidgetResizable(True)
        licenseText = self.addPageWidget("licenseLabel", QLabel())
        licenseText.setStyleSheet(styles.mediumTextStyle)
        licenseText.setWordWrap(True)
        scrollableDesc.setWidget(licenseText)
        self.layout.addWidget(scrollableDesc, 3, 0, 1, 3)

        # Add Verify button button
        button = self.addPageWidget("acceptButton", QPushButton("Accept && &Continue"))
        button.clicked.connect(
            lambda: self.parentWindow.gotoPage("install", self.repoInfo)
        )
        button.setStyleSheet(styles.installButtonStyle)
        self.layout.addWidget(button, 4, 2)

        # Go back button
        button = self.addPageWidget("rejectButton", QPushButton("Go &Back"))
        button.clicked.connect(lambda: self.parentWindow.gotoPage("home"))
        button.setStyleSheet(styles.buttonStyle)
        self.layout.addWidget(button, 4, 1)

        # show layout
        self.setLayout(self.layout)
        self.show()


class InstallPage(Page):
    def __init__(self, name: str, parent: Window, data=None):
        super().__init__(name, parent, data)
        self.configure()
        self.repoInfo: Repo = None
        self.scriptRunner : Runner

    def update(self, data: Repo = None):
        if data:
            self.repoInfo = data
            titleLabel = self.getPageWidget("titleLabel")
            titleLabel.setText(f"Installing <b>{self.repoInfo.appName}</b>")
            self.install()

    def install(self):
        installScriptContent = fetchContent(
            buildUrl(self.repoInfo.repoName, self.repoInfo.installScriptPath)
        )
        self.scriptRunner = Runner(installScriptContent)
        # Run here

    def configure(self):
        self.layout = QGridLayout()
        self.layout.cellRect(5, 3)
        self.layout.setRowStretch(0, 0)
        self.layout.setRowStretch(3, 1)
        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(1, 0)
        self.layout.setColumnStretch(2, 0)

        # Add title text
        titleLabel = self.addPageWidget("titleLabel", QLabel())
        titleLabel.setStyleSheet(styles.titleTextStyle)
        self.layout.addWidget(titleLabel, 0, 0)

        # Repo Name
        repoLabel = self.addPageWidget("logLabel", QLabel())
        repoLabel.setStyleSheet(styles.normalTextStyle)
        repoLabel.setText("[1/34] Updating environment variables.")
        self.layout.addWidget(repoLabel, 1, 0)

        # script logs container - shows output of the running script
        scrollableDesc = QScrollArea()
        scrollableDesc.setFrameShape(QScrollArea.NoFrame)
        scrollableDesc.setStyleSheet("padding: 10px 10px 0 0;")
        scrollableDesc.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # Will expand content inside scroll area to fill available space
        scrollableDesc.setWidgetResizable(True)
        scriptLogLabel = self.addPageWidget("scriptOutputLabel", QLabel())
        scriptLogLabel.setStyleSheet(styles.mediumTextStyle)
        scriptLogLabel.setWordWrap(True)
        scrollableDesc.setWidget(scriptLogLabel)
        self.layout.addWidget(scrollableDesc, 3, 0, 1, 3)

        # Just a test function that adds logs and scrolls to bottom
        def test():
            scriptLogLabel.setText(
                scriptLogLabel.text() + "Doing something not needed<br>"
            )
            verticalBar = scrollableDesc.verticalScrollBar()
            print(verticalBar.maximum())
            verticalBar.setValue(verticalBar.maximum())

        # Cancel install button
        button = self.addPageWidget("cancelButton", QPushButton("&Cancel"))
        button.clicked.connect(test)
        button.setStyleSheet(styles.buttonStyle)
        self.layout.addWidget(button, 4, 2)

        # show layout
        self.setLayout(self.layout)
        self.show()


if __name__ == "__main__":
    app = MainWindow("Linux Installer", sys.argv)
    QFontDatabase.addApplicationFont(ROOT + "/src/assets/codicon.ttf")
    app.addPage(MainPage("home", app))
    app.addPage(LicensePage("license", app))
    app.addPage(InstallPage("install", app))
    app.show()
    # Create and show the form
    app.run()
