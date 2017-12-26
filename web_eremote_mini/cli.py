#!/usr/bin/env python

import fire

from .server import Server

class CliApp(object):
    'Application class for cli usage'
    def serve(self, port=8880):
        'Run server'
        s = Server(port=port)
        s.run()


def main():
    'Entry point of web-eremote-mini'
    fire.Fire(CliApp)

