#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  8 03:20:40 2025

@author: quantum
"""

import logging
from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg
from data import BinanceClient
from analytics import CrosshairHandler, CustomPlotWidget
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import Qt
from data.coins.coin_data import Data
from PyQt5.QtGui import QPalette, QColor
from requests.exceptions import RequestException

# Configure logging
logging.basicConfig(level=logging.INFO, filename='app.log',
                    format='%(asctime)s - %(levelname)s - %(message)s')

def preprocess_data(binance_data):
    processed = []
    for candle in binance_data:
        processed.append({
            "Date": float(candle['open_time']) / 1000,
            "Open": float(candle['open']),
            "High": float(candle['high']),
            "Low": float(candle['low']),
            "Close": float(candle['close'])
        })
    return processed

class CandlestickItem(pg.GraphicsObject):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.generatePicture()

    def generatePicture(self):
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        self.w  = (self.data[1]['Date'] - self.data[0]['Date']) * 0.45
        w = self.w
        for row in self.data:
            t = row['Date']
            open_, high, low, close = row['Open'], row['High'], row['Low'], row['Close']
            p.setPen(pg.mkPen('g' if close > open_ else 'r'))
            p.drawLine(QtCore.QPointF(t, low), QtCore.QPointF(t, high))
            if open_ > close:
                p.setBrush(pg.mkBrush('r'))
                body_top = open_
                body_bottom = close
            else:
                p.setBrush(pg.mkBrush('g'))
                body_top = close
                body_bottom = open_
            body_height = abs(body_top - body_bottom)
            p.setPen(pg.mkPen(None))
            rect = QtCore.QRectF(t - self.w, body_bottom, self.w * 2, body_height)
            p.drawRect(rect)
        p.end()

    def paint(self, painter, option, widget):
        painter.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        rect = self.picture.boundingRect()
        return QtCore.QRectF(rect)

class Candle(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.client = BinanceClient()
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.plot_widget = CustomPlotWidget()
        self.crosshair = CrosshairHandler(self.plot_widget)
        self.plot_widget.setBackground(QColor(30, 34, 45))

        vb = self.plot_widget.getViewBox()
        vb.setLimits(xMin=0, xMax=100, minXRange=70000)

        self.plot_widget.getViewBox().setMouseEnabled(x=True, y=True)
        self.plot_widget.getAxis('left').setVisible(False)
        self.plot_widget.getAxis('right').setVisible(True)
        self.plot_widget.setAxisItems({'bottom': pg.DateAxisItem()})
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_candles)
        self.processed = []
        self.has_plotted = False
        self.current_coin = "BTCUSDT"

        data = Data().watchlists
        self.combobox = QComboBox(self.plot_widget)
        self.combobox.setEditable(True)
        self.combobox.setPlaceholderText('Select coin')
        self.combobox.addItems([item for values in data.values() for item in values])
        self.combobox.setCurrentIndex(0)
        self.combobox.setFixedSize(110, 30)
        self.combobox.setMaxVisibleItems(15)
        pallet = self.combobox.palette()
        pallet.setColor(QPalette.Base, QColor(30, 34, 45))
        pallet.setColor(QPalette.Button, QColor(30, 34, 45))
        self.combobox.setPalette(pallet)
        self.combobox.view().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.combobox.activated[str].connect(self.on_coin_changed)
        self.combobox.lineEdit().editingFinished.connect(self.on_coin_changed)

        self.layout.addWidget(self.plot_widget)
        self.setLayout(self.layout)

        QtCore.QTimer.singleShot(0, self.plot_candlesticks)

    def on_coin_changed(self):
        selected_text = self.combobox.currentText().strip()
        if not selected_text or self.combobox.currentIndex() == 0:
            selected_text = "BTC"
        self.current_coin = selected_text + "USDT"
        logging.info(f"Coin changed to: {self.current_coin}")
        self.has_plotted = False  # Reset to allow replot
        self.timer.stop()  # Stop continuous updates
        self.plot_candlesticks()  # Replot with new coin

    def plot_candlesticks(self):
        if self.has_plotted:
            return
        try:
            _, raw_data = self.client.get_uiklines(self.current_coin, "30m", limit=1000)
            if not raw_data:
                QtWidgets.QMessageBox.warning(self, "Error", f"No data for {self.current_coin}")
                return
            self.processed = preprocess_data(raw_data)
            if not self.processed:
                QtWidgets.QMessageBox.warning(self, "Error", f"Failed to process data")
                return
            self.plot_widget.clear()
            self.crosshair = CrosshairHandler(self.plot_widget)
            candlestick_item = CandlestickItem(self.processed)
            price_line = pg.InfiniteLine(pos=self.processed[-1]['Close'], angle=0, pen=pg.mkPen("white", width=0.7))
            self.plot_widget.addItem(candlestick_item)
            self.plot_widget.addItem(price_line)
            self.has_plotted = True
            self.timer.start(2000)  # Update every 30 seconds
        except RequestException as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"Network error: {e}")
        except (IndexError, KeyError, TypeError) as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"Data error: {e}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Unexpected error: {e}")

    def update_candles(self):
        """Update candlestick data for the current coin."""
        try:
            _, data = self.client.get_uiklines(self.current_coin, "30m", limit=1)
            if not data:
                return
            stripped_data = preprocess_data(data)
            if not stripped_data:
                return
            self.plot_widget.clear()
            self.crosshair = CrosshairHandler(self.plot_widget)
            if int(stripped_data[0]['Open']) == int(self.processed[-1]['Open']):
                self.processed[-1]['Close'] = stripped_data[0]['Close']
            else:
                self.processed.append(stripped_data[0])
            candlestick_item = CandlestickItem(self.processed)
            price_line = pg.InfiniteLine(pos=self.processed[-1]['Close'], angle=0, pen=pg.mkPen("white", width=0.7))
            self.plot_widget.addItem(candlestick_item)
            self.plot_widget.addItem(price_line)
            if len(self.processed) > 1000:
                self.processed.pop(0)
        except RequestException as e:
            QtWidgets.QMessageBox.critical(self, "Network Error", f"{e}")
        except (IndexError, KeyError, TypeError) as e:
            QtWidgets.QMessageBox.critical(self, "Data Error", f"{e}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Unexpected error: {e}")
