#!/usr/bin/env python

import os

from flask import Flask, send_from_directory, jsonify, abort, request
import plyvel
import json

from .eremote import ERemote, find_devices

class Server(object):

    def __init__(self,
                 port=8880,
                 db_dir='/tmp/web_eremote_mini_db',
                 web_sources=os.path.join(os.path.dirname(__file__), '../build/')):
        self.flask_port = port
        self.web_sources = web_sources
        self.flask_app = Flask('web_eremote_mini')
        self.device = None
        if os.path.exists(db_dir):
            print('Found db on {}'.format(db_dir))
        else:
            print('No db found on {} (Automatically create DB)'.format(db_dir))
        self.database = plyvel.DB(db_dir, create_if_missing=True)
        self.serve_apis()
        self.serve_local_files()
        self.register_error_handler()
        self.disable_cache()

    def serve_apis(self):
        self.flask_app.add_url_rule('/api/queryDevices', view_func=self.api_query_devices)
        self.flask_app.add_url_rule('/api/learn', view_func=self.api_learn)
        self.flask_app.add_url_rule('/api/remember', methods=['POST'], view_func=self.api_remember)
        self.flask_app.add_url_rule('/api/commands', view_func=self.api_commands)
        self.flask_app.add_url_rule('/api/sendByName/<command>', view_func=self.api_send_by_name)
        self.flask_app.add_url_rule('/api/deleteByName/<command>', view_func=self.api_delete_by_name)

    def api_send_by_name(self, command):
        if self.device is None:
            self.api_query_devices()
        # todo: check if key exists in DB
        code_utf8 = self.database.get(command.encode('utf-8'))
        self.device.send_code(json.loads(code_utf8.decode('utf-8')))
        return jsonify({'success': True})

    def get_all_commands(self):
        all_commands = []
        for key, _value in self.database:
            all_commands.append(key)
        return all_commands

    def api_delete_by_name(self, command):
        command_byte = command.encode('utf-8')
        found_in_db = False
        if command_byte in self.get_all_commands():
            found_in_db = True
            self.database.delete(command_byte)
        return jsonify({'found-in-db': found_in_db})

    def api_commands(self):
        all_commands = []
        for key, value in self.database:
            all_commands.append([key.decode('utf-8'), json.loads(value.decode('utf-8'))])
        return jsonify(all_commands)

    def register_error_handler(self):
        self.flask_app.register_error_handler(503, self.error_handler_json)

    def error_handler_json(self, e):
        return jsonify({'message': e.description['message']}), e.code

    def api_query_devices(self):
        devices = find_devices()
        if len(devices) == 0:
            abort(503, {'message': 'Cannot find any devices'})
        self.device = devices[0]
        return jsonify([d.mac for d in devices])

    def api_learn(self):
        if self.device is None:
            self.api_query_devices()
        ir_code = self.device.learn()
        return jsonify({'code': ir_code})

    def api_remember(self):
        print(request.headers['Content-Type'])
        # request.json['code'] does not have '[' and ']'.
        code = json.loads('[{}]'.format(request.json['code'])) # Array of integer values
        name = request.json['name']
        existed_in_db = False
        if self.database.get(name.encode('utf-8')):
            existed_in_db = True
        self.database.put(name.encode('utf-8'), json.dumps(code).encode('utf-8'))
        return jsonify({'existed-in-db': existed_in_db})

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
