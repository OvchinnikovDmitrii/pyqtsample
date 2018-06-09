from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, \
    QTableView, QTreeView, QAction,  qApp, QGraphicsView, QGraphicsScene, \
    QPushButton
from PyQt5.QtCore import *
from PyQt5.QtGui import QColor
import DataStructures
import ObjectsModel
import PropertiesModel


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(480, 80))
        self.setWindowTitle("PyQtSample")
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        hbox_layout = QHBoxLayout(self)
        central_widget.setLayout(hbox_layout)

        buttons_background = QWidget(self)
        buttons_layout = QHBoxLayout()
        buttons_background.setLayout(buttons_layout)

        self.add_button = QPushButton("Add")
        buttons_layout.addWidget(self.add_button)

        self.remove_button = QPushButton("Remove")
        buttons_layout.addWidget(self.remove_button)

        tree_layout = QVBoxLayout(self)
        self.tree_view = QTreeView();
        self.tree_view.header().hide()
        self.tree_view.setMaximumWidth(300)
        self.tree_model = ObjectsModel.TreeModel()
        self.tree_view.setModel(self.tree_model)
        tree_layout.addWidget(buttons_background)
        tree_layout.addWidget(self.tree_view)

        hbox_layout.addLayout(tree_layout)

        self.graphics_view = QGraphicsView();
        self.scene = QGraphicsScene();
        self.graphics_view.setScene(self.scene)
        hbox_layout.addWidget(self.graphics_view)

        self.properties_view = QTableView();
        self.properties_view.setMaximumWidth(300)
        self.properties_model = PropertiesModel.TableModel()
        self.properties_view.setModel(self.properties_model)
        hbox_layout.addWidget(self.properties_view)

        self.init_menu()
        self.test()
        self.connectSignals()

    def connectSignals(self):
        self.add_button.clicked.connect(self.onAddClicked)
        self.remove_button.clicked.connect(self.onRemoveClicked)
        self.tree_view.clicked.connect(self.onClicked)
        self.properties_model.dataChanged.connect(self.onPropertyChanged)

    def onPropertyChanged(self):
        self.rebuildModel()

    def rebuildModel(self):
        #save index hierarhy
        indexes = []
        tmp_index = self.tree_view.currentIndex()
        indexes.append(tmp_index)
        while tmp_index.parent().isValid():
            indexes.append(tmp_index.parent())
            tmp_index = tmp_index.parent()

        self.tree_model.initRoot(self.items)
        self.tree_view.expandAll()

        if len(indexes) == 0:
            self.onClicked(self.tree_model.index(0,0))
        else:
            last_index = indexes.pop(-1)
            index = self.tree_model.index(last_index.row(), last_index.column())
            #restore index hierarchy
            while len(indexes) > 0:
                last_index = indexes.pop(-1)
                index = self.tree_model.index(last_index.row(), last_index.column(), index)

            if index.isValid():
                self.onClicked(index)
            else:
                self.onClicked(self.tree_model.index(0, 0))

    def init_menu(self):
        exit_action = QAction("&Exit", self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(qApp.quit)
        file_menu = self.menuBar()
        file_menu.addAction(exit_action)

    def appendObjectOnScene(self, object = DataStructures.Object):
        if object.rect.isValid():
            self.scene.addRect(object.rect, object.color)
        for child in object.childrens:
            self.appendObjectOnScene(child)

    def onClicked(self, index):
        object = index.data(Qt.UserRole + 1)

        self.properties_model.initProperties(object)

        self.scene.clear()
        self.appendObjectOnScene(object)
        self.tree_view.setCurrentIndex(index)

    def onAddClicked(self):
        index = self.tree_view.currentIndex()
        print(index)
        object = index.data(Qt.UserRole + 1)
        print(object.description())
        object.add_children(DataStructures.Object("New item"))
        self.rebuildModel()

    def onRemoveClicked(self):
        index = self.tree_view.currentIndex()
        object = index.data(Qt.UserRole + 1)
        if not object.parent:
            self.items.remove(object)
        else:
            object.parent.childrens.remove(object)

        self.rebuildModel()


    def test(self):
        self.items = []
        static = DataStructures.Object("Static", DataStructures.createRect(0, 0, 800, 200))
        static.add_children(DataStructures.Object("child_1"))
        static.add_children(DataStructures.Object("child_2"))
        static.add_children(DataStructures.Object("child_3"))
        static.color = QColor(200, 0, 0).name()
        static.childrens[0].add_children(DataStructures.Object("child_1.1", DataStructures.createRect(40, 40, 80, 40)))

        self.items.append(static)

        dynamic = DataStructures.Object("Dynamic", DataStructures.createRect(0, 0, 200, 800))
        dynamic.add_children(DataStructures.Object("child_1"))
        dynamic.add_children(DataStructures.Object("child_2"))
        dynamic.add_children(DataStructures.Object("child_3"))
        dynamic.childrens[2].add_children(DataStructures.Object("child_2.1"))
        dynamic.color = QColor(0, 0, 200).name()
        self.items.append(dynamic)

        self.rebuildModel()
