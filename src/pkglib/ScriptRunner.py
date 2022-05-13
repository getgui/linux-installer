import subprocess


class Runner:
    def __init__(self, scriptContent: bytes) -> None:
        self.scriptPath = ""
        self.process = None
        self.stdout = None
        self.stderr = None
        # create the script
        with open("/tmp/installer.sh", "w") as f:
            self.scriptPath = f.name
            f.write(scriptContent.decode("UTF-8"))

    def start(self):
        # run script in a subprocess
        self.process = subprocess.Popen(
            ["bash", self.scriptPath],
            stdout=subprocess.PIPE,
        )
