from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QSizePolicy
)
from PyQt5.QtGui import QColor
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import numpy as np
from analytics import CrosshairHandler, CustomPlotWidget
from PyQt5 import QtCore

class CoveredCallCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Covered Call Calculator")

        # Input fields
        self.stock_price_input = QLineEdit()
        self.stock_price_input.setPlaceholderText("Stock Purchase Price")

        self.strike_price_input = QLineEdit()
        self.strike_price_input.setPlaceholderText("Strike Price")

        self.premium_input = QLineEdit()
        self.premium_input.setPlaceholderText("Premium Received")

        self.contract_input = QLineEdit()
        self.contract_input.setPlaceholderText("Contracts against")

        self.calc_button = QPushButton("Calculate")
        self.calc_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;   /* Green */
                color: white;
                padding: 8px 20px;
                border: none;
                border-radius: 20px;  /* Fully rounded button */
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.calc_button.clicked.connect(self.calculate)

        self.result_label = QLabel("")
        self.result_label.setContentsMargins(0, 0, 0, 0)  # Optional: tighten label margins

        # Arrange inputs horizontally
        input_row = QHBoxLayout()
        input_row.setSpacing(0)  # No space between widgets
        input_row.setContentsMargins(0, 0, 0, 0)
        input_row.addWidget(self.stock_price_input)
        input_row.addWidget(self.strike_price_input)
        input_row.addWidget(self.premium_input)
        input_row.addWidget(self.contract_input)
        input_row.addWidget(self.calc_button)

        # Plot widget
        self.plot_widget = CustomPlotWidget()
        self.plot_widget.setBackground(QColor(30, 34, 45))
        self.cross = CrosshairHandler(self.plot_widget)
        self.plot_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Main vertical layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)  # No space between rows
        main_layout.setContentsMargins(0, 0, 0, 0)  # Remove padding around layout
        main_layout.addLayout(input_row)
        main_layout.addWidget(self.result_label)
        main_layout.addWidget(self.plot_widget)

        self.setLayout(main_layout)

    def calculate(self):
        try:
            stock_price = float(self.stock_price_input.text())
            strike_price = float(self.strike_price_input.text())
            premium = float(self.premium_input.text())
            contract = float(self.contract_input.text())
            
            breakeven = stock_price - premium
            max_gain = ((strike_price - stock_price) + premium) * contract
            
            self.result_label.setText(f"Breakeven: {breakeven:.2f}, Total PnL: {max_gain:.2f} (Excluding fees and dividents)")
            
            # Calculate x and y
            stock_price = float(self.stock_price_input.text())
            strike_price = float(self.strike_price_input.text())
            premium = float(self.premium_input.text())
            contract = float(self.contract_input.text())
            
            breakeven = stock_price - premium
            max_gain = ((strike_price - stock_price) + premium) * contract
            
            self.result_label.setText(f"Breakeven: {breakeven:.2f}, Total PnL: {max_gain:.2f} (Excluding fees and dividents)")
            
            # Calculate x and y
            x = np.linspace(stock_price * 0.5, stock_price * 1.5, 500)
            y = (np.where(x < strike_price, x - stock_price + premium, strike_price - stock_price + premium)) * contract
            
            self.plot_widget.clear()
            
            # Separate y >= 0 and y < 0 regions
            above_zero_x = x[y >= 0]
            above_zero_y = y[y >= 0]
            below_zero_x = x[y < 0]
            below_zero_y = y[y < 0]
            
            # Plot curves
            gain_curve = pg.PlotDataItem(above_zero_x, above_zero_y, pen=pg.mkPen('g', width=2))
            loss_curve = pg.PlotDataItem(below_zero_x, below_zero_y, pen=pg.mkPen('r', width=2))
            self.plot_widget.addItem(gain_curve)
            self.plot_widget.addItem(loss_curve)
            
            # Zero curves for shading
            zero_curve_gain = pg.PlotDataItem(above_zero_x, np.zeros_like(above_zero_x), pen=None)
            zero_curve_loss = pg.PlotDataItem(below_zero_x, np.zeros_like(below_zero_x), pen=None)
            
            # Fill between
            fill_gain = pg.FillBetweenItem(gain_curve, zero_curve_gain, brush=pg.mkBrush(0, 255, 0, 100))
            fill_loss = pg.FillBetweenItem(loss_curve, zero_curve_loss, brush=pg.mkBrush(255, 0, 0, 100))
            self.plot_widget.addItem(fill_gain)
            self.plot_widget.addItem(fill_loss)




        except ValueError as e:
            self.result_label.setText("Invalid input. Please enter numeric values.")
            print(e)
