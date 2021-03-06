# Thanks to Erik Daguerre https://github.com/wolfthefallen/py-GtkSourceCompletion-example/blob/master/main.py

import re
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '4')
from gi.repository import Gtk, GtkSource, GObject

class Plugin():

	def __init__(self, app):
		self.name = "simple_completion"
		self.app = app
		self.THE = app.plugins_manager.THE
		self.commands = []
		self.custom_completors = []	

	def activate(self):

#		1)
#		Set up a provider that get words from what has already been entered
#		in the gtkSource.Buffer that is tied to the GtkSourceView
		
		source_view = self.THE("sourceview_manager", "source_view", None)
		self.view_completion = source_view.get_completion()
		self.view_autocomplete = GtkSource.CompletionWords.new('Words')
		self.view_autocomplete.register(source_view.get_buffer())
		self.view_completion.add_provider(self.view_autocomplete)
				
		# 3) Set up our custom provider for syntax completion.
#		custom_completion_provider = CustomCompletionProvider()
#		self.view_completion.add_provider(custom_completion_provider)
#		self.custom_completion_provider = custom_completion_provider

	
	def add_completion(self, header, words_arr):
		keybuff = GtkSource.Buffer()
		keybuff.begin_not_undoable_action()
		keybuff.set_text('\n'.join(words_arr))
		keybuff.end_not_undoable_action()
		autocomplete = GtkSource.CompletionWords.new(header)
		autocomplete.register(keybuff)
		self.custom_completors.append(autocomplete)
	

	# to add newly opened file words to autocompletion
	# update_completion is called when opened new file (if needed)
	# sometimes we need to avoid adding new words from big files
	# so it is up to you to call this method when open new file
	# the default sourceview_manager calls update_completion
	# for every new sourceview creation (see sourceview_manager)
	def update_completion(self, source_view):
		view_completion = source_view.get_completion()
		
		for ac in self.custom_completors:
			view_completion.add_provider(ac)

		self.view_autocomplete.register(source_view.get_buffer())
		view_completion.add_provider(self.view_autocomplete)





# class CustomCompletionProvider(GObject.GObject, GtkSource.CompletionProvider):
# 	"""
# 	This is a custom Completion Provider
# 	In this instance, it will do 2 things;
# 	1) always provide Hello World! (Not ideal but an option so its in the example)
# 	2) Utilizes the Gtk.TextIter from the TextBuffer to determine if there is a jinja
# 	example of '{{ custom.' if so it will provide you with the options of foo and bar.
# 	if select it will insert foo }} or bar }}, completing your syntax
# 	PLEASE NOTE the GtkTextIter Logic and regex are really rough and should be adjusted and tuned
# 	to fit your requirements
# 	# Implement the Completion Provider
# 	# http://stackoverflow.com/questions/32611820/implementing-gobject-interfaces-in-python
# 	# https://gist.github.com/andialbrecht/4463278 (Python example implementing TreeModel)
# 	# https://developer.gnome.org/gtk3/stable/GtkTreeModel.html (Gtk TreeModel interface specification)
# 	# A special thank you to @zeroSteiner
# 	"""
# 
# 	# apparently interface methods MUST be prefixed with do_
# 	def do_get_name(self):
# 		return 'Custom'
# 
# 	def do_match(self, context):
# 		# this should evaluate the context to determine if this completion
# 		# provider is applicable, for debugging always return True
# 		return True
# 
# 	def do_populate(self, context):
# 		proposals = [
# 			GtkSource.CompletionItem(label='Hello World!', text='Hello World!', icon=None, info=None)  # always proposed
# 		]
# 
# 		# found difference in Gtk Versions
# 		end_iter = context.get_iter()
# 		if not isinstance(end_iter, Gtk.TextIter):
# 			_, end_iter = context.get_iter()
# 
# 		if end_iter:
# 			buf = end_iter.get_buffer()
# 			mov_iter = end_iter.copy()
# 			if mov_iter.backward_search('{{', Gtk.TextSearchFlags.VISIBLE_ONLY):
# 				mov_iter, _ = mov_iter.backward_search('{{', Gtk.TextSearchFlags.VISIBLE_ONLY)
# 				left_text = buf.get_text(mov_iter, end_iter, True)
# 			else:
# 				left_text = ''
# 
# 			if re.match(r'.*\{\{\s*custom\.$', left_text):
# 				proposals.append(
# 					GtkSource.CompletionItem(label='foo', text='foo1 }}')  # optionally proposed based on left search via regex
# 				)
# 				proposals.append(
# 					GtkSource.CompletionItem(label='bar', text='bar }}')  # optionally proposed based on left search via regex
# 				)
# 
# 		context.add_proposals(self, proposals, True)
# 		return
