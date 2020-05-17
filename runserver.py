'''
Created on May 17, 2020

@author: justin

Runs the server from the command line
'''

import argparse
from sanic_server import create_app

argparser = argparse.ArgumentParser(description="starts the app server")
argparser.add_argument("--port", default=8000)
argparser.add_argument("--host", default="0.0.0.0")

args = argparser.parse_args()
app = create_app()
app.run(args.host, port=args.port)

