import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
import pandas as pd
from pyqtgraph import DateAxisItem

import inspect

class AnalysisWidgets(QWidget):
    def __init__(self):
        super().__init__()
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        upper = QWidget()
        horiz = QHBoxLayout()
        upper.setStyleSheet("background-color: #3E3E3E;")
        upper.setLayout(horiz)

        self.layout.addWidget(upper)



        middle = QWidget()
        middle.setStyleSheet("background-color: #3E3E3E;")
        self.layout.addWidget(middle)



        bottom = QWidget()
        bottom.setStyleSheet("background-color: #3E3E3E;")
        self.layout.addWidget(bottom)
