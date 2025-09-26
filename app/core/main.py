import sys
from PySide6.QtWidgets import QApplication
from app.ui.app_ui import AppMainWindow
from app.core.cache import init_db


def main():
    init_db()
    app = QApplication(sys.argv)
    window = AppMainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
