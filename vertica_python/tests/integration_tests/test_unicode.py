# Copyright (c) 2018-2024 Open Text.
# Copyright (c) 2018 Uber Technologies, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Copyright (c) 2013-2017 Uber Technologies, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import annotations

from .base import VerticaPythonIntegrationTestCase


class UnicodeTestCase(VerticaPythonIntegrationTestCase):
    def test_unicode_query(self):
        value = '\u16a0'
        query = "SELECT '{0}'".format(value)

        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(query)
            res = cur.fetchone()

        self.assertEqual(value, res[0])

    def test_unicode_list_parameter(self):
        values = ['\u00f1', 'foo', 3]
        query = "SELECT {0}".format(", ".join(["%s"] * len(values)))

        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(query, tuple(values))
            results = cur.fetchone()

        for val, res in zip(values, results):
            self.assertEqual(val, res)

    def test_unicode_named_parameter_binding(self):
        values = ['\u16b1', 'foo', 3]
        keys = ['\u16a0', 'foo', 3]

        query = "SELECT {0}".format(", ".join([":{0}".format(key) for key in keys]))

        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(query, dict(zip(keys, values)))
            results = cur.fetchone()

        for val, res in zip(values, results):
            self.assertEqual(val, res)

    def test_string_query(self):
        value = 'test'
        query = "SELECT '{0}'".format(value)

        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(query)
            res = cur.fetchone()

        self.assertEqual(value, res[0])

    def test_string_named_parameter_binding(self):
        key = 'test'
        value = 'value'
        query = "SELECT :{0}".format(key)

        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(query, {key: value})
            res = cur.fetchone()

        self.assertEqual(value, res[0])

    # unit test for issue #160
    def test_null_named_parameter_binding(self):
        key = 'test'
        value = None
        query = "SELECT :{0}".format(key)

        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(query, {key: value})
            res = cur.fetchone()

        self.assertEqual(value, res[0])

    # unit test for issue #160
    def test_null_list_parameter(self):
        values = ['\u00f1', 'foo', None]
        query = "SELECT {0}".format(", ".join(["%s"] * len(values)))

        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(query, tuple(values))
            results = cur.fetchone()

        for val, res in zip(values, results):
            self.assertEqual(val, res)
