from PyQt5.QtWidgets import (QApplication)

from widgets.window import MainWindow


def enable_threads_exceptions() -> None:
    import sys
    excepthook = sys.excepthook

    def exception_hook(exctype, value, traceback):
        excepthook(exctype, value, traceback)
        sys.exit(1)

    sys.excepthook = exception_hook


def main():
    enable_threads_exceptions()
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec()


if __name__ == '__main__':
    main()
