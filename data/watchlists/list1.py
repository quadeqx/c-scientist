from PyQt5.QtWidgets import QWidget, QGridLayout
from pyqtgraph import TableWidget
from PyQt5.QtCore import pyqtSignal, QObject, QRunnable, QThreadPool, QTimer
from data.coins.coin_data import coinprice, Data
from functools import partial
import logging
import time
from data.watchlists import CenteredItemDelegate

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WatchlistManager(QWidget):
    def __init__(self):
        super().__init__()

        self.data_manager = Data()
        self.coinprice = coinprice()
        self.threadpool = QThreadPool.globalInstance()
        self.threadpool.setMaxThreadCount(10)  # Allow overlap for slow fetches

        self.fetching = {
            'payments': False,
            'ai': False,
            'meme': False,
            'L_3': False,
            'L_1': False,
            'dexchange': False,
            'liquid_staking': False,
            'L_0': False,
            'L_2': False
            }  # Track fetch status

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # === payments ===
        self.payments = TableWidget(10, 7)
        self.payments.setHorizontalHeaderLabels(['Coin', 'Open', 'High', 'Low', 'Close', 'Volume', 'Trades'])
        self.payments.resizeColumnsToContents()
        self.layout.addWidget(self.payments, 0, 0)

        self.timer_payments = QTimer(self)
        self.timer_payments.timeout.connect(partial(self.start_fetch, self.payments, 'payments'))
        self.timer_payments.start(3000)
        self.start_fetch(self.payments, 'payments')


        # === AI===
        self.ai = TableWidget(10, 1)
        self.ai.setHorizontalHeaderLabels(['AI Coin'])
        self.ai.resizeColumnsToContents()
        self.layout.addWidget(self.ai, 1, 0)

        self.timer_ai = QTimer(self)
        self.timer_ai.timeout.connect(partial(self.start_fetch, self.ai, 'ai'))
        self.timer_ai.start(3000)
        self.start_fetch(self.ai, 'ai')


        # === Memes ===
        self.meme = TableWidget(10, 1)
        self.meme.setHorizontalHeaderLabels(['Meme'])
        self.meme.resizeColumnsToContents()
        self.layout.addWidget(self.meme, 0, 1)

        self.timer_meme = QTimer(self)
        self.timer_meme.timeout.connect(partial(self.start_fetch, self.meme, 'meme'))
        self.timer_meme.start(3000)
        self.start_fetch(self.meme, 'meme')


        # === Layer 3 ===
        self.l3 = TableWidget(10, 1)
        self.l3.setHorizontalHeaderLabels(['Layer 3'])
        self.l3.resizeColumnsToContents()
        self.layout.addWidget(self.l3, 1, 1)

        self.timer_l3 = QTimer(self)
        self.timer_l3.timeout.connect(partial(self.start_fetch, self.l3, 'L_3'))
        self.timer_l3.start(3000)
        self.start_fetch(self.l3, 'L_3')


        # === Layer 1 ===
        self.l1 = TableWidget(10, 1)
        self.l1.setHorizontalHeaderLabels(['Layer 1'])
        self.l1.resizeColumnsToContents()
        self.layout.addWidget(self.l1, 2, 1)

        self.timer_l1 = QTimer(self)
        self.timer_l1.timeout.connect(partial(self.start_fetch, self.ai, 'L_1'))
        self.timer_l1.start(3000)
        self.start_fetch(self.l1, 'L_1')


        # === Dexchange ===
        self.dexchange = TableWidget(10, 1)
        self.dexchange.setHorizontalHeaderLabels(['Dex Exchange'])
        self.dexchange.resizeColumnsToContents()
        self.layout.addWidget(self.dexchange, 1, 2)

        self.timer_dexchange = QTimer(self)
        self.timer_dexchange.timeout.connect(partial(self.start_fetch, self.dexchange, 'dexchange'))
        self.timer_dexchange.start(3000)
        self.start_fetch(self.dexchange, 'dexchange')


        # === Liquid staking ===
        self.liquid_staking = TableWidget()
        self.liquid_staking.setHorizontalHeaderLabels(['Liquid Staking'])
        self.liquid_staking.resizeColumnsToContents()
        self.layout.addWidget(self.liquid_staking, 0, 2)

        self.timer_liquid_staking = QTimer(self)
        self.timer_liquid_staking.timeout.connect(partial(self.start_fetch, self.dexchange, 'liquid_staking'))
        self.timer_liquid_staking.start(3000)
        self.start_fetch(self.liquid_staking, 'liquid_staking')


        # === Layer 0 ===
        self.l0 = TableWidget()
        self.l0.setHorizontalHeaderLabels(['Layer 0'])
        self.l0.resizeColumnsToContents()
        self.layout.addWidget(self.l0, 2, 0)

        self.timer_l0 = QTimer(self)
        self.timer_l0.timeout.connect(partial(self.start_fetch, self.l0, 'L_0'))
        self.timer_l0.start(3000)
        self.start_fetch(self.l0, 'L_0')


        # === Layer 2 ===
        self.l2 = TableWidget()
        self.l2.setHorizontalHeaderLabels(['Layer 2'])
        self.l2.resizeColumnsToContents()
        self.layout.addWidget(self.l2, 2, 2)

        self.timer_l2 = QTimer(self)
        self.timer_l2.timeout.connect(partial(self.start_fetch, self.l2, 'L_2'))
        self.timer_l2.start(3000)
        self.start_fetch(self.l2, 'L_2')



        lists = [self.l1, self.l0, self.l2, self.liquid_staking, self.meme, self.ai, self.payments, self.l3, self.dexchange]

        for idx, item in enumerate(lists):
            item.setItemDelegate(CenteredItemDelegate(item))


    def start_fetch(self, table, category):
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

            # Set row count and redraw table
            table.setRowCount(len(processed))
            table.setData(processed)
            table.setHorizontalHeaderLabels(['Coin', 'Open', 'High', 'Close', 'Low', 'Volume', 'Trades'])

            # Force GUI update
            table.viewport().update()
            table.resizeColumnsToContents()
        except Exception as e:
            logger.error(f"Error updating table for {category}: {str(e)}")

    def closeEvent(self, event):
        self.threadpool.clear()
        self.threadpool.waitForDone()
        super().closeEvent(event)

class FetcherSignals(QObject):
    dataFetched = pyqtSignal(dict)
    finished = pyqtSignal()

class DataFetcher(QRunnable):
    def __init__(self, coinprice, category):
        super().__init__()
        self.coinprice = coinprice
        self.category = category
        self.signals = FetcherSignals()

    def run(self):
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
