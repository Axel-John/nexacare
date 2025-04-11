from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QRect, QEasingCurve
from PySide6.QtGui import QPixmap, QFont, QFontDatabase

class LoadingScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Loading...")
        self.setWindowState(Qt.WindowFullScreen)  # Make the loading screen full screen
        self.setStyleSheet("background-color: #3b8eed;")  # Light blue background
        self.setup_ui()

    def setup_ui(self):
        # Load the Poppins font
        font_id = QFontDatabase.addApplicationFont("L:/MYOLIE/NexaCare/assets/static/Poppins-SemiBold.ttf")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0] if font_id != -1 else "Poppins"

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(20)
        main_layout.setAlignment(Qt.AlignCenter)

        # Logo
        logo_label = QLabel()
        logo_label.setPixmap(QPixmap("assets/icons/logo.png").scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignCenter)

        # Loading text
        loading_text = QLabel("Loading NexaCare...")
        loading_text.setAlignment(Qt.AlignCenter)
        loading_text.setStyleSheet("color: white;")
        loading_text.setFont(QFont(font_family, 24, QFont.Bold))

        # Circular loading animation
        self.loading_circle = QLabel()
        self.loading_circle.setFixedSize(100, 100)
        self.loading_circle.setStyleSheet("""
            QLabel {
                border: 5px solid #dbecff;  /* Ghost white */
                border-top: 5px solid #0056b3;  /* Dark blue */
                border-radius: 50px;
            }
        """)

        # Animation for the circle
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.rotate_circle)
        self.rotation_angle = 0
        self.animation_timer.start(50)  # Rotate every 50ms

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(40)
        self.progress_bar.setFixedWidth(600)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #dbecff;  /* Ghost white */
                border: none;
                border-radius: 20px;
                text-align: center;
                font-size: 16px;
                color: black;
                font-family: 'Poppins';
            }
            QProgressBar::chunk {
                background-color: #0056b3;  /* Dark blue */
                border-radius: 20px;
            }
        """)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        # Add widgets to layout
        main_layout.addWidget(logo_label)
        main_layout.addWidget(self.loading_circle, alignment=Qt.AlignCenter)
        main_layout.addWidget(loading_text)
        main_layout.addWidget(self.progress_bar)  # Add progress bar to the layout

        self.setLayout(main_layout)

        # Timer to simulate loading
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(100)  # Update every 100ms

    def update_progress(self):
        """ Update the progress bar value. """
        value = self.progress_bar.value()
        if value < 100:
            self.progress_bar.setValue(value + 2)  # Increment by 2 for smoother progress
        else:
            self.timer.stop()
            self.close()  # Close the loading screen when done

    def rotate_circle(self):
        """ Rotate the circular loading animation. """
        self.rotation_angle += 10
        self.loading_circle.setStyleSheet(f"""
            QLabel {{
                border: 5px solid #dbecff;  /* Ghost white */
                border-top: 5px solid #0056b3;  /* Dark blue */
                border-radius: 50px;
                transform: rotate({self.rotation_angle}deg);
            }}
        """)
