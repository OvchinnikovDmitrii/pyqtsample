from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem
import DataStructures


class TreeModel(QStandardItemModel):
    def __init__(self, parent=None):
        super(TreeModel, self).__init__(parent)

    def appendItem(self, parent, child):
        childItem = QStandardItem(child.name)
        childItem.setData(child)
        for subItem in child.childrens:
            self.appendItem(childItem, subItem)

        parent.appendRow(childItem)

    def initRoot(self, objects):
        self.clear()
        for object in objects:
            parentItem = QStandardItem(object.name)
            parentItem.setData(object)

            for subItem in object.childrens:
                self.appendItem(parentItem, subItem)

            self.appendRow(parentItem)


