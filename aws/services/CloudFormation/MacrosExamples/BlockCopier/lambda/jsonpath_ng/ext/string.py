#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import re
from .. import DatumInContext, This


SUB = re.compile("sub\(/(.*)/,\s+(.*)\)")
SPLIT = re.compile("split\((.),\s+(\d+),\s+(\d+|-1)\)")


class DefintionInvalid(Exception):
    pass


class Sub(This):
    """Regex subtituor

    Concrete syntax is '`sub(/regex/, repl)`'
    """

    def __init__(self, method=None):
        m = SUB.match(method)
        if m is None:
            raise DefintionInvalid("%s is not valid" % method)
        self.expr = m.group(1).strip()
        self.repl = m.group(2).strip()
        self.regex = re.compile(self.expr)
        self.method = method
        print("%r" % self)

    def find(self, datum):
        datum = DatumInContext.wrap(datum)
        value = self.regex.sub(self.repl, datum.value)
        if value == datum.value:
            return []
        else:
            return [DatumInContext.wrap(value)]

    def __eq__(self, other):
        return (isinstance(other, Sub) and self.method == other.method)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.method)

    def __str__(self):
        return '`sub(/%s/, %s)`' % (self.expr, self.repl)


class Split(This):
    """String splitter

    Concrete syntax is '`split(char, segment, max_split)`'
    """

    def __init__(self, method=None):
        m = SPLIT.match(method)
        if m is None:
            raise DefintionInvalid("%s is not valid" % method)
        self.char = m.group(1)
        self.segment = int(m.group(2))
        self.max_split = int(m.group(3))
        self.method = method

    def find(self, datum):
        datum = DatumInContext.wrap(datum)
        try:
            value = datum.value.split(self.char, self.max_split)[self.segment]
        except Exception:
            return []
        return [DatumInContext.wrap(value)]

    def __eq__(self, other):
        return (isinstance(other, Sub) and self.method == other.method)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.method)

    def __str__(self):
        return '`%s`' % self.method
