import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGraphicsOpacityEffect
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtWidgets import QGraphicsDropShadowEffect

class Chat(QWidget):
    def __init__(self):
        super().__init__()
        # Initialize the main layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Add vertical spacer to center content
        self.layout.addStretch()

        # Create horizontal layout for centering the label
        h_layout = QHBoxLayout()
        h_layout.addStretch()

        # Add stylish text label
        self.text_label = QLabel("You will chat soon!")
        self.text_label.setStyleSheet("""
            font-family: 'Roboto', 'Arial', sans-serif;
            font-size: 24px;
            font-weight: bold;
            color: #FFFFFF;
            background-color: #3E3E3E;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #5E5E5E;
        """)
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setFixedSize(300, 100)  # Fixed size for consistency

        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 100))
        self.text_label.setGraphicsEffect(shadow)

        # Add opacity effect for animation
        self.opacity_effect = QGraphicsOpacityEffect()
        self.text_label.setGraphicsEffect(self.opacity_effect)

        h_layout.addWidget(self.text_label)
        h_layout.addStretch()

        self.layout.addLayout(h_layout)
        self.layout.addStretch()

        # Set minimum size to ensure visibility
        self.setMinimumSize(400, 300)

        # Add pulse animation
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(2000)
        self.animation.setStartValue(0.6)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.setLoopCount(-1)  # Loop indefinitely
        self.animation.start()
