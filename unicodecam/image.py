from .utils import compress as __compress, get_timestamp as __get_timestamp
import os

def take_picture(data:str, name:str = ''):
    '''Take a "picture" using data and a optional name for the file'''
    Image(data, name)

class Image:
    '''
    This class gives the possibility to create "images" from strings.

    An object of this class gathers the strings it has been given and 
    stores them in a textfile with the extension ".ucimg" or ".uccimg" 
    if compressed is true.
    A created file with the extension ".ucimg" can be opened and read 
    line a normal textfile. A file with extension ".uccimg" though 
    contains some special characters that might reduce readability.

    Attributes:
    -----------
    data:
        The gathered data as a string
    name:
        The name of the file that will be created 
        (the file extension stays the same)
    timestamp:
        If true, a timestamp will be added to the end of the image
    compressed:
        If true, the data will get compressed before being written into the file.
    
    Methods:
    --------
    add_data(data:str):
        Takes a string and adds it to data
    finish():
        Finish the "image" by storing all the data in a textfile 
        with the extension ".ucimg"
    '''
    def __init__(self, data:str = '', name:str = '',timestamp=False, compressed=False, finish=True):
        '''
        Create an Image object.

        Parameters:
        -----------
        data:str = ''
            Will be added to the data of the "image".
        name:str = ''
            Changes the name of the file that will be created.
            If empty, the file will have the name "unicodecam" with a timestamp.
        compressed = False:
            If true, the data will be compressed before being written into the file.
        finish = True
            If left True and data is given, the object will create a file instantly.
            If no data is given or finish is False, the object will wait 
            till the finish() method is called.
        '''
        self.data = data
        self.name = name
        self.timestamp = timestamp
        self.compressed = compressed
        if finish and bool(self.data):
            self.finish()

    def add_data(self, data:str):
        '''Add a string to the end of the already gathered data.'''
        self.data += str(data)

    def finish(self):
        '''
        Create a file containing the gathered data.
        If compressed is true, the data will be compressed before being written 
        into the file. The data will not be deleted from the object.
        '''
        # generate filename
        data = self.data
        if self.timestamp:
            data += __get_timestamp()
        filename = __get_filename(self.name, self.compressed)
        if self.compressed:
            data = __compress(data)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(data)
    
def __get_filename(name:str, compressed:bool) -> str:
    '''
    Return a filename consisting of the name, a timestamp, an optional number 
    if this file already exists and the extension".ucimg". 

    If compressed is True, the extension will be ".uccimg".

    If a name is given, the standard name and the timestamp will be replaced by it.
    '''
    
    timestamp = ''

    # if name is empty, set name and timestamp to be used in the filename
    if name == '':
        name = 'unicodecam_'
        # generate a timestamp for the filename
        timestamp = __get_timestamp()

    # optional filename extension if file already exists
    file_num = 0
    file_num_str = ''

    file_ext = '.ucimg'
    if compressed:
        file_ext = '.uccimg'

    while True:
        filename = name + timestamp + file_num_str + file_ext
        if not os.path.exists(filename):
            return filename
        else:
            file_num += 1
            file_num_str = f'({file_num})'
