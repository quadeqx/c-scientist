from PyQt5 import QtWidgets, QtCore

class CenteredItemDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        # Set alignment to center for all cells
        option.displayAlignment = QtCore.Qt.AlignCenter
