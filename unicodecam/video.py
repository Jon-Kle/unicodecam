
from datetime import datetime
import time
import os

from .errors import FrameSizeError
from .utils import create_cmd, compress, RS

class Video:
    '''
    A class to create an ascii video.
    '''
    # gather data till a frame gets finished
    # at finish the time will be taken in seconds
    # if no time has been take before, the time command will be ignored
    # else add the time command to the start of the frame
    def __init__(self):
        self.last_frame = None
        self.last_time = None # has to be initialized before the first frame finishes
        self.current_frame = ''
        self.data =  ''
    
    def add_to_frame(self, data:str):
        '''
        Add data to current frame.
        '''
        self.last_time = self.last_time or time.time()
        # if self.last_time is None:
        #     self.last_time = time.time()
        self.current_frame += data

    def finish_frame(self):
        '''
        Finish current frame and save it.
        '''
        now = time.time()
        if self.last_frame is None:
            frame = self.current_frame
            header = ''
        else:
            # compare with previous frame
            frame = compare(self.current_frame, self.last_frame)
            # get the time difference between frames
            time_diff = now - self.last_time
            self.last_time = now

            time_diff_cmd = create_cmd('t', str(time_diff))
            header = RS + time_diff_cmd

        # compress and assemble frame
        finished_frame = header + compress(frame)
        self.data += finished_frame

        self.last_frame = self.current_frame
        self.last_time = now
        self.current_frame = ''

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
        # assemble
        filename = 'unfinished'
        # filename naming convention unicodecam_Timestamp_optional-number.ucvid
        # save
        with open(filename, 'w') as f:
            f.write(self.data)

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
    else:
        # if jump is higher than 0
        if jump_count > 0:

            if jump_count > 4:
                result += create_cmd('j', str(jump_count))
            else:
                result += last[-jump_count:]

    return result