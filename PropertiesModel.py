from PyQt5.QtCore import QAbstractTableModel, Qt
import DataStructures


class TableModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super(TableModel, self).__init__(parent)
        self.object = None

    def rowCount(self, parent=None):
        if not self.object:
            return 0
        return len(self.object.properties.keys())

    def columnCount(self, parent=None):
        if not self.object:
            return 0
        return 2

    def data(self, QModelIndex, role):
        if role != Qt.DisplayRole and role != Qt.EditRole:
            return None
        row = QModelIndex.row()
        column = QModelIndex.column()
        key = list(self.object.properties.keys())[row]
        if column == 0:
            return key
        if column == 1:
            return self.object.properties[key]
        return None

    def setData(self, index, value, role=Qt.EditRole):
        row = index.row()
        column = index.column()
        key = list(self.object.properties.keys())[row]
        if column == 1:
            self.object.properties[key] = str(value)
            self.dataChanged.emit(index, index)
        return True

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == 0:
                    return "Property"
                if section == 1:
                    return "Value"

        return QAbstractTableModel.headerData(self, section, orientation, role)

    def flags(self, index):
        if index.column() == 1:
            return Qt.ItemIsEnabled | Qt.ItemIsEditable
        return Qt.ItemIsEnabled

    def initProperties(self, object=DataStructures.Object()):
        self.beginResetModel()
        self.object = object
        self.endResetModel()


