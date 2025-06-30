from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg
from data import BinanceClient
from analytics import CrosshairHandler, CustomPlotWidget
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import Qt
from data.coins.coin_data import Data
from PyQt5.QtGui import QPalette, QColor

def preprocess_data(binance_data):
    processed = []
    for candle in binance_data:
        processed.append({
            "Date": float(candle['open_time']) /1000,
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
        w = 700
        print(self.data)
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
            rect = QtCore.QRectF(t - w, body_bottom, w * 2, body_height)
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
        #print(f"Creating MainWindow instance: {id(self)}")
        self.client = BinanceClient()
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.plot_widget = CustomPlotWidget()
        self.crosshair = CrosshairHandler(self.plot_widget)
        self.plot_widget.setBackground(QColor(30, 34, 45))
        self.plot_widget.setAxisItems({'bottom': pg.DateAxisItem()})


        data = Data().watchlists
        self.combobox = QComboBox(self.plot_widget)
        self.combobox.setEditable(True)
        self.combobox.setPlaceholderText('Select item')
        self.combobox.addItems([item for values in data.values() for item in values])
        self.combobox.setFixedSize(110, 30)
        self.combobox.setMaxVisibleItems(15)
        self.combobox.setPlaceholderText('Select coin')

        pallet = self.combobox.palette()
        pallet.setColor(QPalette.Base, QColor(30,34,45))
        pallet.setColor(QPalette.Button, QColor(30,34,45))
        self.combobox.setPalette(pallet)
        self.combobox.view().setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.layout.addWidget(self.plot_widget)
        self.setLayout(self.layout)
        self.has_plotted = False

        # Delay plotting until widget is shown
        QtCore.QTimer.singleShot(0, self.plot_candlesticks)

    def plot_candlesticks(self):

        if self.has_plotted:
            return
        try:
            _, raw_data = self.client.get_uiklines("BTCUSDT", "30m", limit=1000)
            if not raw_data:
                return
            processed = preprocess_data(raw_data)
            if not processed:
                return
            self.plot_widget.clear()  # Clear previous plot
            self.cross4 = CrosshairHandler(self.plot_widget)
            candlestick_item = CandlestickItem(processed)
            self.plot_widget.addItem(candlestick_item)
            self.has_plotted = True
        except Exception:
            pass
