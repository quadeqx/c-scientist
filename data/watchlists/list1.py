import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QGridLayout
from pyqtgraph import TableWidget
from PyQt5 import QtWidgets, QtCore, QtGui

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


        l3 = TableWidget(10, 1)
        l3.setData(self.data_manager.get_watchlist_by_key('L_3'))
        l3.setHorizontalHeaderLabels(['Layer 3'])
        l3.resizeColumnsToContents()
        self.layout.addWidget(l3, 1, 1)


        l1 = TableWidget(10, 1)
        l1.setData(self.data_manager.get_watchlist_by_key('L_1'))
        l1.setHorizontalHeaderLabels(['Layer 1'])
        l1.resizeColumnsToContents()
        self.layout.addWidget(l1, 2, 1)


        dexchange = TableWidget(10, 1)
        dexchange.setData(self.data_manager.get_watchlist_by_key('dexchange'))
        dexchange.setHorizontalHeaderLabels(['Dex Exchange'])
        dexchange.resizeColumnsToContents()
        self.layout.addWidget(dexchange, 1, 2)


        liquid_staking = TableWidget()
        liquid_staking.setData(self.data_manager.get_watchlist_by_key('liquid_staking'))
        liquid_staking.setHorizontalHeaderLabels(['Liquid Staking'])
        liquid_staking.resizeColumnsToContents()
        self.layout.addWidget(liquid_staking, 0, 2)


        l0 = TableWidget()
        l0.setData(self.data_manager.get_watchlist_by_key('L_0'))
        l0.setHorizontalHeaderLabels(['Layer 0'])
        l0.resizeColumnsToContents()
        self.layout.addWidget(l0, 2, 0)


        l2 = TableWidget()
        l2.setData(self.data_manager.get_watchlist_by_key('L_2'))
        l2.setHorizontalHeaderLabels(['Layer 2'])
        delegate = CenteredItemDelegate(l2)
        l2.setItemDelegate(delegate)
        l2.resizeColumnsToContents()
        self.layout.addWidget(l2, 2, 2)


        lists = [l1, l0, l2, liquid_staking, meme, ai, payments, l3, dexchange]

        for idx, item in enumerate(lists):
            item.setItemDelegate(CenteredItemDelegate(item))







class CenteredItemDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        # Set alignment to center for all cells
        option.displayAlignment = QtCore.Qt.AlignCenter


class Data:
    def __init__(self):
        self.watchlists = {
            "payments": ["BTC", "XRP", "BCH", "ARK", "PEPE", "TRX", "DOGE", "VRA", "DOGE"],
            "ai": ["LTC", "AI", "TOKEN", "TAO", "NEAR", "WLD", "AIXBT", "FET", "RENDER", "ALU", "FET"],
            "meme": ["FART", "TRUMP", "SHIB", "BONK", "NOT", "MOODENCY", "BOME", "PEOPLE", "JELLYJELLY", ],
            "analytics": ["ARKM", "CGPT"],
            "dexchange": ["BNB", "INJ", "FTT", "ARKM", "TKO"],
            "liquid_staking": ["WBETH", "LDO", "ANKR", "RPL", "LISTA", "OGN", "QI", "HAEDAL", "FIS", "CHESS"],
            "L_0": ["ATOM", "DOT", "DATA", "ZRO", "AVAX"],
            "L_1": ["HYPE", "ADA", "FIL", "TON", "APT", "TAO", "TIA", "KAVA", "PLUME", "XCN", "VANRY"],
            "L_2": ["OP", "MNT", "CYBER", "ARB", "STX", "IMX","DYDX", "SNX", "ZK", "ZRX","STRK", "*KERNEL",],
            "L_3": ["XAI","DEGEN", "ORBS", "GHST"]


        }

    def get_watchlist_by_key(self, key):
        return [[item] for item in self.watchlists.get(key, [])]
