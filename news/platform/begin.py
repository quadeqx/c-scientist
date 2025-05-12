from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class News(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        text = QLabel("Sit tight news coming soon!")
        self.layout.addWidget(text)
