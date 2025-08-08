from PyQt5.QtWidgets import QWidget, QGridLayout, QTableWidgetItem
import pyqtgraph
from pyqtgraph import TableWidget
from PyQt5.QtCore import pyqtSignal, QObject, QRunnable, QThreadPool, QTimer
from data.coins.coin_data import coinprice, Data
from functools import partial
import logging
import time
from data.watchlists import CenteredItemDelegate
from logging.handlers import RotatingFileHandler
import PyQt5

# Configure logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.propagate = False
"""
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

file_handler = RotatingFileHandler('watchlist.log', maxBytes=1_000_000, backupCount=3)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
"""
class WatchlistManager(QWidget):
    """Watchlist management class."""

    def __init__(self):
        super().__init__()

        self.data_manager = Data()
        self.coinprice = coinprice()
        self.threadpool = QThreadPool.globalInstance()
        self.threadpool.setMaxThreadCount(10)  # Allow overlap for slow fetches

        self.fetching = {
            'Payments': False,
            'Artificial Int': False,
            'Meme': False,
            'Layer 3': False,
            'Layer 1': False,
            'Dexchange': False,
            'Liquid Staking': False,
            'Layer 0': False,
            'Layer 2': False,
            'Analytics': False
            }

        self.table_data = {}

        for category, coins in self.data_manager.watchlists.items():
            self.table_data[category] = {coin: [coin, 0, 0, 0, 0, 0, 0] for coin in coins}



        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)


        self.SetTable('Payments', 0, 0)
        self.SetTable('Meme', 0,1)
        self.SetTable('Liquid Staking', 0, 2)
        self.SetTable('Artificial Int', 1, 0)
        self.SetTable('Layer 3', 1, 1)
        self.SetTable('Dexchange', 1, 2)
        self.SetTable('Layer 0', 2, 0)
        self.SetTable('Layer 1', 2, 1)
        self.SetTable('Layer 2', 2, 2)



    def SetTable(self, category, x, y):
        """Create tables for watchlists."""
        self.category = TableWidget()
        self.category.resizeColumnsToContents()
        self.layout.addWidget(self.category, x, y)

        self.timer = QTimer(self)
        self.timer.timeout.connect(partial(self.start_fetch, self.category, category))
        self.timer.start(3000)
        self.start_fetch(self.category, category)
        self.category.setItemDelegate(CenteredItemDelegate(self.category))


    def start_fetch(self, table, category):
        """Fetch data using threadpolls."""
        if self.fetching[category]:
            logger.debug(f"Fetch already in progress for {category}")
            return
        if self.threadpool.activeThreadCount() >= self.threadpool.maxThreadCount():
            logger.warning(f"Thread pool full, skipping fetch for {category}")
            return
        self.fetching[category] = True
        fetcher = DataFetcher(self.coinprice, category)
        fetcher.signals.dataFetched.connect(partial(self._update_table, table, category))
        fetcher.signals.finished.connect(partial(self._fetch_complete, category))
        self.threadpool.start(fetcher)

    def _fetch_complete(self, category):
        self.fetching[category] = False



    def _update_table(self, table, category, data):
        try:
            processed = self.coinprice.prepare_table_data(data, category)
            logger.info(f"[{id(table)}] Updating table for {category} with data: {processed}")

            new_data = {row[0]: row for row in processed}
            current_data = self.table_data[category]

            if len(new_data) > table.rowCount():
                table.setRowCount(len(new_data))

            max_columns = max(len(row) for row in new_data.values())
            if table.columnCount() < max_columns:
                table.setColumnCount(max_columns)

            table.setHorizontalHeaderLabels([category, 'Open', 'High', 'Low', 'Close', 'Volume', "Trades"])

            table.blockSignals(True)
            for row_idx, (coin, new_row) in enumerate(new_data.items()):
                for col_idx, value in enumerate(new_row):
                    if new_data[coin][0] == current_data[coin][0]:
                        item = QTableWidgetItem(str(value))
                        table.setItem(row_idx, col_idx, item)
            table.blockSignals(False)

            self.table_data[category] = new_data


            # Force GUI update
            table.viewport().update()
            table.resizeColumnsToContents()
            table.horizontalHeader().setSectionResizeMode(PyQt5.QtWidgets.QHeaderView.Stretch)


        except Exception as e:
            logger.error(f"Error updating table for {category}: {str(e)}")



    def closeEvent(self, event):
        """Close threadpools."""
        self.threadpool.clear()
        self.threadpool.waitForDone()
        super().closeEvent(event)

class FetcherSignals(QObject):
    """Signal class for fetched data."""

    dataFetched = pyqtSignal(dict)
    finished = pyqtSignal()

class DataFetcher(QRunnable):
    """Fetches the data for the tables."""

    def __init__(self, coinprice, category):
        super().__init__()
        self.coinprice = coinprice
        self.category = category
        self.signals = FetcherSignals()

    def run(self):
        """Get the data."""
        try:
            start_time = time.time()
            data = self.coinprice.getprices(self.category)
            duration = time.time() - start_time
            logger.info(f"Fetch for {self.category} took {duration:.2f}s")
            self.signals.dataFetched.emit(data)
        except Exception as e:
            logger.error(f"Error fetching data for {self.category}: {str(e)}")
        finally:
            self.signals.finished.emit()
