#!/usr/bin/python2.5

class AppError(Exception):
    """Simple BoPunk Error messages.

    Could use this to implement bopunk pop-up messages in case of errors.
    """
    def __init__(self, description, exit=False, *args):
        """basic error class, includes description. """
        Exception.__init__(self, description, *args)
        self.desc = description
        self.appexit = exit

class VarWidgetException(Exception):
    """exception for var widget use."""
    pass

class DeviceError(Exception):
    """exception for device/firmware communication errors. """
    pass


if __name__ == '__main__':
    raise AppError("Test",exit=True)
