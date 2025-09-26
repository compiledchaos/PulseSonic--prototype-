from turtle import clear
from PySide6.QtCore import Qt, QRect
from PySide6.QtCore import Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QFrame, QLineEdit
import logging
from app.core.cache import SessionLocal, User_Info

logger = logging.getLogger(__name__)


class Login(QWidget):
    # Emitted when login succeeds with (username, password)
    login_success = Signal(str, str)

    redirect_to_signup = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("login_view")
        self.setEnabled(True)
        self.setAutoFillBackground(True)

        self.login_credentials = []

        # Login frame
        self.login_frame = QFrame(self)
        self.login_frame.setObjectName("login_frame")
        self.login_frame.setGeometry(QRect(0, 0, 600, 600))
        self.login_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.login_frame.setFrameShadow(QFrame.Shadow.Raised)

        # Login label
        self.login_label = QLabel(self)
        self.login_label.setObjectName("login_label")
        self.login_label.setGeometry(QRect(0, 40, 600, 100))
        font = QFont()
        font.setFamilies(["Brush Script MT"])
        font.setPointSize(50)
        self.login_label.setFont(font)
        self.login_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.login_label.setText("Login")

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

        # Login button
        self.login_button = QPushButton(self)
        self.login_button.setObjectName("login_button")
        self.login_button.setGeometry(QRect(0, 350, 600, 50))
        self.login_button.setText("Login")
        self.login_button.clicked.connect(self.login)

        # Sign Up button
        self.signup_button = QPushButton(self)
        self.signup_button.setObjectName("signup_button")
        self.signup_button.setGeometry(QRect(0, 450, 600, 50))
        self.signup_button.setText("Sign Up")
        self.signup_button.clicked.connect(self.redirect_to_sign_up)

    def login(self):
        self.username_input.setStyleSheet("clear")
        self.password_input.setStyleSheet("clear")
        self.signup_button.setStyleSheet("clear")
        username = self.username_input.text()
        password = self.password_input.text()
        if username and password:
            if self.check_user_exists(username):
                self.signup_button.setText("Sign Up")
                if self.check_password(username, password):
                    self.login_success.emit(username, password)
                else:
                    logger.error("Incorrect password")
                    self.password_input.setStyleSheet("border: 1px solid red;")
            else:
                logger.error("User does not exist")
                self.username_input.setStyleSheet("border: 1px solid red;")
                self.signup_button.setStyleSheet("border: 1px solid green;")
                self.signup_button.setText("New Here? Sign Up")
        else:
            logger.error("Please enter a username and password")
            self.username_input.setStyleSheet("border: 1px solid red;")
            self.password_input.setStyleSheet("border: 1px solid red;")

    def redirect_to_sign_up(self):
        self.redirect_to_signup.emit()

    def check_user_exists(self, username: str) -> bool:
        session = SessionLocal()
        user = session.query(User_Info).filter(User_Info.username == username).first()
        session.close()
        return user

    def check_password(self, username: str, password: str) -> bool:
        session = SessionLocal()
        user = session.query(User_Info).filter(User_Info.username == username).first()
        session.close()
        return user.password == password
