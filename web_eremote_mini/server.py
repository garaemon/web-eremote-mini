#!/usr/bin/env python

import os

from flask import Flask, send_from_directory
import plyvel


class Server(object):

    def __init__(self,
                 port=8880,
                 db_dir='/tmp/web_eremote_mini_db',
                 web_sources=os.path.join(os.path.dirname(__file__), '../build/')):
        self.flask_port = port
        self.web_sources = web_sources
        self.flask_app = Flask('web_eremote_mini')
        if os.path.exists(db_dir):
            print('Found db on {}'.format(db_dir))
        else:
            print('No db found on {} (Automatically create DB)'.format(db_dir))
        self.database = plyvel.DB(db_dir, create_if_missing=True)
        # API entry points
        self.serve_local_files()
        self.disable_cache()

    def disable_cache(self):
        self.flask_app.after_request(self.no_cache_header)
    def no_cache_header(self, r):
        r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        r.headers["Pragma"] = "no-cache"
        r.headers["Expires"] = "0"
        r.headers['Cache-Control'] = 'public, max-age=0'
        return r

    def serve_local_files(self):
        self.flask_app.add_url_rule(
            '/', defaults={'path': 'index.html'}, view_func=self.serve_local_file_callback)
        self.flask_app.add_url_rule('/<path:path>', view_func=self.serve_local_file_callback)


    def serve_local_file_callback(self, path):
        return send_from_directory(self.web_sources, path)

    def run(self):
        'Run server with blocking procedure'
        try:
            self.flask_app.run(host='0.0.0.0', port=self.flask_port)
        finally:
            self.database.close()
