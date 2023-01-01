class Log:
    '''
    A class to log into a file.
    '''
    def __init__(self, filename:str):
        self.file = filename
        self.data = ''
    
    def entry(self, data:str):
        # add a line to the log file
        with open(self.file, mode='a') as f:
            f.write(data + '\n')
