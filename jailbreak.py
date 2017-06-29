# MIT License

# Copyright (c) 2017 Bruno Rocha

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import lldb
import os
import shlex
import optparse
import sbt

def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand(
    'command script add -f jailbreak.begin_jailbreak_debugging jailbreak')
    debugger.HandleCommand('command alias enable_logging expression -lobjc -O -- extern void turn_on_stack_logging(int); turn_on_stack_logging(1);')


def begin_jailbreak_debugging(debugger, command, result, internal_dict):
    debugger.HandleCommand("platform select remote-ios")
    debugger.HandleCommand("process connect connect://localhost:6666")
