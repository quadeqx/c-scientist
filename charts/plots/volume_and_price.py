from PyQt5.QtCore import QThread, pyqtSignal, QObject
import threading
import traceback
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
from pyqtgraph import InfiniteLine


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
        self.current_coin = "BTCUSDT"
        self.generatePicture()

    def generatePicture(self):
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        self.w  = 1800 *0.45
        t = self.data['Date']
        open_, high, low, close = self.data['Open'], self.data['High'], self.data['Low'], self.data['Close']
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

# Worker class for fetching data in a separate thread
class DataWorker(QObject):
    data_fetched = pyqtSignal(list)  # Signal to emit fetched data
    error_occurred = pyqtSignal(str, str)  # Signal for errors (title, message)

    def __init__(self, client, coin, interval, limit):
        super().__init__()
        self.client = client
        self.coin = coin
        self.interval = interval
        self.limit = limit

    def fetch_data(self):
        try:
            _, data = self.client.get_uiklines(self.coin, self.interval, limit=self.limit)
            if data:
                processed = preprocess_data(data)
                self.data_fetched.emit(processed)
            else:
                self.error_occurred.emit("Error", "No data received")
        except RequestException as e:
            self.error_occurred.emit("Network Error", f"{e}")
        except (IndexError, KeyError, TypeError) as e:
            self.error_occurred.emit("Data Error", f"{str(e)}\n\n{traceback.format_exc()}")
        except Exception as e:
            self.error_occurred.emit("Error", f"Unexpected error: {e}\n\n{traceback.format_exc()}")

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

        vb.setLimits(minXRange=70000)
        vb.setAutoVisible(x=True, y=False)

        self.plot_widget.getAxis('left').setVisible(False)
        self.plot_widget.getAxis('right').setVisible(True)
        self.plot_widget.setAxisItems({'bottom': pg.DateAxisItem()})
        self.current_coin = "BTCUSDT"
        self.processed = []
        self.has_plotted = False
        self.current_price_line = None
        self.new_time = "30m"

        # Setup worker thread
        self.thread = QThread()
        self.worker = DataWorker(self.client, self.current_coin, self.new_time, 1)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.fetch_data)
        self.worker.data_fetched.connect(self.update_candles_with_data)
        self.worker.error_occurred.connect(self.show_error)
        self.thread.start()

        # Timer for periodic updates
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.start_worker)
        self.timer.start(1000)


        def combobox(placeholder: str, data: list, connector):
            combobox = QComboBox(self.plot_widget)
            combobox.setEditable(True)
            combobox.setPlaceholderText(placeholder)
            combobox.addItems(data)
            combobox.setCurrentIndex(0)
            combobox.setFixedSize(110, 30)
            combobox.setMaxVisibleItems(15)
            pallet = combobox.palette()
            pallet.setColor(QPalette.Base, QColor(30, 34, 45))
            pallet.setColor(QPalette.Button, QColor(30, 34, 45))
            combobox.setPalette(pallet)
            combobox.view().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            combobox.activated[str].connect(connector)
            combobox.lineEdit().editingFinished.connect(connector)
            return combobox

        self.time = combobox("Time frame", ["5m", "15m", "30m", "1h", "2h", "4h", "8h", "12h", "1d", "1w"], self.timeframe_changed)
        self.time.move(114,0)
        data = Data().watchlists
        self.select_coin = combobox("Select a coin", [item for values in data.values() for item in values], self.on_coin_changed)


        self.layout.addWidget(self.plot_widget)
        self.setLayout(self.layout)

        QtCore.QTimer.singleShot(0, self.plot_candlesticks)

    def timeframe_changed(self):
        self.new_time = self.time.currentText().strip()
        if not self.new_time or self.time.currentIndex() == 0:
            self.new_time = "30m"
        logging.info(f"Timeframe changed to: {self.new_time}")
        self.has_plotted = False
        self.timer.stop()  # Stop updates
        self.plot_candlesticks()  # Replot with new coin
        self.plot_widget.getViewBox().autoRange()
        self.timer.start(2000)  # Restart updates

    def start_worker(self):
        """Start the worker thread to fetch data."""
        if self.thread.isRunning():
            return  # Avoid starting a new thread if one is already running
        self.worker.coin = self.current_coin  # Update coin for worker
        self.worker.time = self.new_time
        self.thread.start()

    def update_candles_with_data(self, stripped_data):
        """Update candlestick plot with fetched data."""
        try:
            if not stripped_data:
                return
            if self.processed and int(stripped_data[0]['Date']) == int(self.processed[-1]['Date']):
                # Update existing candlestick
                self.processed[-1] = stripped_data[0]
                candlestick_item = CandlestickItem(self.processed[-1])
                # Remove the last candlestick and current price line
                for item in self.plot_widget.items():
                    if isinstance(item, CandlestickItem) and item.data['Date'] == self.processed[-1]['Date']:
                        self.plot_widget.removeItem(item)
                        break
                if self.current_price_line:
                    self.plot_widget.removeItem(self.current_price_line)
                # Add new price line
                self.current_price_line = pg.InfiniteLine(pos=self.processed[-1]['Close'], angle=0)
                self.plot_widget.addItem(self.current_price_line)
                self.plot_widget.addItem(candlestick_item)
            else:
                # Add new candlestick
                self.processed.append(stripped_data[0])
                candlestick_item = CandlestickItem(stripped_data[0])
                if self.current_price_line:
                    self.plot_widget.removeItem(self.current_price_line)
                self.current_price_line = pg.InfiniteLine(pos=stripped_data[0]['Close'], angle=0)
                self.plot_widget.addItem(self.current_price_line)
                self.plot_widget.addItem(candlestick_item)
        finally:
            self.thread.quit()  # Ensure thread quits after processing
            self.thread.wait()

    def show_error(self, title, message):
        """Display error message."""
        QtWidgets.QMessageBox.critical(self, title, message)
        self.thread.quit()
        self.thread.wait()

    def on_coin_changed(self):
        """Handle coin selection change."""
        selected_text = self.select_coin.currentText().strip()
        if not selected_text or self.select_coin.currentIndex() == 0:
            selected_text = "BTC"
        self.current_coin = selected_text + "USDT"
        logging.info(f"Coin changed to: {self.current_coin}")
        self.has_plotted = False
        self.timer.stop()  # Stop updates
        self.plot_candlesticks()  # Replot with new coin
        self.plot_widget.getViewBox().autoRange()
        self.timer.start(2000)  # Restart updates

    def plot_candlesticks(self):
        if self.has_plotted:
            return
        try:
            _, raw_data = self.client.get_uiklines(self.current_coin, self.new_time, limit=1000)
            if not raw_data:
                QtWidgets.QMessageBox.warning(self, "Error", f"No data for {self.current_coin}")
                return
            self.processed = preprocess_data(raw_data)
            if not self.processed:
                QtWidgets.QMessageBox.warning(self, "Error", "Failed to process data")
                return
            self.plot_widget.clear()
            self.crosshair = CrosshairHandler(self.plot_widget)
            for i in range(len(self.processed)):
                candlestick_item = CandlestickItem(self.processed[i])
                self.plot_widget.addItem(candlestick_item)
            self.current_price_line = pg.InfiniteLine(pos=self.processed[-1]['Close'], angle=0)
            self.plot_widget.addItem(self.current_price_line)
            self.has_plotted = True
        except RequestException as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"Network error: {e}")
        except (IndexError, KeyError, TypeError) as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"Data error: {e}\n{traceback.format_exc()}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Unexpected error: {e}\n{traceback.format_exc()}")

    def closeEvent(self, event):
        """Clean up thread on widget close."""
        self.timer.stop()
        self.thread.quit()
        self.thread.wait()
        event.accept()
