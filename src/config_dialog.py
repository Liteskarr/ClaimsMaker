from PyQt5.QtWidgets import (QDialog,
                             QWidget)
from PyQt5.uic import loadUi


class ConfigDialog(QDialog):
    def __init__(self, parent: QWidget, config_filepath: str):
        super().__init__(parent)
        self._config_filepath = config_filepath
        self._text = ''
        with open(config_filepath, 'r', encoding='utf-8') as config:
            self._text = ''.join(config.readlines())
        self._configure_ui()

    def _configure_ui(self):
        loadUi('res/config_dialog.ui', self)
        self.text_area.setPlainText(self._text)
        self.save_button.clicked.connect(self._handle_result_saving)

    def _handle_result_saving(self):
        with open(self._config_filepath, 'w', encoding='utf-8') as config:
            config.write(self.text_area.toPlainText())
        self.close()
