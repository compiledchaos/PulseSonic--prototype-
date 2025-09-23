from PySide6.QtCore import Qt, QRect, QCoreApplication
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QLabel, QListWidget, QListWidgetItem


class RecsView(QWidget):
    """
    Encapsulates the Recommendations UI: header label and results list.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("recs_view")
        self.setEnabled(True)
        self.setAutoFillBackground(True)

        # Header label
        self.recs_label = QLabel(self)
        self.recs_label.setObjectName("recs_label")
        self.recs_label.setGeometry(QRect(0, 0, 600, 50))
        font7 = QFont()
        font7.setFamilies(["Brush Script MT"])
        font7.setPointSize(50)
        self.recs_label.setFont(font7)
        self.recs_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Results list
        self.recs_results = QListWidget(self)
        QListWidgetItem(self.recs_results)
        QListWidgetItem(self.recs_results)
        QListWidgetItem(self.recs_results)
        self.recs_results.setObjectName("recs_results")
        self.recs_results.setGeometry(QRect(75, 95, 440, 290))
        font3 = QFont()
        font3.setFamilies(["Rockwell"])
        font3.setPointSize(15)
        self.recs_results.setFont(font3)
        self.recs_results.setLineWidth(2)
        self.recs_results.setAlternatingRowColors(False)
        self.recs_results.setItemAlignment(Qt.AlignmentFlag.AlignLeading)

    def retranslateUi(self):
        self.recs_label.setText(QCoreApplication.translate("mainWindow", "Recommendations", None))

        __sortingEnabled = self.recs_results.isSortingEnabled()
        self.recs_results.setSortingEnabled(False)
        if self.recs_results.count() >= 3:
            self.recs_results.item(0).setText(
                QCoreApplication.translate("mainWindow", "rec test item-1", None)
            )
            self.recs_results.item(1).setText(
                QCoreApplication.translate("mainWindow", "rec test item-2", None)
            )
            self.recs_results.item(2).setText(
                QCoreApplication.translate("mainWindow", "rec test item-3", None)
            )
        self.recs_results.setSortingEnabled(__sortingEnabled)
