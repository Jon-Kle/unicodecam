from datetime import datetime
import time
import os

class Video:
    '''
    A class to create an ascii video.
    '''
    # gather data till a frame gets finished
    # at finish the time will be taken in seconds
    # if no time has been take before, the time command will be ignored
    # else add the time command to the start of the frame
    def __init__(self):
        # add first frame
        self.current_frame = ''
        self.previous_frame = ''
        self.data = ''
        self.time_length = 0
        self.last_frame_time = None
    
    def add_to_frame(self, data:str):
        '''
        Add data to current frame.
        '''
        self.current_frame += data
        ...

    def finish_frame(self):
        '''
        Finish current frame and save it.
        '''
        t = time.time()
        ...

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