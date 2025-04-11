from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, 
                               QPushButton, QStackedWidget)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QPixmap, QIcon, QColor

class Dashboard(QWidget):
    logout_signal = Signal()

    def __init__(self, role):
        super().__init__()
        self.setWindowTitle("Dashboard")
        self.role = role
        self.nav_buttons = []
        self.setup_ui()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create sidebar and content area
        self.sidebar = self.create_sidebar()
        self.content_area = self.create_content_area()

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content_area, stretch=1)

    def create_sidebar(self):
        # Create the sidebar container
        sidebar = QFrame()
        sidebar.setFixedWidth(80)
        sidebar.setStyleSheet("background-color: #3b8eed;")
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(20)

        # Add logo
        logo_label = QLabel()
        logo_label.setPixmap(QPixmap("assets/icons/logo.png").scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignCenter)
        
        logo_container = QFrame()
        logo_container.setFixedHeight(80)
        logo_container.setStyleSheet("background-color: transparent;")
        
        logo_layout = QHBoxLayout(logo_container)
        logo_layout.setContentsMargins(10, 10, 10, 10)
        logo_layout.addWidget(logo_label)
        
        sidebar_layout.addWidget(logo_container)
        sidebar_layout.addSpacing(50)

        # Create navigation buttons
        nav_container = QFrame()
        nav_container.setStyleSheet("background-color: transparent;")
        
        nav_layout = QVBoxLayout(nav_container)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(30)

        # Define navigation items
        nav_items = [
            {"icon": "assets/icons/bxs-dashboard.svg", "tooltip": "Dashboard", "tab": "dashboard_tab"},
            {"icon": "assets/icons/bxs-group.svg", "tooltip": "Patients", "tab": "patients_tab"},
            {"icon": "assets/icons/bxs-calendar.svg", "tooltip": "Appointments", "tab": "appointments_tab"},
            {"icon": "assets/icons/bxs-cog.svg", "tooltip": "Settings", "tab": "settings_tab"},
        ]

        # Create navigation buttons
        for item in nav_items:
            button = self.create_nav_button(item["icon"], item["tooltip"], item["tab"])
            if item["tab"] == "dashboard_tab":
                button.setStyleSheet(button.styleSheet().replace("transparent", "white"))
                
            self.nav_buttons.append(button)
            nav_layout.addWidget(button, alignment=Qt.AlignCenter)

        sidebar_layout.addWidget(nav_container)
        sidebar_layout.addStretch()
        
        return sidebar

    def create_nav_button(self, icon_path, tooltip, tab_name):
        button = QPushButton()
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(40, 40))
        button.setFixedSize(60, 60)
        button.setToolTip(tooltip)
        button.clicked.connect(lambda checked=False, b=button, tab=tab_name: self.handle_nav_click(b, tab))

        # Set button style
        button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border-radius: 30px;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.1);
            }
        """)
        
        return button

    def create_content_area(self):
        content_container = QFrame()
        content_container.setStyleSheet("background-color: white;")
        
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Create stacked widget for different tabs
        self.stacked_widget = QStackedWidget()
        content_layout.addWidget(self.stacked_widget)

        # Create tab contents
        self.create_dashboard_tab()
        self.create_patients_tab()
        self.create_appointments_tab()
        self.create_settings_tab()

        return content_container

    def create_stats_box(self, title, value, color):
        """Create a simple statistics box with just a value and title"""
        box = QFrame()
        box.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 8px;
            }}
        """)
        
        # Create layout for icon, number and title
        layout = QVBoxLayout(box)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(5)
        
        # Icon placeholder - will be added later
        icon_placeholder = QFrame()
        icon_placeholder.setFixedSize(24, 24)
        icon_placeholder.setStyleSheet("background-color: transparent;")
        layout.addWidget(icon_placeholder, alignment=Qt.AlignLeft)
        
        # Add value with large font
        value_label = QLabel(value)
        value_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: white;
        """)
        layout.addWidget(value_label)
        
        # Add title
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 14px;
            color: rgba(255, 255, 255, 0.8);
        """)
        layout.addWidget(title_label)
        
        # Add stretch to push everything to the top
        layout.addStretch()
        
        return box

    def create_shadow_effect(self):
        """Create a shadow effect for widgets"""
        from PySide6.QtWidgets import QGraphicsDropShadowEffect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 30))  # Semi-transparent black
        shadow.setOffset(0, 2)
        return shadow

    def create_dashboard_tab(self):
        # Dashboard tab
        dashboard_tab = QWidget()
        self.dashboard_layout = QVBoxLayout(dashboard_tab)
        self.dashboard_layout.setContentsMargins(0, 20, 0, 0)  # No left/right margins to allow line to reach edges
        self.dashboard_layout.setSpacing(20)  # Increased spacing for better layout

        # Title container to properly position the title
        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(20, 0, 20, 0)  # Keep some margin for the text itself
        
        # Title label
        title_label = QLabel("Dashboard")
        title_label.setStyleSheet("font-size: 50px; font-weight: bold; color: #333;")
        title_label.setFixedHeight(65)
        title_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        title_layout.addWidget(title_label)
        
        self.dashboard_layout.addWidget(title_container)

        # Horizontal line that will extend the full width
        self.divider_line = QFrame()
        self.divider_line.setFrameShape(QFrame.HLine)
        self.divider_line.setFrameShadow(QFrame.Sunken)
        self.divider_line.setStyleSheet("background-color: black;")
        self.divider_line.setFixedHeight(2)
        self.dashboard_layout.addWidget(self.divider_line)
        
        # Stats boxes container
        stats_container = QWidget()
        stats_layout = QHBoxLayout(stats_container)
        stats_layout.setContentsMargins(20, 10, 20, 10)
        stats_layout.setSpacing(15)  # Space between stat boxes
        
        # Create 5 statistics boxes with sample data
        stats_data = [
            {"title": "Total Patients", "value": "1,245", "color": "#4CAF50"},  # Green
            {"title": "Active Appointments", "value": "37", "color": "#2196F3"},  # Blue
            {"title": "Today's Patients", "value": "12", "color": "#FF9800"},  # Orange
            {"title": "Staff Members", "value": "24", "color": "#9C27B0"},  # Purple
            {"title": "Available Rooms", "value": "8", "color": "#F44336"}   # Red
        ]
        
        for stat in stats_data:
            box = self.create_stats_box(stat["title"], stat["value"], stat["color"])
            # Each box should have the same size policy, expanding equally
            box.setMinimumHeight(120)  # Set a fixed minimum height for uniformity
            stats_layout.addWidget(box)
        
        self.dashboard_layout.addWidget(stats_container)
        
        # Content container with proper margins for the rest of the dashboard
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(20, 10, 20, 20)
        content_layout.addStretch()
        
        self.dashboard_layout.addWidget(content_container, 1)  # Give it stretch to fill available space

        self.dashboard_tab = dashboard_tab
        self.stacked_widget.addWidget(dashboard_tab)

    def create_patients_tab(self):
        patients_tab = QLabel("Patients Content")
        patients_tab.setAlignment(Qt.AlignCenter)
        self.patients_tab = patients_tab
        self.stacked_widget.addWidget(patients_tab)

    def create_appointments_tab(self):
        appointments_tab = QLabel("Appointments Content")
        appointments_tab.setAlignment(Qt.AlignCenter)
        self.appointments_tab = appointments_tab
        self.stacked_widget.addWidget(appointments_tab)

    def create_settings_tab(self):
        settings_tab = QLabel("Settings Content")
        settings_tab.setAlignment(Qt.AlignCenter)
        self.settings_tab = settings_tab
        self.stacked_widget.addWidget(settings_tab)

    def resizeEvent(self, event):
        """Handle window resize events to adjust the divider line width"""
        super().resizeEvent(event)
        
    def switch_tab(self, tab_name):
        if tab_name == "dashboard_tab":
            self.stacked_widget.setCurrentWidget(self.dashboard_tab)
        elif tab_name == "patients_tab":
            self.stacked_widget.setCurrentWidget(self.patients_tab)
        elif tab_name == "appointments_tab":
            self.stacked_widget.setCurrentWidget(self.appointments_tab)
        elif tab_name == "settings_tab":
            self.stacked_widget.setCurrentWidget(self.settings_tab)

    def handle_nav_click(self, button, tab_name):
        # Reset all button styles
        for btn in self.nav_buttons:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border-radius: 30px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: rgba(0, 0, 0, 0.1);
                }
            """)
        
        # Set active button style
        button.setStyleSheet("""
            QPushButton {
                background-color: white;
                border-radius: 30px;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.8);
            }
        """)
        
        self.switch_tab(tab_name)

    def on_logout(self):
        self.logout_signal.emit()