import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject
import logging
from colorama import Fore, Style


logger = logging.getLogger(__name__)

def preprocess_data(data):
    processed = []
    for candle in data:
        processed.append({
            "Date": float(candle['open_time']) / 1000,
            "Open": float(candle['open']),
            "High": float(candle['high']),
            "Low": float(candle['low']),
            "Close": float(candle['close'])
        })
    return processed


class Essentials(QObject):
    width = pyqtSignal(float)

    def __init__(self):
        super().__init__()
        self.value = 900


    @pyqtSlot(float)
    def width_getter(self, width_value):
        logging.info(f"{Fore.RED}We're getting something {width_value} {Style.RESET_ALL}")
        self.value = width_value

        self.width.emit(width_value)


class CandlestickItem(pg.GraphicsObject):
    def __init__(self, data, essentials):
        super().__init__()
        self.width = None
        self.data = data
        self.essentials = essentials
        self.generatePicture()


    @pyqtSlot(float)
    def width_obtainer(self, val: float):
        self.width = val
        logger.info(f"{Fore.GREEN} The emitted width is {self.width} {Style.RESET_ALL}")


    def generatePicture(self):
        logger.info(f"{Fore.BLUE} We've gotten {self.essentials.value} as our width. {Style.RESET_ALL}")
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        self.w  = self.essentials.value *0.45
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
