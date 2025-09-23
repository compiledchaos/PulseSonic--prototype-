# Third-party imports
from PySide6.QtCore import (
    Qt,
    QRect,
    QMetaObject,
    QCoreApplication,
)
from PySide6.QtGui import (
    QFont,
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QFrame,
    QLabel,
    QPushButton,
    QMenuBar,
    QStatusBar,
)

# Local application imports
# import images_rc  # Auto-generated resources file

# Import modular subviews
try:
    from .search import SearchView
    from .player import PlayerView
    from .recs import RecsView
except Exception:
    from app.ui.search import SearchView
    from app.ui.player import PlayerView
    from app.ui.recs import RecsView


class Ui_mainWindow(object):
    """
    Main window UI class for the PulseSonic application.

    This class handles the setup and configuration of the main application window,
    including all widgets, layouts, and visual elements.
    """

    def setupUi(self, mainWindow):
        """
        Initialize and set up the main window UI components.

        Args:
            mainWindow: The main window instance to set up
        """
        # Set main window properties
        if not mainWindow.objectName():
            mainWindow.setObjectName("mainWindow")
        mainWindow.resize(600, 600)
        mainWindow.setAutoFillBackground(False)
        # Create central widget and set as main window's central widget
        self.centralwidget = QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Application title label
        self.app_name = QLabel(self.centralwidget)
        self.app_name.setObjectName("app_name")
        self.app_name.setGeometry(QRect(0, 0, 600, 50))

        # Configure title font
        title_font = QFont()
        title_font.setFamilies(["Brush Script MT"])
        title_font.setPointSize(30)
        title_font.setBold(True)
        title_font.setItalic(False)
        title_font.setUnderline(False)
        title_font.setStrikeOut(False)
        title_font.setKerning(True)

        # Apply font and styling to title
        self.app_name.setFont(title_font)
        self.app_name.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.app_name.setAutoFillBackground(True)
        self.app_name.setFrameShape(QFrame.Shape.Box)
        self.app_name.setFrameShadow(QFrame.Shadow.Sunken)
        self.app_name.setTextFormat(Qt.TextFormat.RichText)
        self.app_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Create navigation bar widget
        self.three_funcs = QWidget(self.centralwidget)
        self.three_funcs.setObjectName("three_funcs")
        self.three_funcs.setGeometry(QRect(0, 55, 600, 51))
        self.three_funcs.setAutoFillBackground(True)

        # Configure button font
        button_font = QFont()
        button_font.setFamilies(["Segoe UI"])
        button_font.setPointSize(20)
        button_font.setBold(False)
        button_font.setItalic(False)

        # Search button
        self.search_button = QPushButton(self.three_funcs)
        self.search_button.setObjectName("search_button")
        self.search_button.setGeometry(QRect(6, 0, 150, 50))
        self.search_button.setFont(button_font)
        self.search_button.setAutoFillBackground(False)

        # Now Playing button
        self.playing_button = QPushButton(self.three_funcs)
        self.playing_button.setObjectName("playing_button")
        self.playing_button.setGeometry(QRect(162, 0, 175, 50))
        self.playing_button.setFont(button_font)
        self.playing_button.setAutoFillBackground(False)

        # Recommendations button
        self.recs_button = QPushButton(self.three_funcs)
        self.recs_button.setObjectName("recs_button")
        self.recs_button.setGeometry(QRect(343, 0, 250, 50))
        self.recs_button.setFont(button_font)
        self.recs_button.setAutoFillBackground(False)

        # Instantiate modular subviews
        self.search_view = SearchView(self.centralwidget)
        self.search_view.setGeometry(QRect(0, 110, 591, 431))

        self.playing_view = PlayerView(self.centralwidget)
        self.playing_view.setGeometry(QRect(0, 110, 591, 431))

        self.recs_view = RecsView(self.centralwidget)
        self.recs_view.setGeometry(QRect(0, 110, 591, 431))
        # Default visibility: show search, hide others
        self.search_view.show()
        self.playing_view.hide()
        self.recs_view.hide()
        mainWindow.setCentralWidget(self.centralwidget)
        self.playing_view.raise_()
        self.recs_view.raise_()
        self.search_view.raise_()
        self.app_name.raise_()
        self.three_funcs.raise_()
        self.menubar = QMenuBar(mainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 600, 33))
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainWindow)
        self.search_button.clicked.connect(self.search_view.show)
        self.playing_button.clicked.connect(self.playing_view.show)
        self.search_button.clicked.connect(self.playing_view.hide)
        self.playing_button.clicked.connect(self.search_view.hide)
        self.search_button.clicked.connect(self.recs_view.hide)
        self.playing_button.clicked.connect(self.recs_view.hide)
        self.recs_button.clicked.connect(self.recs_view.show)
        self.recs_button.clicked.connect(self.playing_view.hide)
        self.recs_button.clicked.connect(self.search_view.hide)

        QMetaObject.connectSlotsByName(mainWindow)

    # setupUi

    def retranslateUi(self, mainWindow):
        mainWindow.setWindowTitle(
            QCoreApplication.translate("mainWindow", "MainWindow", None)
        )
        self.app_name.setText(
            QCoreApplication.translate("mainWindow", "PulseSonic", None)
        )
        self.search_button.setText(
            QCoreApplication.translate("mainWindow", "Search", None)
        )
        self.playing_button.setText(
            QCoreApplication.translate("mainWindow", "Now Playing", None)
        )
        self.recs_button.setText(
            QCoreApplication.translate("mainWindow", "Recommendations", None)
        )
        # Delegate translation to subviews
        self.search_view.retranslateUi()
        self.playing_view.retranslateUi()
        self.recs_view.retranslateUi()

    # retranslateUi
