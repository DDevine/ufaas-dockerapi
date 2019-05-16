from dataclasses import dataclass
from typing import Dict


@dataclass
class AuthConfig:
    username: str
    password: str

    def to_dict(self) -> Dict[str, str]:
        return {"username": self.username, "password": self.password}
