from PyQt5.QtCore import QThread, pyqtSignal, QObject, QMetaObject, Q_ARG, Qt, pyqtSlot, QTimer
import threading
import traceback
from functools import partial
from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg
from data import BinanceClient
from analytics import CrosshairHandler, CustomPlotWidget
from PyQt5.QtWidgets import QComboBox
from data.coins.coin_data import Data
from PyQt5.QtGui import QPalette, QColor
from requests.exceptions import RequestException
from pyqtgraph import InfiniteLine
from . import preprocess_data, CandlestickItem, Essentials
import logging
import time
from colorama import Fore, Style

logger = logging.getLogger(__name__)


class DataWorker(QObject):
    data_fetched = pyqtSignal(dict)
    error_occurred = pyqtSignal(str, str)  # Signal for errors (title, message)
    width_emitted = pyqtSignal(float)


    def __init__(self, client, coin, interval):
        super().__init__()
        self.client = client
        self._coin = coin
        self._interval = interval
        self._burst_done = False

    @pyqtSlot()
    def start(self):
        logger.info("Op's started...")
        self.timer = QTimer()
        self.timer.setInterval(2000)
        self.timer.timeout.connect(self.emitter)
        self.timer.start()

    @pyqtSlot()
    def emitter(self):
        if not self._burst_done:
            _, raw = self.client.get_uiklines(self._coin, self._interval, limit= 5)
            width = int(raw[-1]["open_time"] - raw[-2]["open_time"]) / 1000
            logger.info(f"{Fore.GREEN} {width} {Style.RESET_ALL}")
            self.width_emitted.emit(width)
            preprocessed = preprocess_data(raw)
            for u in preprocessed:
                logger.info(f"Emitted {u} for updates..........")
                self.data_fetched.emit(u)
                self._burst_done = True

        else:
            logger.info("Perfoming single calls..........................................")
            _, raw = self.client.get_uiklines(self._coin, self._interval, 1)
            preprocesed = preprocess_data(raw)
            self.data_fetched.emit(preprocesed[0])


    @pyqtSlot(str)
    def update_coin(self, coin):
        self._burst_done = False
        logger.info(f"Updating coin to: {coin}")
        self._coin = coin

    @pyqtSlot(str)
    def update_interval(self, interval):
        self._burst_done = False
        logging.info(f"{Fore.RED}Updating interval to: {interval} {Style.RESET_ALL}")

        self._interval = interval


class Candle(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.plot_widget = CustomPlotWidget()
        self.crosshair = CrosshairHandler(self.plot_widget)
        self.plot_widget.setBackground(QColor(30, 34, 45))
        vb = self.plot_widget.getViewBox()

        vb.setLimits(minXRange=None)
        vb.setAutoVisible(x=True, y=False)

        self.plot_widget.getAxis('left').setVisible(False)
        self.plot_widget.getAxis('right').setVisible(True)
        self.plot_widget.setAxisItems({'bottom': pg.DateAxisItem()})
        self.current_coin = "BTCUSDT"
        self.has_plotted = False
        self.current_price_line = None
        self.new_time = "30m"
        self.essential = Essentials()

        # === Start in Qthread and run fetching there ===
        self.client = BinanceClient()
        self.thread = QThread()
        self.worker = DataWorker(self.client, self.current_coin, self.new_time)

        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.start)
        self.worker.data_fetched.connect(self.plotter)
        self.thread.start()


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
            combobox.currentIndexChanged.connect(connector)
            return combobox




        self.time = combobox("Time frame", ["1s", "1m","5m", "15m", "30m", "1h", "2h", "4h", "8h", "12h", "1d", "1w"], self.timeframe_changed)
        self.time.move(114,0)
        data = Data().watchlists
        self.select_coin = combobox("Select a coin", [item for values in data.values() for item in values], self.on_coin_changed)


        self.layout.addWidget(self.plot_widget)
        self.setLayout(self.layout)


    def timeframe_changed(self):
        self.new_time = self.time.currentText().strip() or "5m"
        logging.info(f"Timeframe changed to: {self.new_time}")

        self.plot_widget.clear()

        self.worker.width_emitted.connect(self.essential.width_getter)

        QMetaObject.invokeMethod(self.worker, "update_interval",
                                Qt.QueuedConnection, Q_ARG(str, self.new_time))


    def on_coin_changed(self):
        selected_text = self.select_coin.currentText().strip() or "BTC"
        self.current_coin = selected_text + "USDT"
        logging.info(f"Coin changed to: {self.current_coin}")
        self.plot_widget.clear()
        QMetaObject.invokeMethod(self.worker, "update_coin",
                                 Qt.QueuedConnection, Q_ARG(str, self.current_coin))


    @pyqtSlot(dict)
    def plotter(self, values: dict):
        logger.info(f"Plotting can be done here using....%s", values)
        self.plot_widget.addItem(CandlestickItem(values, self.essential))









