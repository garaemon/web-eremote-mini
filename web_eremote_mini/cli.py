#!/usr/bin/env python

import os

import fire

from .server import Server

PROJECT_DIR = os.path.join(os.path.dirname(__file__), '..')

class CliApp(object):
    'Application class for cli usage'
    def serve(self, port=8880, database_directory=os.path.join(PROJECT_DIR, 'db')):
        'Run server'
        s = Server(port=port, db_dir=database_directory)
        s.run()


def main():
    'Entry point of web-eremote-mini'
    fire.Fire(CliApp)

