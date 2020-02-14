import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from . import commands


class Plugin():
	
	def __init__(self, app):
		self.name = "highlight"
		self.app = app
		self.commands = []
		self.files_manager = None
		self.tag_name = "search-match"
#		self.tag = None

		
	def activate(self):
		pass
		
	def get_plugins_refs(self):
		# get files_manager
		if not self.files_manager:
			self.files_manager = self.app.plugins_manager.get_plugin("files_manager")
			
		
	def key_bindings(self, event, keyval_name, ctrl, alt, shift):
		pass
		
	
	def highlight_signal(self, buffer, location, mark):
		if mark.get_name() == "insert":
			iters = buffer.get_selection_bounds()

			if not iters:
				# remove highlight
				self.remove_highlight()
			else:
				(iter_start, iter_end) = iters
				search = buffer.get_text(iter_start, iter_end, False)
				self.highlight(search)
		
		
	def highlight(self, search):
		self.get_plugins_refs()
			
		self.remove_highlight()
		
		buffer = self.files_manager.current_file.source_view.get_buffer() 
		tag_table = buffer.get_tag_table();
			
		tag = Gtk.TextTag.new("search-match")
		style = buffer.get_style_scheme()
		search_tag = style.get_style("search-match")
		tag.props.background = search_tag.props.background
		tag_table.add(tag)

		start_iter = buffer.get_start_iter()
		matches = start_iter.forward_search(search, 0, None)
		while matches != None:
			(match_start, match_end) = matches
			buffer.apply_tag(tag, match_start, match_end)
			matches = match_end.forward_search(search, 0, None)
		
		
		
		
	def remove_highlight(self):
#		if not self.tag:
#			return
			
		self.get_plugins_refs()
		buffer = self.files_manager.current_file.source_view.get_buffer()
		tag_table = buffer.get_tag_table();
		tag = tag_table.lookup(self.tag_name)
		
		if not tag:
			return
			
		tag_table.remove(tag)
		buffer.remove_tag_by_name(self.tag_name, buffer.get_start_iter(), buffer.get_end_iter())
	
	