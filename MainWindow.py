from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, \
    QTableView, QTreeView, QAction,  qApp, QGraphicsView, QGraphicsScene, \
    QPushButton
from PyQt5.QtCore import *
from PyQt5.QtGui import QColor
import DataStructures
import ObjectsModel
import PropertiesModel

# Наследуемся от QMainWindow
class MainWindow(QMainWindow):
    # Переопределяем конструктор класса
    def __init__(self):
        # Обязательно нужно вызвать метод супер класса
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(480, 80))  # Устанавливаем размеры
        self.setWindowTitle("Line Edit IP Address")  # Устанавливаем заголовок окна
        central_widget = QWidget(self)  # Создаём центральный виджет
        self.setCentralWidget(central_widget)  # Устанавливаем центральный виджет

        hbox_layout = QHBoxLayout(self)  # Создаём QGridLayout
        central_widget.setLayout(hbox_layout)  # Устанавливаем данное размещение в центральный виджет

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

    def rebuildModel(self, index=QModelIndex()):
        self.tree_model.initRoot(self.items)
        self.tree_view.expandAll()

        # if index == QModelIndex() or not index.isValid(): #sometimes crushes, enable to select item by index
        index = self.tree_model.index(0, 0)

        self.onClicked(index)

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

    def onClicked(self, index=QModelIndex()):
        object = index.data(Qt.UserRole + 1)
        # object = DataStructures.Object
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
        self.rebuildModel(self.tree_view.currentIndex())

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
