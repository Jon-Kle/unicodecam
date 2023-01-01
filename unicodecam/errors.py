
class FileFormatError(IOError):
    def __init__(self, reason):
        IOError.__init__(reason)
        self.reason = reason