import subprocess
import time
import re
import sys
from datetime import datetime
from collections import defaultdict
import threading
import Queue

from last_five.common import parse_line, OK

FIVE_MINUTES = 60*5

queue = Queue.Queue()


def flush(outputfile, queue, flush_interval=FIVE_MINUTES):
    """For each flush interval read the queued data and compute count"""

    last_flush = int(time.time())
    next_flush = last_flush + flush_interval
    count = 0
    while True:
        while True:
            try:
                val = queue.get_nowait()
            except Queue.Empty:
                break
            if val['epoch'] > next_flush:
                # put back for next time
                queue.put(val)
                break
            if val['status_code'] not in OK:
                count += 1
        now = int(time.time())
        if now > next_flush:
            with open(outputfile, 'a') as fd:
                msg = "%s %s %s\n" % (last_flush+1, next_flush, count)
                fd.write(msg)
            last_flush = next_flush
            next_flush = next_flush + FLUSH_INTERVAL
            count = 0
        time.sleep(1)


def readem(request_log_file, queue):
    """Tail given file and add parsed lines to queue"""

    f = subprocess.Popen(['tail','-F', '-n0', request_log_file],\
            stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    while True:
        line = f.stdout.readline()
        values = parse_line(line)
        queue.put(values)


def main():
    if len(sys.argv) != 3:
        print "Usage: tail_five <reqlog file> <output file>"
        sys.exit(2)
    
    request_log_file = sys.argv[1]
    output_file = sys.argv[2]

    treadem = threading.Thread(target=readem, args=(request_log_file, queue))
    treadem.daemon = True
    treadem.start()

    tflush = threading.Thread(target=flush, args=(output_file, queue, 10))
    tflush.daemon = True
    tflush.start()

    while True:
        time.sleep(1)


if __name__ == '__main__':
    main()
