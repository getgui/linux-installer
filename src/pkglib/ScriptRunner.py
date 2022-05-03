import subprocess
import tempfile


class Runner:
    def __init__(self, scriptContent: str) -> None:
        self.scriptPath = ""
        self.process = None
        # create the script
        with tempfile.NamedTemporaryFile() as f:
            self.scriptPath = f.name
            f.write(scriptContent)

    def start(self):
        # run script in a subprocess
        self.process = subprocess.run(
            ["bash", self.scriptPath], check=True, capture_output=True
        )
        
