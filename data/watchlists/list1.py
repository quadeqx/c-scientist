from PyQt5.QtWidgets import QWidget, QGridLayout
from pyqtgraph import TableWidget
from PyQt5 import QtWidgets, QtCore
from data.coins.coin_data import coinprice, Data

class WatchlistManager(QWidget):
    def __init__(self):
        super().__init__()

        self.data_manager = Data()
        self.coinprice = coinprice()

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        payments = TableWidget(10, 6)
        data0 = self.coinprice.getprices('payments')
        processed = self.coinprice.prepare_table_data(data0)
        payments.setData(processed)
        payments.setHorizontalHeaderLabels(['Payments'])
        payments.resizeColumnsToContents()
        self.layout.addWidget(payments, 0, 0)


        ai = TableWidget(10, 1)
        data1 = self.coinprice.getprices('ai')
        ai.setData(self.coinprice.prepare_table_data(data1))
        ai.setHorizontalHeaderLabels(['AI'])
        ai.resizeColumnsToContents()
        self.layout.addWidget(ai, 1, 0)


        meme = TableWidget(10, 1)
        meme_data = self.coinprice.getprices('meme')
        meme.setData(self.coinprice.prepare_table_data(meme_data))
        meme.setHorizontalHeaderLabels(['Meme'])
        meme.resizeColumnsToContents()
        self.layout.addWidget(meme, 0, 1)


        l3 = TableWidget(10, 1)
        l3_data = self.coinprice.getprices('L_3')
        l3.setData(self.coinprice.prepare_table_data(l3_data))
        l3.setHorizontalHeaderLabels(['Layer 3'])
        l3.resizeColumnsToContents()
        self.layout.addWidget(l3, 1, 1)


        l1 = TableWidget(10, 1)
        l1_data = self.coinprice.getprices('L_1')
        l1.setData(self.coinprice.prepare_table_data(l1_data))
        l1.setHorizontalHeaderLabels(['Layer 1'])
        l1.resizeColumnsToContents()
        self.layout.addWidget(l1, 2, 1)


        dexchange = TableWidget(10, 1)
        dexchange_data = self.coinprice.getprices('dexchange')
        dexchange.setData(self.coinprice.prepare_table_data(dexchange_data))
        dexchange.setHorizontalHeaderLabels(['Dex Exchange'])
        dexchange.resizeColumnsToContents()
        self.layout.addWidget(dexchange, 1, 2)


        liquid_staking = TableWidget()
        liquid_staking_data = self.coinprice.getprices('liquid_staking')
        liquid_staking.setData(self.coinprice.prepare_table_data(liquid_staking_data))
        liquid_staking.setHorizontalHeaderLabels(['Liquid Staking'])
        liquid_staking.resizeColumnsToContents()
        self.layout.addWidget(liquid_staking, 0, 2)


        l0 = TableWidget()
        l0_data = self.coinprice.getprices('L_0')
        l0.setData(self.coinprice.prepare_table_data(l0_data))
        l0.setHorizontalHeaderLabels(['Layer 0'])
        l0.resizeColumnsToContents()
        self.layout.addWidget(l0, 2, 0)


        l2 = TableWidget()
        l2_data = self.coinprice.getprices('L_2')
        l2.setData(self.coinprice.prepare_table_data(l2_data))
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



