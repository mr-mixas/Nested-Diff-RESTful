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

from flask import Flask, Response, jsonify, render_template, request

from nested_diff import Differ, Patcher
from nested_diff.fmt import HtmlFormatter, TextFormatter, TermFormatter

app = Flask(__name__)


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
    # this page is almost never reloaded, so it is OK to embed css in it
    return render_template('index.html', html_fmt_css=HtmlFormatter.get_css())


@app.route('/ping')
def health_check():
    return Response('pong', status=200)


@app.route('/diff', methods=['POST'])
def diff():
    try:
        diff_opts = request.json.get('diff_opts', {'U': False})
    except AttributeError:
        return Response('Object expected', status=400)

    try:
        diff = Differ(**diff_opts).diff(
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


@app.route('/format', methods=['POST'])
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


@app.route('/patch', methods=['POST'])
def patch():
    try:
        return jsonify(Patcher().patch(
            request.json['target'],
            request.json['patch'],
        ))
    except Exception:
        return Response('Incorrect arguments', status=400)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
