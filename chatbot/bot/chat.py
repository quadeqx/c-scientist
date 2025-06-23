from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt

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
        self.text_label = QLabel("Section under Development!")
        self.text_label.setStyleSheet("""
            font-family: 'Roboto', 'Arial', sans-serif;
            font-size: 60px;
            font-weight: bold;
            color: #FFFFFF;
            background-color: #3E3E3E;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #5E5E5E;
        """)
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setFixedSize(800, 300)  # Fixed size for consistency

        h_layout.addWidget(self.text_label)
        h_layout.addStretch()

        self.layout.addLayout(h_layout)
        self.layout.addStretch()

