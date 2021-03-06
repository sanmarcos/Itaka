#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Itaka is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.
# 
# Itaka is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Itaka; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
# Copyright 2003-2009 Marc E.
# http://itaka.jardinpresente.com.ar
#
# $Id$

""" Itaka console output and logging engine """

import __builtin__

# Global output functions
def print_message(string):
    """
    Print wrapper.

    @type str: str
    @param str: Message
    """
    
    print '[*] %s' % (str(string))

def print_warning(*strings):
    """
    Print warning wrapper.

    @type *strings: anything
    @param *strings: Anything
    """

    print_message('WARNING: %s' % (" - ".join(str(item) for item in strings)))

def print_error(*strings):
    """
    Print error wrapper.

    @type *strings: anything
    @param *strings: Anything
    """

    print_message('ERROR: %s' % (" - ".join(str(item) for item in strings)))

def print_debug(*strings):
    """
    Print debug wrapper.

    @type *strings: anything
    @param *strings: Anything
    """

    print_message('DEBUG: %s' % (" - ".join(str(item) for item in strings)))

def print_type(*strings):
    """
    Print type wrapper.

    @type *strings: anything
    @param *strings: Anything
    """

    print_message('DEBUG: %s' % (" - ".join(str(type(item)) for item in strings)))

def print_dir(*strings):
    """
    Print dir wrapper.

    @type *strings: anything
    @param *strings: Anything
    """

    print_message('DEBUG: %s' % (" - ".join(str(dir(item)) for item in strings)))

# Register them for global use
__builtin__.print_m = print_message
__builtin__.print_e = print_error
__builtin__.print_w = print_warning
__builtin__.print_d = print_debug
__builtin__.print_t = print_type
__builtin__.print_dir = print_dir

class BaseMessage:
    """
    Base class for console output.
    """

    def __init__(self, message):
        """
        Constructor.

        @type message: str
        @param message: The message to print on the Console
        """

        self.message = message
        print_message(self.message)

class BaseFailureMessage(BaseMessage):
    """
    Base class for failure messages.
    """

    def __init__(self, debug, caller, message, type):
        """
        Constructor

        @type debug: bool
        @param debug: Whether the L{caller} arguments will be printed

        @type caller: tuple
        @param caller: Specifies the class and method were the failure ocurred

        @type message: str
        @param message: The message to print

        @type type: str
        @param type: The type of failure: 'WARNING', 'ERROR', 'DEBUG'
        """

        self.caller = '.'.join(caller)
        self.message = message
        self.debug = debug
        self.type = type

        if self.debug:
            self.message = ' '.join((self.caller, self.message))

        print '[*] %s: %s' % (str(self.type), str(self.message))
                

class Console:
    """
    Console I/O handler organized by message type. Also handle GUI logging when passed an instance
    """

    def __init__(self, itaka_globals):
        """
        Constructor for console output handler
        
        @type itaka_globals: module
        @param itaka_globals: Configuration module globals
        """

        self.itaka_globals = itaka_globals
        if self.itaka_globals.console_verbosity['debug']:
            BaseMessage(_('Itaka %(version)s (r%(revision)s) starting') % {'version': self.itaka_globals.__version__, 'revision': self.itaka_globals.__revision__.split()[1]})
        elif self.itaka_globals.console_verbosity['normal']: 
            BaseMessage(_('Itaka %s starting') % (self.itaka_globals.__version__))
            
    def message(self, message):
        """
        Message handler
        
        @type message: str
        @param message: Message to print to the console
        """
        
        if self.itaka_globals.console_verbosity['normal']:
            BaseMessage(message)

    def failure(self, caller, message, failure_type='ERROR'):
        """
        Failure handler abstract

        @type caller: tuple
        @param caller: Specifies the class and method were the warning ocurred

        @type message: str
        @param message: Message to print to the console

        @type failure_type: str
        @param failure_type: What kind of failure it is, either 'ERROR' (default), 'WARNING' or 'DEBUG'
        """

        if failure_type == 'ERROR':
            if not self.itaka_globals.console_verbosity['quiet']:
                BaseFailureMessage(self.itaka_globals.console_verbosity['quiet'], caller, message, failure_type)

        elif failure_type == 'WARNING':
            if self.itaka_globals.console_verbosity['normal']:
                BaseFailureMessage(self.itaka_globals.console_verbosity['normal'], caller, message, failure_type)

        elif failure_type == 'DEBUG':
            if self.itaka_globals.console_verbosity['debug']:
                BaseFailureMessage(self.itaka_globals.console_verbosity['debug'], caller, message, failure_type)

