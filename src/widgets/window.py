from PyQt5.QtWidgets import (QMainWindow)

from widgets.main_widget import MainWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._configure_ui()

    def _configure_ui(self):
        self.setWindowTitle('Конструктор претензий')
        self.setCentralWidget(MainWidget())
