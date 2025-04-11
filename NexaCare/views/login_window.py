from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton, QInputDialog, QMessageBox
from PySide6.QtCore import Qt, QMargins, Signal, QTimer
from PySide6.QtGui import QFont, QFontDatabase, QMovie
import hashlib
from models.database import Database  # Import the Database class

class LoginWindow(QWidget):
    create_account_signal = Signal()
    login_success_signal = Signal(str)
    back_signal = Signal()

    def __init__(self, user_role="User"):
        super().__init__()
        self.setWindowTitle("Login")
        self.user_role = user_role
        self.database = Database()
        self.setup_ui()

    def setup_ui(self):
        # Load the Poppins font
        font_id = QFontDatabase.addApplicationFont("L:/MYOLIE/NexaCare/assets/static/Poppins-SemiBold.ttf")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0] if font_id != -1 else "Poppins"

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        # White background frame
        white_frame = QFrame()
        white_frame.setStyleSheet("background-color: white;")
        white_frame.setFrameShape(QFrame.NoFrame)

        white_layout = QVBoxLayout()
        white_layout.setContentsMargins(0, 0, 0, 0)
        white_layout.setAlignment(Qt.AlignCenter)
        white_frame.setLayout(white_layout)

        # Centering container horizontally
        container_wrapper = QHBoxLayout()
        container_wrapper.setAlignment(Qt.AlignCenter)
        container_wrapper.setContentsMargins(50, 50, 50, 50)

        # Main container
        container = QFrame()
        container.setFixedSize(1000, 600)
        container.setStyleSheet("background: white;")

        container_layout = QHBoxLayout()
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        # Left section with GIF
        left_section = QFrame()
        left_section.setFixedWidth(500)
        gif_label = QLabel(left_section)
        gif_label.setAlignment(Qt.AlignCenter)
        gif_label.setStyleSheet("background-color: #dbecff;")
        gif_label.setGeometry(0, 0, 500, 600)

        movie = QMovie("assets/gifs/left_section_login.gif")
        movie.setCacheMode(QMovie.CacheAll)
        movie.setScaledSize(gif_label.size())
        gif_label.setMovie(movie)
        movie.start()

        left_section_layout = QVBoxLayout(left_section)
        left_section_layout.addWidget(gif_label)
        left_section_layout.setContentsMargins(0, 0, 0, 0)
        left_section_layout.setAlignment(Qt.AlignCenter)

        # Right section - Light Blue
        right_section = QFrame()
        right_section.setStyleSheet("background-color: #3b8eed;")
        right_section.setFixedWidth(500)

        # === ADD WELCOME TEXT ===
        welcome_label = QLabel(f"Welcome, {self.user_role}!")
        welcome_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        welcome_label.setStyleSheet("color: white;")
        welcome_label.setFont(QFont(font_family, 25, QFont.Bold))  # Poppins Bold

        # === ADD USERNAME & PASSWORD FIELDS ===
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("User ID")
        self.username_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: white;
                border: 2px solid transparent;
                border-radius: 15px;
                padding: 10px;
                font-size: 16px;
                font-family: '{font_family}';
                color: black;
            }}
            QLineEdit:hover {{
                border: 2px solid #0056b3;
            }}
            QLineEdit:focus {{
                border: 2px solid #0056b3;
            }}
        """)
        self.username_input.setFixedWidth(350)
        self.username_input.setFixedHeight(50)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: white;
                border: 2px solid transparent;
                border-radius: 15px;
                padding: 10px;
                font-size: 16px;
                font-family: '{font_family}';
                color: black;
            }}
            QLineEdit:hover {{
                border: 2px solid #0056b3;
            }}
            QLineEdit:focus {{
                border: 2px solid #0056b3;
            }}
        """)
        self.password_input.setFixedWidth(350)

        # Optimize password input handling to reduce lag
        self.password_input.textChanged.connect(self.handle_password_input)

        # Error message labels
        self.username_error_label = QLabel("")
        self.username_error_label.setStyleSheet("""
            QLabel {
                color: red;
                font-size: 12px;
                font-family: 'Poppins';
            }
        """)
        self.username_error_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.username_error_label.setFixedHeight(15)  # Set a fixed height to avoid layout disruption

        self.password_error_label = QLabel("")
        self.password_error_label.setStyleSheet("""
            QLabel {
                color: red;
                font-size: 12px;
                font-family: 'Poppins';
            }
        """)
        self.password_error_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.password_error_label.setFixedHeight(15)  # Set a fixed height to avoid layout disruption

        # Timer for clearing error messages
        self.error_timer = QTimer()
        self.error_timer.setSingleShot(True)
        self.error_timer.timeout.connect(self.clear_error_messages)

        # === ADD BUTTONS ===
        login_button = QPushButton("Log In")
        login_button.setFixedSize(350, 50)
        login_button.setStyleSheet(f"""
            QPushButton {{
                background-color: #0056b3;
                color: white;
                border-radius: 15px;
                font-size: 16px;
                font-family: '{font_family}';
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #004094;
            }}
        """)
        login_button.clicked.connect(self.check_credentials)

        create_account_button = QPushButton("Create Account")
        create_account_button.setFixedSize(350, 50)
        create_account_button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: white;
                border: 2px solid white;
                border-radius: 15px;
                font-size: 16px;
                font-family: '{font_family}';
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: rgba(255, 255, 255, 0.2);
            }}
        """)
        create_account_button.clicked.connect(self.on_create_account)

        # Add back button
        back_button = QPushButton("Back")
        back_button.setFixedSize(100, 50)
        back_button.setStyleSheet(f"""
            QPushButton {{
                background-color: #f0f0f0;
                color: black;
                border-radius: 15px;
                font-size: 16px;
                font-family: '{font_family}';
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #d6d6d6;
            }}
        """)
        back_button.clicked.connect(self.on_back)

        # === ADD FORGOT PASSWORD BUTTON ===
        forgot_password_button = QPushButton("Forgot Password?")
        forgot_password_button.setFixedSize(350, 40)
        forgot_password_button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: white;
                font-size: 14px;
                font-family: '{font_family}';
                text-decoration: underline;
                border: none;
            }}
            QPushButton:hover {{
                color: #d6d6d6;
            }}
        """)
        forgot_password_button.clicked.connect(self.on_forgot_password)

        # Layout for input fields and buttons
        input_layout = QVBoxLayout()
        input_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        input_layout.setContentsMargins(70, 20, 0, 0)

        # Username field with error label
        username_layout = QVBoxLayout()
        username_layout.setSpacing(0)  # Remove extra spacing
        username_layout.addWidget(self.username_input)
        username_layout.addWidget(self.username_error_label)
        input_layout.addLayout(username_layout)

        input_layout.addSpacing(20)

        # Password field with error label
        password_layout = QVBoxLayout()
        password_layout.setSpacing(0)  # Remove extra spacing
        password_layout.addWidget(self.password_input)
        password_layout.addWidget(self.password_error_label)
        input_layout.addLayout(password_layout)

        input_layout.addSpacing(30)
        input_layout.addWidget(login_button)
        input_layout.addSpacing(10)
        input_layout.addWidget(create_account_button)
        input_layout.addSpacing(10)
        input_layout.addWidget(back_button)
        input_layout.addWidget(forgot_password_button, alignment=Qt.AlignCenter)

        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(QMargins(0, 100, 100, 0))
        right_layout.setAlignment(Qt.AlignTop)
        right_layout.addWidget(welcome_label)
        right_layout.addLayout(input_layout)

        right_section.setLayout(right_layout)
        container_layout.addWidget(left_section)
        container_layout.addWidget(right_section)
        container.setLayout(container_layout)

        container_wrapper.addWidget(container)
        white_layout.addLayout(container_wrapper)

        main_layout.addWidget(white_frame)

        self.setLayout(main_layout)

    def on_create_account(self):
        self.create_account_signal.emit()

    def check_credentials(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        # Clear previous error messages
        self.clear_error_messages()

        if not username or not password:
            if not username:
                self.username_error_label.setText("Username is required.")
            if not password:
                self.password_error_label.setText("Password is required.")
            self.error_timer.start(2000)
            return

        try:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            self.database.cursor.execute(
                "SELECT password FROM accounts WHERE username = ?",
                (username,)
            )
            result = self.database.cursor.fetchone()

            if result:
                stored_password = result[0]
                if stored_password == hashed_password:
                    self.clear_error_messages()  # Clear error messages on success
                    self.login_success_signal.emit(self.user_role)
                else:
                    self.password_error_label.setText("Invalid password.")
                    self.error_timer.start(1000)  # Start timer to clear messages after 1000ms
            else:
                self.username_error_label.setText("Invalid username.")
                self.error_timer.start(1000)  # Start timer to clear messages after 1000ms
        except Exception as e:
            self.username_error_label.setText(f"Error: {e}")
            self.error_timer.start(1000)  # Start timer to clear messages after 1000ms

    def clear_error_messages(self):
        """ Clear the error messages for username and password. """
        self.username_error_label.setText("")
        self.password_error_label.setText("")

    def register_user(self, username, password):
        try:
            self.database.add_user(username, password, self.user_role)
            print(f"User {username} registered with role {self.user_role}.")
        except Exception as e:
            print(f"Error registering user: {e}")

    def on_back(self):
        self.back_signal.emit()

    def on_forgot_password(self):
        """ Handle the forgot password mechanism. """
        username, ok = QInputDialog.getText(self, "Forgot Password", "Enter your username (e.g., 2025D0001):")
        if ok and username.strip():
            new_password, ok = QInputDialog.getText(self, "Reset Password", "Enter your new password:", QLineEdit.Password)
            if ok and new_password.strip():
                try:
                    hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
                    self.database.cursor.execute(
                        "UPDATE accounts SET password = ? WHERE username = ?",
                        (hashed_password, username.strip())
                    )
                    if self.database.cursor.rowcount > 0:
                        self.database.connection.commit()
                        QMessageBox.information(self, "Success", "Password updated successfully!")
                    else:
                        QMessageBox.warning(self, "Error", "Username not found.")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to update password: {e}")

    def handle_password_input(self):
        # Debounce the input handling to avoid processing on every keystroke
        if hasattr(self, '_password_timer') and self._password_timer.isActive():
            self._password_timer.stop()

        self._password_timer = QTimer(self)
        self._password_timer.setSingleShot(True)
        self._password_timer.timeout.connect(self.process_password_input)
        self._password_timer.start(300)  # Delay processing by 300ms

    def process_password_input(self):
        # Perform any necessary processing for the password input
        password = self.password_input.text()
        # ...existing logic for password validation or handling...