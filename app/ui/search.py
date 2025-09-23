from PySide6.QtCore import Qt, QRect, QCoreApplication
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QLabel


class SearchView(QWidget):
    """
    Encapsulates the Search UI: search bar, search button, results label and list.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("search_view")
        self.setEnabled(True)
        self.setAcceptDrops(False)
        self.setAutoFillBackground(True)

        # Search bar
        self.search_bar = QLineEdit(self)
        self.search_bar.setObjectName("search_bar")
        self.search_bar.setGeometry(QRect(75, 50, 361, 30))
        self.search_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Search button
        self.search_b = QPushButton(self)
        self.search_b.setObjectName("search_b")
        self.search_b.setGeometry(QRect(436, 50, 80, 32))
        font2 = QFont()
        font2.setFamilies(["Segoe Print"])
        font2.setPointSize(13)
        self.search_b.setFont(font2)

        # Search results list
        self.search_results = QListWidget(self)
        QListWidgetItem(self.search_results)
        QListWidgetItem(self.search_results)
        QListWidgetItem(self.search_results)
        self.search_results.setObjectName("search_results")
        self.search_results.setGeometry(QRect(75, 140, 441, 291))
        font3 = QFont()
        font3.setFamilies(["Rockwell"])
        font3.setPointSize(15)
        self.search_results.setFont(font3)
        self.search_results.setLineWidth(2)
        self.search_results.setAlternatingRowColors(False)
        self.search_results.setItemAlignment(Qt.AlignmentFlag.AlignLeading)

        # Results label
        self.label = QLabel(self)
        self.label.setObjectName("label")
        self.label.setGeometry(QRect(75, 100, 101, 40))
        font4 = QFont()
        font4.setFamilies(["Segoe Print"])
        font4.setPointSize(20)
        self.label.setFont(font4)

    def retranslateUi(self):
        # Translate/search UI text and populate demo items
        self.search_b.setText(QCoreApplication.translate("mainWindow", "Search", None))
        self.label.setText(QCoreApplication.translate("mainWindow", "Results: ", None))

        __sortingEnabled = self.search_results.isSortingEnabled()
        self.search_results.setSortingEnabled(False)
        if self.search_results.count() >= 3:
            self.search_results.item(0).setText(
                QCoreApplication.translate("mainWindow", "test item-1", None)
            )
            self.search_results.item(1).setText(
                QCoreApplication.translate("mainWindow", "test item-2", None)
            )
            self.search_results.item(2).setText(
                QCoreApplication.translate("mainWindow", "test item-3", None)
            )
        self.search_results.setSortingEnabled(__sortingEnabled)
