import json
import typing

from betterconf import Config, field
from betterconf.config import AbstractProvider


class FileProvider(AbstractProvider):
    def __init__(self, filepath: str):
        with open(filepath, 'r', encoding='utf-8') as file:
            self._settings = json.load(file)

    def get(self, name: str) -> typing.Any:
        return self._settings.get(name, None)


DadataProvider = FileProvider('dadata.json')


class _DadataConfig(Config):
    TOKEN = field('TOKEN', provider=DadataProvider)


DadataConfig = _DadataConfig()
