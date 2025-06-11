import pyqtgraph as pg
from pyqtgraph import DateAxisItem, PlotWidget, InfiniteLine
import PyQt5
from PyQt5.QtCore import QDate, Qt, QPointF
from PyQt5.QtGui import QBrush, QColor, QPainter, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTabWidget, QCalendarWidget, QGridLayout
import pandas as pd
from PyQt5.QtGui import QPainter, QBrush, QColor
import inspect
import sys
from .. import CustomPlotWidget, CrosshairHandler



class AnalysisWidgets(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)

        upper = QWidget()
        horiz = QHBoxLayout()
        upper.setStyleSheet("background-color: #3E3E3E;")
        upper.setLayout(horiz)

        self.portfolio = CustomPlotWidget()
        self.cross = CrosshairHandler(self.portfolio)
        horiz.addWidget(self.portfolio, stretch=1)


        self.by_coin = CustomPlotWidget()
        self.cross2 = CrosshairHandler(self.by_coin)
        horiz.addWidget(self.by_coin, stretch=1)

        key_metrics = QWidget()

        layout = QGridLayout()

        highest_profit = QWidget()
        highest_profit.setStyleSheet("background-color: #00ff00;")
        max_profit_layout = QVBoxLayout()
        highest_profit.setLayout(max_profit_layout)
        label = QLabel("Highest Profit")
        label.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        max_profit_layout.addWidget(label)


        highest_loss = QWidget()
        highest_loss.setStyleSheet("background-color: #ff0000;")
        highest_loss_layout = QVBoxLayout()
        highest_loss.setLayout(highest_loss_layout)
        label = QLabel("Highest Loss")
        label.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        highest_loss_layout.addWidget(label)


        volume = QWidget()
        volume.setStyleSheet("background-color: #0000ff")
        volume_layout = QVBoxLayout()
        volume.setLayout(volume_layout)
        label = QLabel("Volume")
        label.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        volume_layout.addWidget(label)

        net_profit = QWidget()
        net_profit.setStyleSheet("background-color: #ffff00;")
        net_profit_layout = QVBoxLayout()
        net_profit.setLayout(net_profit_layout)
        label = QLabel("Net Profit")
        label.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        net_profit_layout.addWidget(label)


        layout.addWidget(highest_profit, 0, 0)
        layout.addWidget(highest_loss, 0, 1)
        layout.addWidget(volume, 1, 0)
        layout.addWidget(net_profit, 1, 1)
        key_metrics.setLayout(layout)

        horiz.addWidget(key_metrics, stretch=1)

        self.layout.addWidget(upper, stretch=1)



        middle = QWidget()
        mid_horiz = QHBoxLayout()
        middle.setStyleSheet("background-color: #3E3E3E;")
        middle.setLayout(mid_horiz)


        class CustomCalendar(QCalendarWidget):
            def __init__(self):
                super().__init__()
                self.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)

            def paintCell(self, painter: QPainter, rect, date: QDate):

                # Call base implementation first to draw the default cell
                super().paintCell(painter, rect, date)

                # Custom paint logic for a specific date
                if date == QDate(2025, 5, 13):
                    painter.save()
                    painter.setClipRect(rect, Qt.IntersectClip)
                    painter.fillRect(rect, QColor(0, 255, 0, 100))
                    painter.setPen(Qt.green)
                    painter.setFont(QFont("Arial", 10, QFont.Normal))

                    text_rect = rect.adjusted(0, 20, 0, 0)
                    painter.drawText(text_rect, Qt.AlignHCenter | Qt.AlignBottom, "+ 2%")
                    painter.restore()

        calendar = CustomCalendar()
        mid_horiz.addWidget(calendar, stretch=1)


        self.inner = CustomPlotWidget()
        self.cross3 = CrosshairHandler(self.inner)
        mid_horiz.addWidget(self.inner, stretch=1)

        holdings_widget = QWidget()
        mid_horiz.addWidget(holdings_widget, stretch=1)
        self.layout.addWidget(middle, stretch=1)


        bottom = pg.TableWidget(10, 3, None, editable=True)
        bottom.setData([[1,2,3,4,5,6,7,8,9]])
        bottom.setStyleSheet("background-color: #3E3E3E;")
        bottom.horizontalHeader().setSectionResizeMode(PyQt5.QtWidgets.QHeaderView.Stretch)
        bottom.setHorizontalHeaderLabels(
            ["Date", "Ticker", "Entry Price", "Exit Price", "Leverage", "Position size", "Entry Fees", "Exit Fees", "Net Profit"])
        self.layout.addWidget(bottom, stretch=1)


