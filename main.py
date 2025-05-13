import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QSizePolicy, QLabel
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtCore import Qt
import pandas as pd
import time
from charts.plots.volume_and_price import PriceAndVolume
from analytics.dashboard.visuals import AnalysisWidgets
from chatbot.bot.chat import Chat
from news.platform.begin import News
from reviews.rating.begin import Reviews

class CryptoDashboard(QMainWindow):
    def __init__(self):
        super().__init__()

        # Remove default title bar
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Read dataset
        self.df = pd.read_csv('data/BTCUSDT-2024-MAR.csv')

        # Set window properties
        self.setWindowTitle("Crypto Dashboard")
        self.setWindowIcon(QIcon('favicon.ico'))
        self.resize(800, 600)

        # Main widget and layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Create custom headerbar
        self.headerbar()

        # Create tab widget
        self.tab = QTabWidget()
        self.tab.setContentsMargins(0, 0, 0, 0)
        # Hide the default tab bar
        self.tab.tabBar().hide()

        # Add tabs
        self.chart = PriceAndVolume()
        self.analysis = AnalysisWidgets()
        self.chat = Chat()
        self.news = News()
        self.reviews = Reviews()

        self.tab.addTab(self.chart, "Charts")
        self.tab.addTab(self.analysis, "Analytics")
        self.tab.addTab(self.chat, "Chatbot")
        self.tab.addTab(self.news, "News")
        self.tab.addTab(self.reviews, "Reviews")

        # Add tab widget to main layout
        self.main_layout.addWidget(self.tab)

        self.apply_dark_theme()

        # Variables for window dragging
        self.dragging = False
        self.mouse_pos = None

    def headerbar(self):
        # Create headerbar widget
        headerbar = QWidget()
        headerbar.setFixedHeight(40)
        headerbar.setStyleSheet("background-color: #2E2E2E;")

        # Headerbar layout
        header_layout = QHBoxLayout(headerbar)
        header_layout.setContentsMargins(10, 0, 10, 0)
        header_layout.setSpacing(10)

        # Left spacer for centering
        left_spacer = QWidget()
        left_layout = QVBoxLayout(left_spacer)
        left_label = QLabel("Quadeqx")
        left_layout.addWidget(left_label)
        left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        header_layout.addWidget(left_spacer)

        # Tab buttons (mimicking QTabWidget tabs)
        tab_bar = QWidget()
        tab_layout = QHBoxLayout(tab_bar)
        tab_layout.setSpacing(10)

        # Create buttons for each tab
        charts_button = QPushButton("Charts")
        charts_button.setFixedSize(100, 30)
        charts_button.clicked.connect(lambda: self.tab.setCurrentIndex(0))
        tab_layout.addWidget(charts_button)

        analytics_button = QPushButton("Analytics")
        analytics_button.setFixedSize(100, 30)
        analytics_button.clicked.connect(lambda: self.tab.setCurrentIndex(1))
        tab_layout.addWidget(analytics_button)

        chat_button = QPushButton("Chatbot")
        chat_button.setFixedSize(100,30)
        chat_button.clicked.connect(lambda: self.tab.setCurrentIndex(2))
        tab_layout.addWidget(chat_button)

        news_button = QPushButton("News")
        news_button.setFixedSize(100,30)
        news_button.clicked.connect(lambda: self.tab.setCurrentIndex(3))
        tab_layout.addWidget(news_button)


        review_button = QPushButton("Reviews")
        review_button.setFixedSize(100, 30)
        review_button.clicked.connect(lambda: self.tab.setCurrentIndex(4))
        tab_layout.addWidget(review_button)

        header_layout.addWidget(tab_bar)

        # Right spacer
        right_spacer = QWidget()
        right_layout = QHBoxLayout(right_spacer)
        label = QLabel("Balance: ")
        right_layout.addWidget(label, alignment=Qt.AlignCenter)
        right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        header_layout.addWidget(right_spacer)

        # Window control buttons
        minimize_button = QPushButton("−")
        minimize_button.setFixedSize(15, 15)
        minimize_button.clicked.connect(self.showMinimized)
        header_layout.addWidget(minimize_button)

        maximize_button = QPushButton("O")
        maximize_button.setFixedSize(15, 15)
        maximize_button.clicked.connect(self.toggle_maximize)
        header_layout.addWidget(maximize_button)

        close_button = QPushButton("✕")
        close_button.setFixedSize(15, 15)
        close_button.clicked.connect(self.close)
        header_layout.addWidget(close_button)

        # Add headerbar to main layout
        self.main_layout.addWidget(headerbar)

    def apply_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        self.setPalette(palette)

        # Style buttons in headerbar
        button_style = """
            QPushButton {
                background-color: #3E3E3E;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #5E5E5E;
            }
            QPushButton:checked {
            background-color: #1E90FF;
            }
        """
        for button in self.findChildren(QPushButton):
            button.setStyleSheet(button_style)

    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    # Window dragging implementation
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.pos().y() < 40:  # Headerbar height
            self.dragging = True
            self.mouse_pos = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.mouse_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.dragging = False
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CryptoDashboard()
    window.show()
    sys.exit(app.exec_())
