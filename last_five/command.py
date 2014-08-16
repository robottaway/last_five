"""This script will take as input a CommonLogger format log and produce
a count of all non-200 status codes.
"""
import re
import sys
import os
import time

from last_five.common import parse_dt, parse_line, OK

FIVE_MINUTES = 5*60


def filerev(somefile, buffer=0x20000):
    """Generator read given file line by line in reverse and yield one line at a time.

    see SO:
    http://stackoverflow.com/questions/2301789/read-a-file-in-reverse-order-using-python
    """
    somefile.seek(0, os.SEEK_END)
    size = somefile.tell()
    lines = ['']
    rem = size % buffer
    pos = max(0, (size // buffer - 1) * buffer)
    while pos >= 0:
        somefile.seek(pos, os.SEEK_SET)
        data = somefile.read(rem + buffer) + lines[0]
        rem = 0
        lines = re.findall('[^\n]*\n?', data)
        ix = len(lines) - 2
        while ix > 0:
            yield lines[ix]
            ix -= 1
        pos -= buffer
    else:
        yield lines[0]


def main():
    if len(sys.argv) != 2:
        print "Usage: python last_five.py <file>"
        sys.exit(2)
    
    now = int(time.time()) 
    five_ago = now - FIVE_MINUTES
    count_not_ok = 0

    with open(sys.argv[1], 'r') as f:
      for line in filerev(f):
        vals = parse_line(line)
        code = vals['status_code']
        ts = vals['epoch']
        if ts > five_ago and ts <= now and code not in OK:
            count_not_ok += 1

    print "Found %s non-200 status codes" % (count_not_ok,)

if __name__ == "__main__":
    main()
