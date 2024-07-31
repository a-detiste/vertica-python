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

"""
CancelRequest message

The frontend sends a CancelRequest message to cancel the processing of the
current operation. The cancel request must be sent across a new connection to
the server. The server will process this request and then close the connection.

The cancel request might or might not have any effect. If the cancellation is
effective, the current command will terminate early and return an error message.
If the cancellation fails (e.g. the server has finished processing the command),
then there will be no visible result at all.
"""

from __future__ import annotations

from struct import pack

from ..message import BulkFrontendMessage


class CancelRequest(BulkFrontendMessage):
    message_id = None

    def __init__(self, backend_pid, backend_key):
        BulkFrontendMessage.__init__(self)
        self._backend_pid = backend_pid   # The process ID of the target backend
        self._backend_key = backend_key   # The secret key of the target backend

    def read_bytes(self):
        bytes_ = pack('!3I', 80877102, self._backend_pid, self._backend_key)
        return bytes_
