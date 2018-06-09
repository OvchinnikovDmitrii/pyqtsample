#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
import MainWindow as MWnd

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    mw = MWnd.MainWindow()
    mw.showMaximized()
    sys.exit(app.exec())