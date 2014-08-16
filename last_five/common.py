import time
import re
from datetime import datetime
from collections import defaultdict

OK = range(200, 300)

# example: 127.0.0.1 - - [14/Aug/2014 15:29:39] "GET / HTTP/1.1" 200 32 0.0003
LINE_REGEX = '(?P<ip>[(\d\.)]+) - - \[(?P<dtstr>.*?)\] "(?P<req>.*?)" ' \
    '(?P<status_code>\d+) (?P<content_length>\d+) (?P<reqtime>\d+.\d+)'


def parse_dt(dtstr):
    b = datetime.strptime(dtstr, "%d/%b/%Y %H:%M:%S")
    return time.mktime(b.timetuple())


def parse_line(line):
    m = re.match(LINE_REGEX, line)
    if not m:
        return None
    vals = m.groupdict()
    epoch = parse_dt(vals['dtstr'])
    status_code = int(vals['status_code'])
    return {"status_code": status_code, "epoch": epoch}
