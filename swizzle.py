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
import string
import random

def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand(
    'command script add -f swizzle.swizzle swizzle')


def swizzle(debugger, command, result, internal_dict):
    command_args = shlex.split(command)
    parser = generate_option_parser()
    try:
        (options, args) = parser.parse_args(command_args)
    except:
        result.SetError(parser.usage)
        return

    res = lldb.SBCommandReturnObject()
    interpreter = debugger.GetCommandInterpreter()

    expr_options = lldb.SBExpressionOptions()
    expr_options.SetIgnoreBreakpoints(True);
    expr_options.SetFetchDynamicValue(lldb.eNoDynamicValues);
    expr_options.SetTimeoutInMicroSeconds (30*1000*1000) # 30 second timeout
    expr_options.SetTryAllThreads (True)
    expr_options.SetUnwindOnError(True)
    expr_options.SetGenerateDebugInfo(True)
    expr_options.SetLanguage (lldb.eLanguageTypeObjC_plus_plus)
    expr_options.SetCoerceResultToId(True)
    frame = debugger.GetSelectedTarget().GetProcess().GetSelectedThread().GetSelectedFrame()
    command_script = generate_script(options)
    frame.EvaluateExpression (command_script, expr_options)

def generate_script(options):
    pointer_name = random_arg_name()
    swizzled_name = random_arg_name()
    command_script = ""
    emptyArgs = ")"
    if options.count > 0:
        emptyArgs = get_swizzle_args(options.count) + ")"
    command_script += r'''
                    @import com.saurik.substrate.MS;
                    BOOL (*'''+ pointer_name +''')(id self, SEL _cmd'''+ emptyArgs +''';
                    BOOL (^'''+ swizzled_name +''')(id, SEL'''+ ("id" * options.count) +''') = ^(id self, SEL _cmd'''+ emptyArgs +''' {
                        '''+ options.method +'''
                    };
                    MSHookMessageEx(
                    ['''+ options.cls +''' class], @selector('''+ options.selector +'''),
                    &'''+ swizzled_name +''', &'''+ pointer_name +'''
                    );
                    '''
    return command_script

def random_arg_name():
    return '$' + ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(14))

def get_swizzle_args(count):
    arg = ""
    for i in range(0,count):
        arg += ", id arg%d" % (i+1)
    return arg

def generate_option_parser():
    usage = ""
    parser = optparse.OptionParser(usage=usage, prog="swizzle")
    parser.add_option("-c", "--class",
                          action="store",
                          default="",
                          dest="cls",
                          help="Class to swizzle.")
    parser.add_option("-s", "--selector",
                          action="store",
                          default="",
                          dest="selector",
                          help="Selector to swizzle.")
    parser.add_option("-m", "--method",
                          action="store",
                          default="",
                          dest="method",
                          help="New method.")
    parser.add_option("-a", "--arg-count",
                      action="store",
                      default=0,
                      type="int",
                      dest="count",
                      help="Number of arguments of original method. (available on the swizzled method as arg1, arg2, etc")
    return parser
