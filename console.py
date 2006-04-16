#! /usr/bin/env python
# -*- coding: utf8 -*-
# Itaka Screenshooting Server (Twisted+GTK2) (Windows/Linux)
# Console handling
import globals as iglobals

class Console:
	""" Console I/O handler organized by message type. Also handle GUI logging for non-Twisted. """
	def __init__(self, ginstance):
		""" Init the console handler with the GUI instance. """
		self.igui = ginstance
		print "[*] Itaka %s starting up..." % (iglobals.version)
		
	def __del__(self):
		""" Destructor. """
		print "[*] Itaka shutting down..."
		
	def msg(self, message, gui=False):
		""" Message handler. """
		# The gui argument is for the FTP method. It couples the console logger with the GUI logger.
		# In the Twisted method, logging is done by its engine.
		# Note the peculiar syntax of the argument you must pass to logger.
		# A dict with the first key being 'message', coupled with a str()'ed tuple'd message.
		print "[*] %s" % (message)
		if gui: self.igui.logger({'message': [str(message)]})
		
	def warn(self, caller, message, gui=False):
		""" Warning handler. """
		self.array = ".".join(caller)
		print "[*] WARNING: %s: %s" % (self.array, message)
		if gui: self.igui.logger({'message': [str("[*] ERROR: %s: %s" % (self.array, message))]})		
		
	def debug(self, caller, message, gui=False):
		""" Debug handler. """
		self.array = ".".join(caller)
		print "[*] DEBUG: %s: %s" % (self.array, message)
		if gui: self.igui.logger({'message': [str("[*] ERROR: %s: %s" % (self.array, message))]})
		
	def error(self, caller, message, gui=False):
		""" Error handler. """
		self.array = ".".join(caller)
		print "[*] ERROR: %s: %s" % (self.array, message)
		if gui: self.igui.logger({'message': [str("[*] ERROR: %s: %s" % (self.array, message))]})
