'''
Created on May 17, 2020

@author: justin

Runs the server from the command line
'''

import argparse
from sanicServer import runServer

argparser = argparse.ArgumentParser(description="starts the app server")
argparser.add_argument("--port", default=8000)
argparser.add_argument("--host", default="0.0.0.0")
argparser.add_argument("--settings", default=None)
argparser.add_argument("--auto-reload", action="store_true")

args = argparser.parse_args()
runServer(**vars(args))
