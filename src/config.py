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


DadataProvider = FileProvider('dadata.json')


class _DadataConfig(Config):
    TOKEN = field('TOKEN', provider=DadataProvider)


DadataConfig = _DadataConfig()

SettingsProvider = FileProvider('settings.json')


class _SettingsConfig(Config):
    SHEET_NAME = field('SHEET_NAME', provider=SettingsProvider)
    COLUMN_START = field('COLUMN_START', provider=SettingsProvider, caster=to_int)
    ROW_LABEL = field('ROW_LABEL', provider=SettingsProvider, caster=to_int)
    ROW_DATA = field('ROW_DATA', provider=SettingsProvider, caster=to_int)


SettingsConfig = _SettingsConfig()
