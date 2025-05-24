import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QGridLayout
from pyqtgraph import TableWidget

class WatchlistManager(QWidget):
    def __init__(self):
        super().__init__()

        self.data_manager = Data()

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        payments = TableWidget(10, 6)
        payments.setData(self.data_manager.get_watchlist_by_key('payments'))
        payments.setHorizontalHeaderLabels(['Payments'])
        payments.resizeColumnsToContents()
        self.layout.addWidget(payments, 0, 0)


        ai = TableWidget(10, 1)
        ai.setData(self.data_manager.get_watchlist_by_key('ai'))
        ai.setHorizontalHeaderLabels(['AI'])
        ai.resizeColumnsToContents()
        self.layout.addWidget(ai, 1, 0)


        meme = TableWidget(10, 1)
        meme.setData(self.data_manager.get_watchlist_by_key('meme'))
        meme.setHorizontalHeaderLabels(['Meme'])
        meme.resizeColumnsToContents()
        self.layout.addWidget(meme, 0, 1)


        analytics = TableWidget(10, 1)
        analytics.setData(self.data_manager.get_watchlist_by_key('analytics'))
        analytics.setHorizontalHeaderLabels(['Analytics'])
        analytics.resizeColumnsToContents()
        self.layout.addWidget(analytics, 1, 1)


        dexchange = TableWidget(10, 1)
        dexchange.setData(['BNB'])
        dexchange.setHorizontalHeaderLabels(['Dex Exchange'])
        dexchange.resizeColumnsToContents()
        self.layout.addWidget(dexchange, 0, 2)


        computing = TableWidget(10, 1)
        computing.setData(['Sample'])
        computing.setHorizontalHeaderLabels(['Computing & Infrastructure'])
        computing.resizeColumnsToContents()
        self.layout.addWidget(computing, 1, 2)


        sports = TableWidget()
        sports.setData(['Maclaren'])
        sports.setHorizontalHeaderLabels(['Sports'])
        sports.resizeColumnsToContents()
        self.layout.addWidget(sports, 2, 1)









class Data:
    def __init__(self):
        self.watchlists = {
            "payments": ["BTC", "XRP", "BCH", "ARK", "PEPE", "TRX", "DOGE", "VRA", "DOGE"],
            "ai": ["LTC", "AI", "TOKEN", "TAO", "NEAR"],
            "meme": ["FART", "TRUMP", "SHIB", "BONK", "NOT", "MOODENCY", "BOME", "PEOPLE", "JELLYJELLY", ],
            "analytics": ["ARKM", "CGPT"]
        }

    def get_watchlist_by_key(self, key):
        return [[item] for item in self.watchlists.get(key, [])]
