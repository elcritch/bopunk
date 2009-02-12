#!/usr/bin/python2.5

class AppError(Exception):
    def __init__(self, description, exit=False, *args):
        """docstring for __init__"""
        Exception.__init__(self, description, *args)
        self.desc = description
        self.appexit = exit

class VarWidgetException(Exception):
    pass

class DeviceError(Exception): 
    pass


if __name__ == '__main__':
    raise AppError("Test",exit=True)