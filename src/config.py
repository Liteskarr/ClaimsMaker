import json
import typing

from betterconf import Config, field
from betterconf.caster import to_int
from betterconf.config import AbstractProvider


class FileProvider(AbstractProvider):
    def __init__(self, filepath: str):
        with open(filepath, 'r', encoding='utf-8') as file:
            self._settings = json.load(file)

    def get(self, name: str) -> typing.Any:
        return self._settings.get(name, None)


MainProvider = FileProvider('settings.json')


class _MainConfig(Config):
    SHEET_NAME = field('SHEET_NAME', provider=MainProvider)
    COLUMN_START = field('COLUMN_START', provider=MainProvider, caster=to_int)
    ROW_LABEL = field('ROW_LABEL', provider=MainProvider, caster=to_int)
    ROW_DATA = field('ROW_DATA', provider=MainProvider, caster=to_int)
    TOKEN = field('DADATA_TOKEN', provider=MainProvider)


MainConfig = _MainConfig()
