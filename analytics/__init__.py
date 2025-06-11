import pyqtgraph as pg
from pyqtgraph import PlotWidget, InfiniteLine
from PyQt5.QtCore import Qt, QPointF


class CustomPlotWidget(PlotWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vLine = None
        self.hLine = None

    def setCrosshairs(self, vLine, hLine):
        self.vLine = vLine
        self.hLine = hLine

    def leaveEvent(self, event):
        if self.vLine and self.hLine:
            self.vLine.hide()
            self.hLine.hide()
        super().leaveEvent(event)


class CrosshairHandler:
    def __init__(self, plot_widget: CustomPlotWidget):
        self.plot_widget = plot_widget

        self.vLine = InfiniteLine(angle=90, movable=False, pen=pg.mkPen('white', width=1, style=Qt.DotLine))
        self.hLine = InfiniteLine(angle=0, movable=False, pen=pg.mkPen('white', width=1, style=Qt.DotLine))

        self.plot_widget.addItem(self.vLine, ignoreBounds=True)
        self.plot_widget.addItem(self.hLine, ignoreBounds=True)

        self.plot_widget.setCrosshairs(self.vLine, self.hLine)

        self.plot_widget.setMouseTracking(True)

        self.plot_widget.scene().sigMouseMoved.connect(self.mouseMoved)

    def mouseMoved(self, evt: QPointF):
        if self.plot_widget.sceneBoundingRect().contains(evt):
            mouse_point = self.plot_widget.getViewBox().mapSceneToView(evt)
            self.vLine.setPos(mouse_point.x())
            self.hLine.setPos(mouse_point.y())
            self.vLine.show()
            self.hLine.show()

__all__ = ['CustomPlotWidget', 'CrosshairHandler']
