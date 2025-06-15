
from dataclasses import dataclass

@dataclass
class User:
    username: str
    role: str

@dataclass
class Message:
    sender: str
    content: str
