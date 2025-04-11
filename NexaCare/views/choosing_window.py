from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFrame
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QSize, Qt, Signal
from PySide6.QtGui import QIcon

class AnimatedButton(QPushButton):
    def __init__(self, text, icon_path):
        super().__init__(text)
        self.setFixedSize(250, 250)
        self.setCheckable(True)  # Toggle button behavior

        # Set icon
        self.setIcon(QIcon(icon_path))
        self.setIconSize(QSize(80, 80))  # Adjust icon size

        self.setStyleSheet("""
            QPushButton {
                background-color: #9dd1ed;
                border-radius: 30px;
                font-size: 20px;
                font-weight: bold;
                color: black;
                margin: 0;
                padding: 0;
                border: none;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #8cc1dc;
            }
            QPushButton:checked {
                background-color: #3b8eed;
                color: white;
            }
        """)

        # Animation for scaling effect
        self.size_animation = QPropertyAnimation(self, b"minimumSize")
        self.size_animation.setEasingCurve(QEasingCurve.OutQuad)
        self.size_animation.setDuration(200)  # 200ms smooth transition

    def enterEvent(self, event):
        self.animate_size(QSize(270, 270))  # Grow to 270x270 on hover
        super().enterEvent(event)

    def leaveEvent(self, event):
        if not self.isChecked():
            self.animate_size(QSize(250, 250))  # Shrink back to 250x250
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.animate_size(QSize(270, 270))  # Keep enlarged size
        super().mousePressEvent(event)

    def animate_size(self, target_size):
        """ Animates the button resizing while keeping position fixed. """
        self.size_animation.stop()
        self.size_animation.setStartValue(self.minimumSize())
        self.size_animation.setEndValue(target_size)
        self.size_animation.start()


class ChoosingWindow(QWidget):
    proceed_signal = Signal(str)  # Signal to notify when proceed button is clicked

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Choose User")
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        # White background frame
        white_frame = QFrame()
        white_frame.setAutoFillBackground(True)
        white_frame.setFrameShape(QFrame.NoFrame)
        white_frame.setStyleSheet("background-color: white;")

        white_layout = QVBoxLayout()
        white_layout.setContentsMargins(0, 0, 0, 0)
        white_frame.setLayout(white_layout)

        main_layout.addWidget(white_frame)

        # Container for buttons and proceed button
        button_container = QVBoxLayout()
        button_container.setSpacing(30)  # Adjust spacing between buttons and proceed button
        button_container.setAlignment(Qt.AlignCenter)

        # Horizontal layout for buttons
        box_layout = QHBoxLayout()
        box_layout.setSpacing(10)
        box_layout.setContentsMargins(0, 0, 0, 0)
        box_layout.setAlignment(Qt.AlignCenter)  # Center align the buttons

        container = QWidget()
        container.setFixedSize(3 * 270 + 2 * 80, 300)  # Increase width & add height
        container_layout = QHBoxLayout()
        container_layout.setSpacing(25)  # Increase spacing
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setAlignment(Qt.AlignCenter)  # Keep it centered

        self.buttons = []
        self.selected_role = None
        labels_and_icons = [
            {"label": "HR", "icon": "assets/icons/recepicon.png"},
            {"label": "Doctor", "icon": "assets/icons/doctor_logo.png"}
        ]

        for item in labels_and_icons:
            button = AnimatedButton(item["label"], item["icon"])
            button.clicked.connect(lambda checked, b=button, l=item["label"]: self.set_active_button(b, l))
            self.buttons.append(button)
            container_layout.addWidget(button)

        container.setLayout(container_layout)
        box_layout.addWidget(container)

        button_container.addLayout(box_layout)

        # Proceed button (below the 3 buttons)
        self.proceed_button = QPushButton("Proceed")
        self.proceed_button.setFixedSize(200, 60)
        self.proceed_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                font-size: 18px;
                font-weight: bold;
                color: black;
                border: 2px solid black;
                border-radius: 30px;
            }
            QPushButton:hover {
                background-color: #8cc1dc;
            }
        """)
        self.proceed_button.clicked.connect(self.on_proceed)

        button_container.addWidget(self.proceed_button, alignment=Qt.AlignCenter)

        white_layout.addLayout(button_container)
        self.setLayout(main_layout)

    def set_active_button(self, clicked_button, role):
        """ Ensures only one button stays active at a time and stores the selected role. """
        self.selected_role = role
        for button in self.buttons:
            button.setChecked(button == clicked_button)
            if button == clicked_button:
                button.animate_size(QSize(270, 270))  # Keep it enlarged
            else:
                button.animate_size(QSize(250, 250))  # Return others to normal

    def on_proceed(self):
        """ Emit signal to navigate to the login window when the proceed button is clicked. """
        if self.selected_role:
            self.proceed_signal.emit(self.selected_role)
        else:
            print("No role selected.")