from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore")

    model: str = Field(alias="MODEL")
    camera_url: str = Field(alias="CAMERA_URL")
    confidence_threshold: float = Field(alias="CONFIDENCE_THRESHOLD")
    check_interval: int = Field(alias="CHECK_INTERVAL")
    bot_token: str = Field(alias="BOT_TOKEN")
    message_chat_ids: list[int] = Field(alias="MESSAGE_CHAT_IDS")

    @field_validator("message_chat_ids", mode="before")
    @classmethod
    def parse_chat_ids(cls, v: Any) -> list[int]:
        if isinstance(v, int | float):
            return [int(v)]
        elif isinstance(v, str):
            v = v.strip()
            if v.startswith("[") and v.endswith("]"):
                content = v[1:-1].strip()
                if content:
                    return [int(x.strip()) for x in content.split(",") if x.strip()]
                else:
                    return []
            else:
                return [int(v)]
        elif isinstance(v, list):
            return v
        return v


config: Config = Config()
