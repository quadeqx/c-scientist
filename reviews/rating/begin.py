from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt

class Reviews(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Add vertical spacer to center content
        self.layout.addStretch()

        # Create horizontal layout for centering the label
        h_layout = QHBoxLayout()
        h_layout.addStretch()

        self.text_label = QLabel("Reviewing is disabled!")
        self.text_label.setStyleSheet("""
            font-family: 'Roboto', 'Arial', sans-serif;
            font-size: 40px;
            font-weight: bold;
            color: #FFFFFF;
            background-color: #3E3E3E;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #5E5E5E;
        """)
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setFixedSize(800, 300)

        h_layout.addWidget(self.text_label)
        h_layout.addStretch()
        self.layout.addLayout(h_layout)
        self.layout.addStretch()
