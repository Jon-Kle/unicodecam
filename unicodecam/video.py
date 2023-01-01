
from datetime import datetime
import time
import os

from unicodecam.errors import FrameSizeError
from unicodecam.utils import create_cmd, compress

class Video:
    '''
    A class to create an ascii video.
    '''
    # gather data till a frame gets finished
    # at finish the time will be taken in seconds
    # if no time has been take before, the time command will be ignored
    # else add the time command to the start of the frame
    def __init__(self):
        self.last_frame = ''
        self.current_frame = ''
    
    def add_to_frame(self, data:str):
        '''
        Add data to current frame.
        '''
        self.current_frame += data

    def finish_frame(self):
        '''
        Finish current frame and save it.
        '''
        # compare with previous frame
        frame = compare(self.current_frame, self.last_frame)
        # compress the result
        compressed_frame = compress(frame)
        # generate the timestamp (timestamp before the data of the frame)
        # add the finished frame to the complete data
        # empty current_frame and save it in last_frame
        self.last_frame = self.current_frame
        self.current_frame = ''

    def add_frame(self, data:str):
        '''
        Add a frame with the given data and finish it instantly.
        '''
        self.current_frame = data
        ...
    
    def finish(self):
        '''
        Finish video.
        '''
        ...

def compare(frame:str, last:str) -> str:
    # if they are not of equal length, raise exception
    if len(frame) != len(last):
        raise FrameSizeError('The new frame must be of equal length as the last frame')
    
    jump_count = 0
    result = ''

    # compare each character
    for i, char in enumerate(frame):
        # if they are indifferent, increment counter
        if char == last[i]:
            jump_count += 1
        # if they are different
        else:
            # handle different jump_count numbers
            if jump_count > 4:
                result += create_cmd('j', str(jump_count))
            else:
                result += last[i-jump_count:i]
            jump_count = 0
            
            # add current character to result, because it is different from the old one
            result += char

    return result