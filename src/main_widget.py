from datetime import datetime
from decimal import Decimal

from PyQt5.QtWidgets import (QWidget,
                             QFileDialog,
                             QListWidgetItem,
                             QMessageBox)
from PyQt5.uic import loadUi

from src.background_process import BackgroundProcess, BackgroundProcessArgs
from src.config_dialog import ConfigDialog
from src.entity import Entity
from src.months import MONTHS
from src.progress_dialog import ProgressDialog


class MainWidget(QWidget):
    RECORDS_FILTERS = {
        'Претензия': lambda r: r.Credit == Decimal('0'),
        'Запрос': lambda r: r.Debit == Decimal('0'),
        'Претензия с запросом': lambda r: True,
    }

    ENTITIES_TYPE_FILTERS = {
        'ИП': {'type': 'INDIVIDUAL'},
        'ЮЛ': {'type': 'LEGAL'},
        'ВСЕ': {}
    }

    def __init__(self):
        super().__init__()
        # Paths
        self.template_path: str = ''
        self.data_paths: list[str] = []
        self.dir_path: str = ''
        # Settings
        self.current_filter = self.RECORDS_FILTERS['Претензия']
        self.current_type_filter = self.ENTITIES_TYPE_FILTERS['ВСЕ']
        self.date = ''
        self.number = ''
        # Other widgets
        self.dialog = ProgressDialog(self)
        self._configure_ui()
        self.set_today_date()

    def _configure_ui(self):
        loadUi('res/main_widget.ui', self)
        # Non-settings buttons
        self.load_template_button.clicked.connect(self.load_template)
        self.add_data_button.clicked.connect(self.add_data)
        self.delete_data_button.clicked.connect(self.delete_data)
        self.choose_dir_button.clicked.connect(self.choose_dir)
        self.print_result_button.clicked.connect(self.print_result)
        self.config_button.clicked.connect(self._handle_config_opening)
        # Filters
        self.claim_radio.toggled.connect(lambda: self.change_filter(self.claim_radio.text()))
        self.request_radio.toggled.connect(lambda: self.change_filter(self.request_radio.text()))
        self.claim_request_radio.toggled.connect(lambda: self.change_filter(self.claim_request_radio.text()))
        # Type Filters
        self.legal_radio.toggled.connect(lambda: self.change_type_filter(self.legal_radio.text()))
        self.individual_radio.toggled.connect(lambda: self.change_type_filter(self.individual_radio.text()))
        self.all_radio.toggled.connect(lambda: self.change_type_filter(self.all_radio.text()))
        # Date
        self.date_line.editingFinished.connect(self.change_date)
        # Number
        self.number_line.editingFinished.connect(self.change_number)
        self._update_ui()

    def change_date(self):
        self.date = self.date_line.text()

    def set_today_date(self):
        self.date_line.setText(datetime.now().strftime(f'%d {MONTHS[datetime.now().month]} %Y'))
        self.change_date()

    def change_number(self):
        self.number = self.number_line.text()

    def change_type_filter(self, text: str):
        self.current_type_filter = self.ENTITIES_TYPE_FILTERS[text]

    def change_filter(self, text: str):
        self.current_filter = self.RECORDS_FILTERS[text]

    def load_template(self):
        self.template_path = QFileDialog.getOpenFileName(self, 'Выбор файла', '', '*.docx')[0]
        if self.template_path:
            self.template_line.setText(self.template_path)
        self._update_ui()

    def add_data(self):
        data_path = QFileDialog.getOpenFileName(self, 'Выбор файла', '', '*.xlsx')[0]
        if data_path and data_path not in self.data_paths:
            self.data_paths.append(data_path)
            self.data_list.addItem(QListWidgetItem(data_path))
        self._update_ui()

    def delete_data(self):
        deleted_item = self.data_list.currentItem()
        if deleted_item:
            self.data_paths.remove(deleted_item.text())
            self.data_list.takeItem(self.data_list.currentRow())
        self._update_ui()

    def choose_dir(self):
        self.dir_path = QFileDialog.getExistingDirectory(self, 'Выбор директории', '', QFileDialog.ShowDirsOnly)
        if self.dir_path:
            self.dir_line.setText(self.dir_path)
        self._update_ui()

    def _handle_config_opening(self):
        ConfigDialog(self, 'settings.json').show()

    def _handle_starting(self):
        self.dialog.show()
        self.dialog.set_state('Начало работы', percent=0)

    def _handle_record_reading(self, filename: str, number: int, count: int):
        self.dialog.set_state(f'Чтение файла: {filename}', int(number / count * 100))

    def _handle_entity_processing(self, entity: Entity, number: int, count: int):
        self.dialog.set_state(f'Сбор данных по ИНН: {entity.INN}', percent=int(100 * number / count))

    def _handle_entity_printing(self, entity: Entity, number: int, count: int):
        self.dialog.set_state(f'Распечатка данных по ИНН: {entity.INN}', percent=int(100 * number / count))

    def _handle_error(self, message: str):
        self._handle_finishing()
        message_box = QMessageBox(self)
        message_box.setIcon(QMessageBox.Critical)
        message_box.setWindowTitle('Ошибка!')
        message_box.setText('При выполнении операции произошла ошибка!')
        message_box.setInformativeText(message)
        message_box.exec()

    def _handle_finishing(self):
        self.dialog.set_state('', percent=0)
        self.dialog.hide()

    def print_result(self):
        args = BackgroundProcessArgs(
            self.data_paths,
            self.template_path,
            self.dir_path,
            self.number,
            self.date,
            self.current_filter,
            self.current_type_filter
        )
        process = BackgroundProcess(args)
        process.started.connect(self._handle_starting)
        process.record_read.connect(self._handle_record_reading)
        process.entity_processed.connect(self._handle_entity_processing)
        process.entity_printed.connect(self._handle_entity_printing)
        process.error.connect(self._handle_error)
        process.finished.connect(self._handle_finishing)
        process.run()

    def _update_ui(self):
        self.print_result_button.setEnabled(bool(self.dir_path) and bool(self.data_paths) and bool(self.template_path))
