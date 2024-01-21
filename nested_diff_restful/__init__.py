# -*- coding: utf-8 -*-
#
# Copyright 2024 Michael Samoglyadov
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

"""REST API and web UI for nested-diff"""

__version__ = '1.0.0'
__author__ = 'Michael Samoglyadov'
__license__ = 'Apache License, Version 2.0'
__website__ = 'https://github.com/mr-mixas/Nested-Diff-RESTful'


def start_wsgi_server():
    import gunicorn.app.base
    import nested_diff_restful.api

    class WSGIServer(gunicorn.app.base.Application):
        def init(self, parser, opts, args):
            pass  # pragma nocover

        def load(self):
            return nested_diff_restful.api.app  # pragma nocover

    WSGIServer().run()
