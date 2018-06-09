from PyQt5.QtGui import QPolygonF
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QColor

class Object:
    def __init__(self, name="ObjectName", param1="2", param2="12"):
        self.childrens = []
        self.name = name
        self.properties = {}
        self.properties["name"] = name
        self.properties["param1"] = param1
        self.properties["param2"] = param2
        self.polygons = []
        self.color = QColor(55, 140, 55)
        self.parent = None

    def add_children(self, object):
        self.childrens.append(object)
        object.parent = self

    def description(self, indent=0):
        result = " " * 4 * indent + self.name + "\n"
        for key in self.properties.keys():
            result += " " * (4 * indent + 2) + key + " - " + str(self.properties[key]) + "\n"
        for children in self.childrens:
            result += children.description(indent + 1)
        return result


    # @staticmethod
def createPoly(x, y, w, h):
    return QPolygonF([QPointF(x, y), QPointF(x + w, y), QPointF(x + w, y + h), QPointF(x, y + h)])

