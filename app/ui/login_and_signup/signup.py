from PySide6.QtCore import Qt, QRect
from PySide6.QtCore import Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QFrame, QLineEdit
import logging

logger = logging.getLogger(__name__)


class Signup(QWidget):
    # Emitted when signup succeeds with (username, password)
    signup_success = Signal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("signup_view")
        self.setEnabled(True)
        self.setAutoFillBackground(True)

        self.signup_credentials = []

        # Sign Up frame
        self.signup_frame = QFrame(self)
        self.signup_frame.setObjectName("signup_frame")
        self.signup_frame.setGeometry(QRect(0, 0, 600, 600))
        self.signup_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.signup_frame.setFrameShadow(QFrame.Shadow.Raised)

        # Sign Up label
        self.signup_label = QLabel(self)
        self.signup_label.setObjectName("signup_label")
        self.signup_label.setGeometry(QRect(0, 50, 600, 50))
        font = QFont()
        font.setFamilies(["Brush Script MT"])
        font.setPointSize(50)
        self.signup_label.setFont(font)
        self.signup_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.signup_label.setText("Sign Up")

        # Username input
        self.username_input = QLineEdit(self)
        self.username_input.setObjectName("username_input")
        self.username_input.setGeometry(QRect(0, 150, 600, 50))
        self.username_input.setPlaceholderText("Username")
        self.username_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.username_input.setMaxLength(20)
        self.username_input.setEchoMode(QLineEdit.EchoMode.Normal)

        # Password input
        self.password_input = QLineEdit(self)
        self.password_input.setObjectName("password_input")
        self.password_input.setGeometry(QRect(0, 250, 600, 50))
        self.password_input.setPlaceholderText("Password")
        self.password_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.password_input.setMaxLength(20)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Sign Up button
        self.signup_button = QPushButton(self)
        self.signup_button.setObjectName("signup_button")
        self.signup_button.setGeometry(QRect(0, 350, 600, 50))
        self.signup_button.setText("Sign Up")
        self.signup_button.clicked.connect(self.signup)

    def signup(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if username and password:
            self.signup_credentials.append((username, password))
            # Emit custom signal indicating signup success
            self.signup_success.emit(username, password)
        else:
            logger.error("Please enter a username and password")
