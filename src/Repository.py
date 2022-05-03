from dataclasses import dataclass
from PySide6.QtGui import QImage
import yaml
from helpers import fetchImage


@dataclass
class Repo:
    appName: str
    author: str
    repoName: str
    repoUrl: str
    repoImageUrl: str
    repoDescription: str
    repoImage: QImage
    license: str
    installScriptPath: str

    def __init__(self) -> None:
        pass

    def loadRepo(self, repoName: str, yamlData: str):
        content = yaml.safe_load(yamlData)
        self.repoName = repoName
        self.appName = content["AppName"]
        self.author = content["Author"]
        self.repoDescription = content["Description"]
        self.repoImageUrl = content["IconPath"]
        self.installScriptPath = content["InstallScript"]
        self.repoImage = QImage()
        result, remoteImage = fetchImage(self.repoName, self.repoImageUrl)
        if result:
            # TODO: make remote image load an async task, default octocat
            self.repoImage.loadFromData(remoteImage)
        else:
            self.repoImage.load("./src/assets/octocat.png")
        self.repoUrl = f"https://raw.githubusercontent.com/{str(repoName)}/master/"
        self.license = None
