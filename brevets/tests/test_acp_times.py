"""
Nose tests for acp_times.py

Write your tests HERE AND ONLY HERE.
"""

import nose    # Testing framework
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)

import sys
sys.path.append("/brevets")

import arrow

from acp_times import open_time, close_time

def test_1():
    
    start_time = '2023-02-21T00:00'    

    start_time = arrow.get(start_time, 'YYYY-MM-DDTHH:mm')

    assert open_time(150, 0, start_time)

    assert close_time(150, 0, start_time) 

def test_2():

    start_time = '2023-02-21T00:00'

    start_time = arrow.get(start_time, 'YYYY-MM-DDTHH:mm')

    assert open_time(-100, 200, start_time)

    assert close_time(-100, 200, start_time)

def test_3():
    
    start_time = '2023-02-21T00:00'

    start_time = arrow.get(start_time, 'YYYY-MM-DDTHH:mm')

    assert open_time(20, 200, start_time)

    assert close_time(20, 200, start_time)

def test_4():

    start_time = '2023-02-21T00:00'

    start_time = arrow.get(start_time, 'YYYY-MM-DDTHH:mm')

    assert open_time(445, 600, start_time)
    assert close_time(445, 600, start_time)

    assert open_time(750, 1000, start_time)
    assert close_time(750, 1000, start_time)

def test_5():

    start_time = '2023-02-21T00:00'

    start_time = arrow.get(start_time, 'YYYY-MM-DDTHH:mm')

    assert open_time(400, 1000, start_time)
    assert close_time(400, 1000, start_time)

    assert open_time(75, 200, start_time)
    assert close_time(75, 200, start_time)