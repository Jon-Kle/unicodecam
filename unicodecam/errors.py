
class FileFormatError(IOError):
    def __init__(self, reason):
        IOError.__init__(reason)
        self.reason = reason

class FrameSizeError(Exception):
    def __init__(self, reason):
        Exception.__init__(self, reason)
        self.reason = reason