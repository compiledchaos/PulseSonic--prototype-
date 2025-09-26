from PySide6.QtCore import Qt, QRect
from PySide6.QtCore import Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QFrame, QLineEdit
import logging
from app.core.cache import SessionLocal, User_Info

logger = logging.getLogger(__name__)


class Signup(QWidget):
    # Emitted when signup succeeds with (username, password)
    signup_success = Signal(str, str)
    redirect_to_login_view = Signal()

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

        # Redirect to login button
        self.redirect_to_login = QPushButton(self)
        self.redirect_to_login.setObjectName("redirect_to_login")
        self.redirect_to_login.setGeometry(QRect(0, 450, 600, 50))
        self.redirect_to_login.setText("Already have an account? Login")
        self.redirect_to_login.clicked.connect(self.to_login)

        self.redirect_to_login.hide()

    def to_login(self):
        self.redirect_to_login_view.emit()

    def signup(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if username and password:
            if self.check_user_exists(username):
                logger.error("User already exists")
                self.username_input.setStyleSheet("border: 1px solid red;")
                self.redirect_to_login.setStyleSheet("border: 1px solid green;")
                self.redirect_to_login.show()
            else:
                self.add_user(username, password)
                # Emit custom signal indicating signup success
                self.signup_success.emit(username, password)
        else:
            logger.error("Please enter a username and password")
            self.username_input.setStyleSheet("border: 1px solid red;")
            self.password_input.setStyleSheet("border: 1px solid red;")

    def check_user_exists(self, username):
        session = SessionLocal()
        user = session.query(User_Info).filter(User_Info.username == username).first()
        session.close()
        return user

    def add_user(self, username, password):
        session = SessionLocal()
        user = User_Info(username=username, password=password)
        session.add(user)
        session.commit()
        session.close()
