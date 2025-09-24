from PySide6.QtCore import Qt, QRect, QCoreApplication
from PySide6.QtGui import QFont, QPalette, QBrush, QColor, QPixmap, QImage
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QProgressBar
import requests


class PlayerView(QWidget):
    """
    Encapsulates the Now Playing UI: track name, cover art, transport controls,
    progress bar, and artist name.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.url = ""
        self.setObjectName("playing_view")
        self.setEnabled(True)
        self.setAutoFillBackground(True)

        # Track name label
        self.track_name = QLabel(self)
        self.track_name.setObjectName("track_name")
        self.track_name.setGeometry(QRect(0, 0, 600, 50))
        font5 = QFont()
        font5.setFamilies(["Brush Script MT"])
        font5.setPointSize(50)
        font5.setItalic(False)
        self.track_name.setFont(font5)
        self.track_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Cover art frame
        self.cover_art = QLabel(self)
        self.cover_art.setObjectName("cover_art")
        self.cover_art.setGeometry(QRect(150, 60, 300, 300))
        self.cover_art.setScaledContents(True)
        self.cover_art.hide()

        # Load cover art if URL was preset

        if self.url:
            self.set_cover_url(self.url)

        # Progress bar
        self.progressBar = QProgressBar(self)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setGeometry(QRect(150, 360, 300, 50))
        palette2 = QPalette()
        brush3 = QBrush(QColor(0, 0, 255, 255))
        brush3.setStyle(Qt.BrushStyle.SolidPattern)
        # if QT_VERSION >= QT_VERSION_CHECK(6, 6, 0)
        palette2.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Accent, brush3)
        # endif
        # if QT_VERSION >= QT_VERSION_CHECK(6, 6, 0)
        palette2.setBrush(
            QPalette.ColorGroup.Inactive, QPalette.ColorRole.Accent, brush3
        )
        # endif
        # if QT_VERSION >= QT_VERSION_CHECK(6, 6, 0)
        palette2.setBrush(
            QPalette.ColorGroup.Disabled, QPalette.ColorRole.Accent, brush3
        )
        # endif
        self.progressBar.setPalette(palette2)
        self.progressBar.setValue(24)
        self.progressBar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progressBar.setTextVisible(False)
        self.progressBar.setOrientation(Qt.Orientation.Horizontal)
        self.progressBar.setInvertedAppearance(False)

        # Artist name label
        self.artist_name = QLabel(self)
        self.artist_name.setObjectName("artist_name")
        self.artist_name.setGeometry(QRect(0, 390, 600, 50))
        font6 = QFont()
        font6.setFamilies(["Script MT"])
        font6.setPointSize(20)
        self.artist_name.setFont(font6)
        self.artist_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Pause and Play buttons
        self.pause = QPushButton(self)
        self.pause.setObjectName("play")
        self.pause.setGeometry(QRect(483, 210, 80, 25))

        self.play = QPushButton(self)
        self.play.setObjectName("pause")
        self.play.setGeometry(QRect(37, 210, 79, 24))

    def set_cover_url(self, url: str):
        """
        Set or update the cover art from an image URL.

        Args:
            url: Direct URL to the image to display.
        """
        self.url = url or ""
        if not self.url:
            self.cover_art.clear()
            self.cover_art.hide()
            return

        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            img = QImage()
            img.loadFromData(response.content)
            if img.isNull():
                # Failed to decode
                self.cover_art.clear()
                self.cover_art.hide()
                return
            self.cover_art.setPixmap(QPixmap.fromImage(img))
            self.cover_art.show()
        except Exception:
            # Network or decoding error; hide the image
            self.cover_art.clear()
            self.cover_art.hide()

    def retranslateUi(self):
        self.track_name.setText(QCoreApplication.translate("mainWindow", "Track", None))
        self.pause.setText(QCoreApplication.translate("mainWindow", "Play", None))
        self.play.setText(QCoreApplication.translate("mainWindow", "Pause", None))
        self.artist_name.setText(
            QCoreApplication.translate("mainWindow", "Artist Name", None)
        )
