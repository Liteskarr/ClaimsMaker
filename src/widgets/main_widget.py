import os

from PyQt5.QtWidgets import (QWidget,
                             QFileDialog)
from PyQt5.QtCore import (pyqtSignal)
from PyQt5.uic import loadUi
from docxtpl import DocxTemplate

from widgets.working_dialog import WorkingDialog
from dadata_parser import get_entities_by_inn
from data_parser import parse_file
from builder import build
from worker import Worker


class ResultPrinter(Worker):
    data_loaded = pyqtSignal()
    data_checked = pyqtSignal()
    data_printed = pyqtSignal()

    def __init__(self, data_path: str, template_path: str, output_path: str):
        super().__init__(self._target, data_path, template_path, output_path)

    def _target(self, data_path, template_path, output_path):
        records = list(parse_file(data_path))
        inns = list(set(map(lambda x: x.TargetINN, records)))
        self.data_loaded.emit()
        entities = get_entities_by_inn(inns, type='LEGAL')
        self.data_checked.emit()
        for entity in entities:
            if not entity.IsActive:
                continue
            r = list(filter(lambda x: x.TargetINN == entity.INN, records))
            build(r, {}, DocxTemplate(template_path), os.path.join(output_path, f'{entity.INN}.docx'))
        self.data_printed.emit()


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.template_path = ''
        self.data_path = ''
        self.dir_path = ''
        self.dialog: WorkingDialog = None
        self._configure_ui()

    def _configure_ui(self):
        loadUi('res/main_widget.ui', self)
        self.load_template_button.clicked.connect(self.load_template)
        self.load_data_button.clicked.connect(self.load_data)
        self.choose_dir_button.clicked.connect(self.choose_dir)
        self.print_result_button.clicked.connect(self.print_result)
        self._update_ui()

    def load_template(self):
        self.template_path = QFileDialog.getOpenFileName(self, 'Выбор файла', '', '', '')[0]
        if self.template_path:
            self.template_line.setText(self.template_path)
        self._update_ui()

    def load_data(self):
        self.data_path = QFileDialog.getOpenFileName(self, 'Выбор файла', '', '', '')[0]
        if self.data_path:
            self.data_line.setText(self.data_path)
        self._update_ui()

    def choose_dir(self):
        self.dir_path = QFileDialog.getExistingDirectory(self, 'Выбор директории', '', QFileDialog.ShowDirsOnly)
        if self.dir_path:
            self.dir_line.setText(self.dir_path)
        self._update_ui()

    def handle_data_loading(self):
        self.working_dialog.set_state('Сбор данных организаций', 50)

    def handle_data_checking(self):
        self.working_dialog.set_state('Распечатка претензий', 75)

    def handle_data_printing(self):
        self.working_dialog.set_state('Завершено!', 100)
        self.working_dialog.close()
        self.working_dialog = None

    def print_result(self):
        self.working_dialog = WorkingDialog(self)
        self.working_dialog.show()
        self.working_dialog.set_state('Загрузка данных', 25)
        printer = ResultPrinter(self.data_path, self.template_path, self.dir_path)
        printer.data_loaded.connect(self.handle_data_loading)
        printer.data_checked.connect(self.handle_data_checking)
        printer.data_printed.connect(self.handle_data_printing)
        printer.run()

    def _update_ui(self):
        self.print_result_button.setEnabled(bool(self.dir_path) and bool(self.data_path) and bool(self.template_path))
