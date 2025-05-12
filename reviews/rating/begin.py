from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class Reviews(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        text = QLabel("You will review once the system is on")
        self.layout.addWidget(text)
