#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 09:11:53 2025.

@author: quantum
"""

from . import *


class CandlestickItem(pg.GraphicsObject):
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.data = data  # DataFrame with columns: 'Date', 'Open', 'High', 'Low', 'Close'
        self.generatePicture()

    def generatePicture(self):
        self.picture = pg.QtGui.QPicture()
        p = pg.QtGui.QPainter(self.picture)

        w = 600  # Width of the candlestick (adjust as needed)
        for _, row in self.data.iterrows():
            t = row['Date']  # Use the timestamp from the 'Date' column
            open, high, low, close = row['Open'], row['High'], row['Low'], row['Close']

            # Draw the wick (high to low)
            p.setPen(pg.mkPen('g' if close > open else 'r'))
            p.drawLine(pg.QtCore.QPointF(t, low), pg.QtCore.QPointF(t, high))

            # Draw the candlestick body
            if open > close:
                p.setBrush(pg.mkBrush('r'))  # Red for bearish
                body_top = open
                body_bottom = close
            else:
                p.setBrush(pg.mkBrush('g'))  # Green for bullish
                body_top = close
                body_bottom = open

            # Ensure the height is positive
            body_height = abs(body_top - body_bottom)

            # Draw the rectangle
            p.setPen(pg.mkPen(None))  # No border for the body
            p.drawRect(pg.QtCore.QRectF(t - w, body_bottom, w * 2, body_height))

        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return pg.QtCore.QRectF(self.picture.boundingRect())


class PriceAndVolume(QWidget):
    def __init__(self):
        super().__init__()

        self.__df = pd.read_csv('data/BTCUSDT-2024-MAR.csv')

        if not all(col in self.__df.columns for col in ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']):
            raise ValueError("CSV file must contain 'Date', 'Open', 'High', 'Low', 'Close', and 'Volume' columns.")

        # Convert 'Date' column to datetime and then to Unix timestamps (in seconds)
        self.__df['Date'] = pd.to_datetime(self.__df['Date']).astype(int) / 1e9

        # Create a QVBoxLayout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        layout.setSpacing(0)  # Remove spacing between widgets

        # Create PyQtGraph PlotWidget for price plot
        self.__price_plot = pg.PlotWidget()
        self.__price_plot.showGrid(x=True, y=True)
        self.__price_plot.getAxis('left').setVisible(False)
        self.__price_plot.getAxis('right').setVisible(True)



        # Create candlestick item
        self.__candles = CandlestickItem(self.__df)
        self.__price_plot.addItem(self.__candles)
        self.__price_plot.getAxis('bottom').setVisible(False)

        # Adjust the y-axis range for the candlestick plot
        min_price = self.__df[['Low', 'Close']].min().min()
        max_price = self.__df[['High', 'Open']].max().max()
        self.__price_plot.setYRange(min_price, max_price, padding=0.01)

        # Create PyQtGraph PlotWidget for volume plot
        self.__volume_plot = pg.PlotWidget()
        self.__volume_plot.showGrid(x=True, y=True)
        self.__volume_plot.getAxis('left').setVisible(False)
        self.__volume_plot.getAxis('right').setVisible(True)
        self.__volume_plot.getAxis('bottom').setVisible(False)

        self.__plot_OI = pg.PlotWidget()
        self.__plot_OI.showGrid(x=False, y=True)
        self.__plot_OI.getAxis('left').setVisible(False)
        self.__plot_OI.getAxis('right').setVisible(True)
        self.__plot_OI.setXRange(7, 7*24)
        self.__plot_OI.setAxisItems({'bottom': DateAxisItem()})



        # Add plots to the layout
        layout.addWidget(self.__price_plot, stretch=2)  # Price plot takes 75% of the space
        layout.addWidget(self.__volume_plot, stretch=1)  # Volume plot takes 25% of the space
        layout.addWidget(self.__plot_OI, stretch=1)

        # Link price and volume x-axis
        self.__price_plot.setXLink(self.__volume_plot)
        self.__plot_OI.setXLink(self.__price_plot)

        # Plot volume histogram
        self.__plot_volume()

    def __plot_volume(self):
        # Create a bar graph item for the volume histogram
        x = self.__df['Date'].values
        y = self.__df['Volume'].values
        w = 600

        # Create a list of brushes for each bar
        open = self.__df['Open']
        close = self.__df['Close']
        brushes = [pg.mkBrush('g' if close[i] > open[i] else 'r') for i in range(len(self.__df))]

        # Create the bar graph item
        bargraph = pg.BarGraphItem(x=x, height=y, width=w * 2, brushes=brushes, pen=None)
        self.__volume_plot.addItem(bargraph)

        # Set the x-axis to use DatetimeAxis
        #self.__volume_plot.setAxisItems({'bottom': DateAxisItem(orientation='bottom')})

        # Adjust the y-axis range for the volume plot
        self.__volume_plot.setYRange(0, max(y) * 1.1)  # Add 10% padding

    def __plot_OI(self):
        plot = pg.PlotWidget()
