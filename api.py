# -*- coding: utf-8 -*-
#
# Copyright 2021 Michael Samoglyadov
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from flask import Flask, Response, jsonify, render_template, request

from nested_diff import Differ, Patcher, TYPE_HANDLERS
from nested_diff.formatters import HtmlFormatter, TextFormatter, TermFormatter
from nested_diff.handlers import TextHandler


flask_kwargs = {}

for kw in ('static_folder', 'static_url_path', 'template_folder'):
    try:
        flask_kwargs[kw] = os.environ['NESTED_DIFF_REST_' + kw.upper()]
    except KeyError:
        pass

app = Flask(__name__, **flask_kwargs)


def format_diff_response(fmt, diff, opts):
    mimetype = 'text/plain'

    if fmt == 'text':
        formatter = TextFormatter
    elif fmt == 'term':
        formatter = TermFormatter
    elif fmt == 'html':
        formatter = HtmlFormatter
    else:
        return Response('Unsupported format ' + fmt, status=400)

    return Response(
        formatter(**opts).format(diff),
        status=200,
        mimetype=mimetype,
    )


@app.route('/')
def index():
    resp = Response(
        render_template('index.html'),
        mimetype='text/html',
        status=200,
    )
    resp.add_etag()
    resp.make_conditional(request)

    return resp


@app.route('/ping')
def health_check():
    return Response('pong', status=200)


@app.route('/api/v1/diff', methods=['POST'])
def diff():
    try:
        diff_opts = request.json.get('diff_opts', {'U': False})
    except AttributeError:
        return Response('Object expected', status=400)

    extra_handlers = []

    text_diff_ctx = diff_opts.pop('text_diff_ctx', -1)
    if text_diff_ctx >= 0:
        extra_handlers.append(TextHandler(context=text_diff_ctx))

    try:
        _, diff = Differ(
            handlers=TYPE_HANDLERS + tuple(extra_handlers),
            **diff_opts,
        ).diff(
            request.json.get('a', None),
            request.json.get('b', None),
        )
    except Exception:
        return Response('Incorrect options', status=400)

    ofmt = request.json.get('ofmt', 'json')
    if ofmt == 'json':
        return jsonify(diff)

    ofmt_opts = request.json.get('ofmt_opts', {})

    return format_diff_response(ofmt, diff, ofmt_opts)


@app.route('/api/v1/format', methods=['POST'])
def format():
    try:
        diff = request.json.get('diff', {})
        ofmt = request.json.get('ofmt', None)
        if ofmt is None:
            return jsonify(diff)

        ofmt_opts = request.json.get('ofmt_opts', {})

        return format_diff_response(ofmt, diff, ofmt_opts)
    except Exception:
        return Response('Incorrect arguments', status=400)


@app.route('/api/v1/patch', methods=['POST'])
def patch():
    try:
        return jsonify(Patcher().patch(
            request.json['target'],
            request.json['patch'],
        ))
    except Exception:
        return Response('Incorrect arguments', status=400)


@app.route('/api/v1/nested_diff.css')
def nested_diff_css():
    resp = Response(HtmlFormatter.get_css(), mimetype='text/css', status=200)
    resp.add_etag()
    resp.make_conditional(request)

    return resp


@app.route('/api/v1/nested_diff.js')
def nested_diff_script():
    resp = Response(
        HtmlFormatter().get_script(),
        mimetype='text/javascript',
        status=200,
    )
    resp.add_etag()
    resp.make_conditional(request)

    return resp


if __name__ == '__main__':
    app.run(
        host=os.environ.get('NESTED_DIFF_REST_HOST', 'localhost'),
        port=os.environ.get('NESTED_DIFF_REST_PORT', 8080),
        debug=True if 'NESTED_DIFF_REST_DEBUG' in os.environ else False,
    )
