from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt, QMargins, Signal
from PySide6.QtGui import QColor, QFont, QFontDatabase, QMovie
from models.database import Database

class LoginWindow(QWidget):
    def __init__(self, user_role="User"):  # Default role is "User"
        super().__init__()
        self.setWindowTitle("Login")
        self.user_role = user_role  # Store selected role
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

        # Left section - Ghost White
        left_section = QFrame()
        left_section.setStyleSheet("background-color: #dbecff;")
        left_section.setFixedWidth(500)

        # Right section - Light Blue
        right_section = QFrame()
        right_section.setStyleSheet("background-color: #3b8eed;")
        right_section.setFixedWidth(500)

        # === ADD WELCOME TEXT ===
        welcome_label = QLabel(f"Welcome, {self.user_role}!")
        welcome_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        welcome_label.setStyleSheet("color: white;")
        welcome_label.setFont(QFont(font_family, 25, QFont.Bold))

        # === ADD USERNAME & PASSWORD FIELDS ===
        username_input = QLineEdit()
        username_input.setPlaceholderText("User ID")
        username_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 2px solid transparent;
                border-radius: 15px;
                padding: 10px;
                font-size: 16px;
                color: black;
                transition: border 0.3s ease-in-out;
            }
            QLineEdit:hover {
                border: 2px solid #0056b3;
            }
        """)
        username_input.setFixedWidth(350)
        username_input.setFixedHeight(50)

        password_input = QLineEdit()
        password_input.setPlaceholderText("Password")
        password_input.setEchoMode(QLineEdit.Password)
        password_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 2px solid transparent;
                border-radius: 15px;
                padding: 10px;
                font-size: 16px;
                color: black;
                transition: border 0.3s ease-in-out;
            }
            QLineEdit:hover {
                border: 2px solid #0056b3;
            }
        """)
        password_input.setFixedWidth(350)

        # === ADD BUTTONS ===
        login_button = QPushButton("Log In")
        login_button.setFixedSize(350, 50)
        login_button.setStyleSheet("""
            QPushButton {
                background-color: #0056b3;
                color: white;
                border-radius: 15px;
                font-size: 16px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #004094;
            }
        """)

        create_account_button = QPushButton("Create Account")
        create_account_button.setFixedSize(350, 50)
        create_account_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: 2px solid white;
                border-radius: 15px;
                font-size: 16px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)

        # Layout for input fields and buttons
        input_layout = QVBoxLayout()
        input_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        input_layout.setContentsMargins(70, 20, 0, 0)
        input_layout.addWidget(username_input)
        input_layout.addSpacing(20)
        input_layout.addWidget(password_input)
        input_layout.addSpacing(30)
        input_layout.addWidget(login_button)  # Add login button
        input_layout.addSpacing(10)
        input_layout.addWidget(create_account_button)  # Add create account button

        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(QMargins(0, 100, 100, 0))  # Adjust position
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

class CreateAccountWindow(QWidget):
    back_signal = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create Account")
        self.setup_ui()
        self.database = Database()

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
        welcome_label = QLabel("Create Your Account")
        welcome_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        welcome_label.setStyleSheet("color: white;")
        welcome_label.setFont(QFont(font_family, 25, QFont.Bold))  # Poppins Bold

        # === ADD NAME, PASSWORD & CONFIRM PASSWORD FIELDS ===
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name")
        self.name_input.setStyleSheet(f"""
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
        self.name_input.setFixedWidth(350)
        self.name_input.setFixedHeight(50)

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
                transition: border 0.3s ease-in-out;
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

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm Password")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setStyleSheet(f"""
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
        self.confirm_password_input.setFixedWidth(350)

        # === ADD BUTTONS ===
        create_account_button = QPushButton("Create Account")
        create_account_button.setFixedSize(350, 50)
        create_account_button.setStyleSheet(f"""
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
        create_account_button.clicked.connect(self.create_account)

        login_button = QPushButton("Login")
        login_button.setFixedSize(350, 50)
        login_button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: #0056b3;
                border: 2px solid #0056b3;
                border-radius: 15px;
                font-size: 16px;
                font-family: '{font_family}';
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: rgba(0, 86, 179, 0.1);
            }}
        """)
        login_button.clicked.connect(self.on_back)

        back_button = QPushButton("Back", self)
        back_button.setFixedSize(100, 40)
        back_button.setStyleSheet(f"""
            QPushButton {{
                background-color: #3b8eed;
                color: white;
                border-radius: 10px;
                font-size: 14px;
                font-family: '{font_family}';
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #0056b3;
            }}
        """)
        back_button.clicked.connect(self.on_back)
        back_button.move(20, 20)

        # Layout for input fields and buttons
        input_layout = QVBoxLayout()
        input_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        input_layout.setContentsMargins(70, 20, 0, 0)
        input_layout.addWidget(self.name_input)
        input_layout.addSpacing(20)
        input_layout.addWidget(self.password_input)
        input_layout.addSpacing(20)
        input_layout.addWidget(self.confirm_password_input)
        input_layout.addSpacing(30)
        input_layout.addWidget(create_account_button)
        input_layout.addSpacing(10)
        input_layout.addWidget(login_button)

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

    def on_back(self):
        self.back_signal.emit()

    def create_account(self):
        name = self.name_input.text().strip()
        password = self.password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()

        if not name or not password or not confirm_password:
            QMessageBox.warning(self, "Error", "All fields are required!")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match!")
            return

        try:
            role = self.login_window.user_role.lower()
            username = self.database.add_user(name, password, role)
            QMessageBox.information(
                self, "Success",
                f"Account created successfully!\nYour username is: {username}"
            )
        except ValueError as ve:
            QMessageBox.warning(self, "Error", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create account: {e}")