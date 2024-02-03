import json
from pathlib import Path
from typing import Dict, Any

CONFIG_FILE = 'config.json'


def __get_root_path(path: str) -> Path:
    return Path(__file__).parent.parent.joinpath(path)


def _read_config(path: str) -> Dict[str, Any]:
    root_path = __get_root_path(path)
    with open(root_path) as f:
        return json.load(f)


class BotConfig:
    def __init__(self, data):
        self.token = data['token']
        self.chat_group_id = data['chat_group_id']


class AppConfig:
    def __init__(self, bot):
        self.bot = bot
        # can bo add one more configs


def __get_config() -> AppConfig:
    _config = _read_config(CONFIG_FILE)
    _bot_config = _config['bot']
    bot = BotConfig(_bot_config)
    return AppConfig(bot)


def get_bot_config() -> BotConfig:
    return __get_config().bot
