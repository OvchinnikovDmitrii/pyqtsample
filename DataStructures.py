from PyQt5.QtCore import QPointF, QRectF
from PyQt5.QtGui import QColor

class Object:
    def __init__(self, name="ObjectName", rect=QRectF()):
        self.childrens = []
        self.properties = {}
        self.properties["name"] = name
        self.properties["x"] = rect.x()
        self.properties["y"] = rect.y()
        self.properties["w"] = rect.width()
        self.properties["h"] = rect.height()
        self.properties["color"] = QColor(55,155,55).name()
        self.parent = None

    @property
    def rect(self):
        return QRectF(float(self.properties["x"]), float(self.properties["y"]),
                      float(self.properties["w"]), float(self.properties["h"]))

    @property
    def color(self):
        return QColor(self.properties["color"])

    @color.setter
    def color(self, value):
        self.properties["color"] = value

    @property
    def name(self):
        return self.properties["name"]

    @name.setter
    def name(self, value):
        self.properties["name"] = value

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


def createRect(x, y, w, h):
    return QRectF(x, y, w, h)
