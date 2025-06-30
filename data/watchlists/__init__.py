from PyQt5 import QtWidgets, QtCore

class CenteredItemDelegate(QtWidgets.QStyledItemDelegate):
    """Centers cell contents."""

    def initStyleOption(self, option, index):
        """Set the centering."""
        super().initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter
