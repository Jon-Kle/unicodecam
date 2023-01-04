
from datetime import datetime
# import re
import time
import os

from .errors import FrameSizeError
from .utils import create_cmd, compress, RS, get_timestamp

class Video:
    '''
    A class to create an ascii video.
    '''
    def __init__(self, name:str=''):
        self.name = name # filename without extension
        self.current_frame_data = [] # gathered snippets of the current frame
        self.data = '' # processed recording data
        self.last_frame = None # set after first frame has finished
        self.last_time = None # set before first frame finishes

        # statistics
        self.total_time = 0
        self.frame_count = 0
    
    def add_to_frame(self, data:str):
        '''
        Add data to current frame.
        '''
        self.current_frame_data.append(data)

    def finish_frame(self):
        '''
        Finish current frame and save it.
        '''
        now = time.time()
        current_frame = ''.join(self.current_frame_data)
        if self.last_frame is None:
            frame = current_frame
            header = ''
            self.last_time = now
        else:
            # compare with previous frame
            frame = compare(current_frame, self.last_frame)
            
            # time difference between frames
            time_diff = now - self.last_time
            time_diff_cmd = create_cmd('t', str(time_diff))

            self.total_time += time_diff # statistics
            self.last_time = now

            # assemble header
            header = f'{RS}\n{time_diff_cmd}'

        # compress and assemble frame
        finished_frame = header + compress(frame)
        self.data += finished_frame

        self.last_frame = current_frame
        self.current_frame_data.clear()
        self.frame_count += 1

    def add_frame(self, data:str):
        '''
        Add a frame with the given data and finish it instantly.
        '''
        self.add_to_frame(data)
        self.finish_frame()
    
    def finish(self):
        '''
        Finish video.
        '''
        # add metadata
        timestamp = get_timestamp(invert=True)
        duration = self.total_time
        row_count = self.last_frame.count('\n')
        column_count = len(self.last_frame)//row_count-1 # -1 because \n does not count
        fps = round(self.frame_count/self.total_time, 1)
        metadata_str = f'\ntime: {timestamp}'\
            f'\nduration: {duration}s'\
            f'\nformat: {column_count}x{row_count} (width, height)'\
            f'\nframes: {self.frame_count}'\
            f'\nfps: {fps}\n'
            # add format and average fps

        metadata = create_cmd('M', metadata_str)
        # assemble
        self.data = ''.join([metadata, self.data])
        filename = get_filename(self.name)
        # save
        with open(filename, 'w') as f:
            f.write(self.data)

def get_filename(name:str) -> str:
    '''
    Return a filename consisting of the name, a timestamp, an optional number 
    if this file already exists and the extension".ucimg". 

    If a name is given, the standard name and the timestamp will be replaced by it.
    '''
    name_parts = [
        name, # name
        '', # timestamp
        '', # file number (optional)
        '.ucvid' # file extension
    ]
    # if no filename is given
    if name == '':
        name_parts[0], name_parts[1] = 'unicodecam_', get_timestamp()
    # for distinguishing files with the same name
    file_num = 0
    # for not creating multiple files with the same name 
    while True:
        filename = ''.join(name_parts)
        if not os.path.exists(filename):
            return filename
        else:
            file_num += 1
            name_parts[2] = f'({file_num})'

def compare(frame:str, last:str) -> str:

    # for color support
    # raw_frame = re.sub(r'\x1b[^m]*m', '', frame)
    # raw_last = re.sub(r'\x1b[^m]*m', '', last)
    # len_frame = len([c for c in frame if ord(c) > 31 or ord(c) == 9])
    # len_last = len([c for c in last if ord(c) > 31 or ord(c) == 9])

    if len(frame) != len(last):
        raise FrameSizeError('The new frame must be of equal length as the last frame')
    
    jump_count = 0
    result = ''
    result_data = []

    # compare each character
    for i, char in enumerate(frame):
        # if they are indifferent, increment counter
        if char == last[i]:
            jump_count += 1
        # if they are different
        else:
            # handle different jump_count numbers
            if jump_count > 4:
                result_data.append(create_cmd('j', str(jump_count)))
            else:
                result_data.append(last[i-jump_count:i])
            jump_count = 0
            
            # add current character to result, because it is different from the old one
            result += ''.join(result_data)
            result_data = []
    else:
        # if jump is higher than 0
        if jump_count > 0:

            if jump_count > 4:
                result += create_cmd('j', str(jump_count))
            else:
                result += last[-jump_count:]

    return result
