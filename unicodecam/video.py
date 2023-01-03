
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
    # gather data till a frame gets finished
    # at finish the time will be taken in seconds
    # if no time has been take before, the time command will be ignored
    # else add the time command to the start of the frame
    def __init__(self, name:str=''):
        self.name = name
        self.last_frame = None
        self.last_time = None # has to be initialized before the first frame finishes
        self.current_frame_data = []
        self.data =  ''

        # statistics
        self.total_time = 0
        self.frame_count = 0
    
    def add_to_frame(self, data:str):
        '''
        Add data to current frame.
        '''
        if self.last_time is None:
            self.last_time = time.time()
        self.current_frame_data.append(data)

    def finish_frame(self):
        '''
        Finish current frame and save it.
        '''
        now = time.time()
        current_frame_data = ''.join(self.current_frame_data)
        if self.last_frame is None:
            frame = current_frame_data
            header = ''
            # print('took the first route')
        else:
            # print('took the second route')
            # compare with previous frame
            frame = compare(current_frame_data, self.last_frame)
            # get the time difference between frames
            time_diff = now - self.last_time
            self.last_time = now

            time_diff_cmd = create_cmd('t', str(time_diff))
            self.total_time += time_diff # statistics
            header = RS + time_diff_cmd

        # compress and assemble frame
        finished_frame = header + compress(frame)
        self.data += finished_frame

        self.last_frame = current_frame_data
        # print('this is the last frame after everything:', self.last_frame)
        self.last_time = now
        self.current_frame_data = []
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
        # add metadata (timestamp)
        metadata_str = f'Total time: {self.total_time}s\n'\
            f'Total frames: {self.frame_count}\n'\
            # add format and average fps

        metadata = create_cmd('M', metadata_str)
        print(repr(metadata))
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
    
    timestamp = ''

    # if name is empty, set name and timestamp to be used in the filename
    if name == '':
        name = 'unicodecam_'
        # generate a timestamp for the filename
        timestamp = get_timestamp()

    # optional filename extension if file already exists
    file_num = 0
    file_num_str = ''

    file_ext = '.ucvid'

    while True:
        filename = name + timestamp + file_num_str + file_ext
        if not os.path.exists(filename):
            return filename
        else:
            file_num += 1
            file_num_str = f'({file_num})'

def compare(frame:str, last:str) -> str:
    # if they are not of equal length, raise exception
    # raw_frame = re.sub(r'\x1b[^m]*m', '', frame)
    # raw_last = re.sub(r'\x1b[^m]*m', '', last)
    # len_frame = len([c for c in frame if ord(c) > 31 or ord(c) == 9])
    # len_last = len([c for c in last if ord(c) > 31 or ord(c) == 9])
    if len(frame) != len(last):
    # if len(raw_frame) != len(raw_last):
        print(len(frame), len(last))
        # print(frame)
        # print(last)
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

