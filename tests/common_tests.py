"""Test out the common module
"""
import unittest

from last_five.common import parse_dt, parse_line, OK


class TestCommon(unittest.TestCase):
    
    def test_parse_line_good(self):
        line = '127.0.0.1 - - [16/Aug/2014 04:45:18] "GET / HTTP/1.1" 200 32 0.0003'
        vals = parse_line(line)
        self.assertEqual(vals['status_code'], 200)

    def test_parse_line_bad(self):
        line = "\n\n\n"
        vals = parse_line(line)
        self.assertEqual(vals, None)

    def test_parse_dt(self):
        dtstr = '16/Aug/2014 04:45:18'
        val = parse_dt(dtstr)
    
    def test_parse_dt_bad(self):
        derp = 'asdfasd'
        try:
            parse_dt(derp)
            self.fail("Expect ValueError")
        except ValueError:
            pass
