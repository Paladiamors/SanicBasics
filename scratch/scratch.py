'''
Created on May 17, 2020

@author: justin
'''

import datetime

def test_datetime():
    now = datetime.datetime.utcnow()
    ts = now.timestamp()
    print(ts)
    
    now2 = datetime.datetime.utcfromtimestamp(ts)
    print(now, now2)


class InOut:
    
    def __init__(self):
        
        print("the class was created")
        
    
    def __del__(self):
        print("the class was deleted")
        

def ioTest():
    io = InOut()
    
    
ioTest()