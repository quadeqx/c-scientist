from PyQt5.QtWidgets import QWidget, QGridLayout
from data.calculators.covered_call import CoveredCallCalculator

class Option_calculators(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        for i in range(3):
            for j in range(3):
                calculator = CoveredCallCalculator()
                self.layout.addWidget(calculator, i, j)
