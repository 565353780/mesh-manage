#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Channel(object):
    def __init__(self):
        self.name = ""
        self.value = 0
        self.size = 0
        self.type = ""
        self.count = 1
        return

    def updateName(self):
        if self.name in ["x", "y", "z", "nx", "ny", "nz"]:
            self.size = 4
            self.type = "F"
            self.count = 1
            return True
        if self.name in ["r", "g", "b", "rgb", "instance_label"]:
            self.size = 4
            self.type = "U"
            self.count = 1
            return True
        self.size = 4
        self.type = "F"
        self.count = 1
        return True

    def setName(self, name):
        self.name = name
        return self.updateName()

    def updateValue(self):
        if self.type == "F":
            self.value = float(self.value)
            return True
        if self.type == "U":
            self.value = int(self.value)
            return True
        if self.type == "I":
            self.value = int(self.value)
            return True
        return True

    def setValue(self, value):
        self.value = value
        self.updateValue()
        return True

    def outputInfo(self, info_level=0):
        line_start = "\t" * info_level
        print(line_start + "[INFO][Channel]")
        print(line_start + "\t name: " + self.name)
        print(line_start + "\t value: " + str(self.value))
        print(line_start + "\t size: " + str(self.size))
        print(line_start + "\t type: " + self.type)
        print(line_start + "\t count: " + str(self.count))
        return True

