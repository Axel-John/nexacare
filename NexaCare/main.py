from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PySide6.QtCore import Qt, QEasingCurve, QPropertyAnimation
from views.choosing_window import ChoosingWindow
from views.login_window import LoginWindow
from views.create_account_window import CreateAccountWindow
from views.dashboard import Dashboard

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NexaCare")
        self.adjust_window_size()
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.show_choose_window()

    def adjust_window_size(self):
        # Maximize the window while keeping the navigation bar visible
        self.setWindowState(Qt.WindowMaximized)

        # Set minimum size constraints to ensure proper layout
        self.setMinimumSize(1100, 700)
        

    def show_choose_window(self):
        self.choose_window = ChoosingWindow()
        self.choose_window.proceed_signal.connect(self.show_login_window)
        self.stacked_widget.addWidget(self.choose_window)
        self.stacked_widget.setCurrentWidget(self.choose_window)

    def show_login_window(self, role):
        self.login_window = LoginWindow(role)
        self.login_window.create_account_signal.connect(self.show_create_account_window)
        self.login_window.login_success_signal.connect(self.show_dashboard)
        self.login_window.back_signal.connect(self.show_choose_window)
        self.stacked_widget.addWidget(self.login_window)
        self.animate_transition(self.choose_window, self.login_window)

    def show_create_account_window(self):
        self.create_account_window = CreateAccountWindow()
        self.create_account_window.login_window = self.login_window
        self.create_account_window.back_signal.connect(lambda: self.show_login_window(self.login_window.user_role))
        self.stacked_widget.addWidget(self.create_account_window)
        self.animate_transition(self.login_window, self.create_account_window)

    def show_dashboard(self, role):
        self.dashboard = Dashboard(role)
        self.dashboard.logout_signal.connect(self.show_choose_window)  # Navigate back to choosing window on log out
        self.stacked_widget.addWidget(self.dashboard)
        self.animate_transition(self.login_window, self.dashboard)

    def animate_transition(self, from_widget, to_widget):
        self.stacked_widget.setCurrentWidget(to_widget)
        animation = QPropertyAnimation(self.stacked_widget, b"geometry")
        animation.setDuration(500)
        animation.setStartValue(self.stacked_widget.geometry())
        animation.setEndValue(self.stacked_widget.geometry())
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.start()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
