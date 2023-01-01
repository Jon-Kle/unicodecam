from .errors import FileFormatError
import time
from datetime import datetime

APC = '\x9f'
TS = '\x9c'
RS = '\x1e'

def compress(data:str) -> str:
    compressed = ''
    char_count = 1
    last_char = ''
    # get every character in data
    for char in data:
        if last_char == char:
            char_count += 1
        else:
            compressed += last_char
            # if the character repeats for more than 5 times
            if char_count > 5:
                # insert command "r" (repeat) with the character count
                compressed += create_cmd('r', int(char_count-1))
            else:
                # if it repeats less than 5 times, print the characters
                compressed += last_char*(char_count-1)
            char_count = 1
        last_char = char
    # handle the last character, because the loop doesn't
    else:
        compressed += last_char
        if char_count > 5:
            compressed += f'{APC}r{char_count-1}{TS}'
        else:
            compressed += last_char*(char_count-1)
        char_count = 1
    return compressed

def decompress(data:str) -> str:
    decompressed = ''
    last_char = ''
    i = 0
    while i < len(data):
        if data[i] == APC:
            cmd, arg, length = read_cmd(data[i:])
            i += length
            arg = int(arg)
            if cmd == 'r':
                decompressed += last_char*arg
            else:
                raise FileFormatError(f"The file command {cmd} can't be used in .uccimg")
        else:
            decompressed += data[i]
        last_char = data[i]
        i += 1
    return decompressed

def create_cmd(cmd:str, arg:str) -> str:
    '''
    Create a command in the format: APC, cmd, arg, TS.
    cmd has to be only 1 character long.
    '''
    if len(cmd) != 1:
        raise ValueError("Argument doesn't meet the conditions")
    return f'{APC}{cmd}{arg}{TS}'

def read_cmd(text:str) -> tuple:
    '''
    Take a text of which the first character is APC.
    Read the characters till TS. Return the first character of the read command as cmd
    and the other characters as arg.
    Also return the length of the command+1

    Example:
        >>> cmd, arg, length = __read_cmd(data[i:])
        >>> i += length
        >>> arg = int(arg)
        >>> match cmd:
        >>>     case ...:
    '''
    if text[0] != APC:
        raise ValueError("Argument doesn't meet the conditions")
    cmd_str = ''
    i = 1
    while True:
        if text[i] == TS:
            break
        cmd_str += text[i]
        i += 1
    cmd = cmd_str[0]
    arg = cmd_str[1:]
    length = i
    return cmd, arg, length

def get_timestamp() -> str:
    '''
        Return a timestamp from year, month, day, hour, minute and second.
        '''
    # create filename timestamp
    timestamp = time.time()
    timestamp = datetime.fromtimestamp(timestamp)
    timestamp = timestamp.strftime('%Y.%m.%d_%H:%M:%S')
    return timestamp