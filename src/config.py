import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    itu_username: str | None = os.getenv("ITU_USERNAME")
    itu_password: str | None = os.getenv("ITU_PASSWORD")
    pushbullet_token: str | None = os.getenv("PUSHBULLET_TOKEN")
