import sys
from PySide6.QtWidgets import QApplication
from app.ui.app_ui import AppMainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppMainWindow()
    window.show()
    sys.exit(app.exec())
