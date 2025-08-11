from dataclasses import dataclass
from typing import Optional
try:
    from pushbullet import Pushbullet as _Pushbullet
except Exception:
    _Pushbullet = None  # allow running without library

@dataclass
class PushbulletNotifier:
    token: Optional[str]

    def send(self, title: str, body: str) -> bool:
        if not self.token or not _Pushbullet:
            return False
        try:
            pb = _Pushbullet(self.token)
            pb.push_note(title, body)
            return True
        except Exception:
            return False
