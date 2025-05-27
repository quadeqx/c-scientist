from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg
from datetime import datetime
import traceback
from data.coins.coin_data import BinanceClient

def ts_to_datetime(ms_timestamp):
    return datetime.fromtimestamp(ms_timestamp / 1000.0).isoformat()

def preprocess_binance_data(binance_data):
    processed = []
    for candle in binance_data:
        dt = datetime.fromisoformat(candle["open_time"])
        timestamp = dt.timestamp()
        processed.append({
            "Date": timestamp,
            "Open": float(candle["open"]),
            "High": float(candle["high"]),
            "Low": float(candle["low"]),
            "Close": float(candle["close"])
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
        w = 30

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
        print(f"Creating MainWindow instance: {id(self)}")
        self.client = BinanceClient()
        self.layout = QtWidgets.QVBoxLayout()
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setAxisItems({'bottom': pg.DateAxisItem()})
        self.layout.addWidget(self.plot_widget)


        self.setLayout(self.layout)
        self.has_plotted = False

        # Delay plotting until widget is shown
        QtCore.QTimer.singleShot(0, self.plot_candlesticks)

    def plot_candlesticks(self):
        if self.has_plotted:
            print("Skipping redundant plot call")
            print("Call stack:", traceback.format_stack())
            return
        try:
            print("Fetching data and plotting...")
            print("Call stack:", traceback.format_stack())
            raw_data = self.client.get_uiklines("BTCUSDT", "1m", limit=1000)
            if not raw_data:
                print("No data to plot (API call skipped)")
                return
            processed = preprocess_binance_data(raw_data)
            if not processed:
                print("No data received from Binance API")
                return
            self.plot_widget.clear()  # Clear previous plot
            candlestick_item = CandlestickItem(processed)
            self.plot_widget.addItem(candlestick_item)
            start = processed[0]['Date'] if len(processed) >= 10 else processed[0]['Date']
            end = processed[-1]['Date']
            self.plot_widget.setXRange(start, end, padding=0.05)
            self.has_plotted = True
        except Exception as e:
            print(f"Error fetching or plotting data: {e}")
