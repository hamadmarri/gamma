#
#### Author: Hamad Al Marri <hamad.s.almarri@gmail.com>
#### Date: Feb 11th, 2020
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#
#
#	files_manager: is responsible to manage all opened documents.
#
#
#

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from . import files_manager_commands as commands

from .file import File
from .create_file_mixin import CreateFileMixin
from .close_file_mixin import CloseFileMixin
from .open_file_mixin import OpenFileMixin


class Plugin(CreateFileMixin, CloseFileMixin, OpenFileMixin):
	
	def __init__(self, app):
		self.name = "files_manager"
		self.app = app
		self.signal_handler = app.signal_handler
		self.builder = app.builder
		self.plugins = app.plugins_manager.plugins
		self.sourceview_manager = app.sourceview_manager
		self.commands = []
		self.files = []
		self.current_file = None
		self.counter = 1
		
	
	def activate(self):
		self.signal_handler.key_bindings_to_plugins.append(self)
		
		commands.set_commands(self)
		
		# default empty file when open editor with no opened files
		self.current_file = File("empty", self.sourceview_manager.source_view, new_file=True, init_file=True)

		# add empty/current_file to files array
		self.files.append(self.current_file)
				
	
	# key_bindings is called by SignalHandler
	def key_bindings(self, event, keyval_name, ctrl, alt, shift):		
		# close current file is bound to "<Ctrl>+w"
		# TODO: check if need saving before close
		if ctrl and keyval_name == "w":
			# close current_file
			self.close_current_file()
		elif shift and ctrl and keyval_name == "W":
			self.close_all()
			
	
	
	def rename_file(self, file_object, filename):
		# check if it is the new init file, need to be added to ui
		if file_object.init_file:
			file_object.init_file = False	# not init anymore	
			file_object.filename = filename
			self.plugins["ui_manager.ui_manager"].add_filename_to_ui(file_object)
		
		# if new file added by the user
		else:
			# rename in array
			file_object.filename = filename
			self.plugins["ui_manager.ui_manager"].rename_file(file_object)
			
		
		
	
	# handler of "clicked" event
	# it switch the view to the filename in clicked button
	def side_file_clicked(self, filename):
	
		# is_already_openned gets the index of the file in "files" array
		file_index = self.is_already_openned(filename)
		
		# if found, which should!, switch to it
		if file_index >= 0:
			self.switch_to_file(file_index) 
	
	
	
	
	
	def switch_to_file(self, file_index):
		# check if it is the current_file, then exit method 
		if self.current_file == self.files[file_index]:
			return
				
		# get file object
		f = self.files[file_index]
		
		# replace the source view 
		self.plugins["ui_manager.ui_manager"].replace_sourceview_widget(f.source_view)
				
		# reposition file in files list
		del self.files[file_index]
		self.files.append(f)
		self.current_file = f
				
		# update headerbar to filename
		self.plugins["ui_manager.ui_manager"].update_header(f.filename)
		
		
		
		
		
	# returns file index if found or -1
	def is_already_openned(self, filename):
		for i, f in enumerate(self.files):
			print(f"{filename} {f.filename} {filename == f.filename}")
			if filename == f.filename:
				return i	
		return -1
		
		
		
		
