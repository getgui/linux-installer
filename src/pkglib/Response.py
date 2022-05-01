from dataclasses import dataclass


@dataclass
class Response:
    success: bool
    content: None

    def __init__(self, success, content) -> None:
        self.success = success
        self.content = content
