from PyQt5.QtWidgets import (QWidget,
                             QDialog)
from PyQt5.uic import loadUi


class WorkingDialog(QDialog):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._configure_ui()

    def _configure_ui(self):
        loadUi('res/dialog.ui', self)

    def set_state(self, state: str, percent: int):
        self.label.setText(state)
        self.progress.setValue(percent)
