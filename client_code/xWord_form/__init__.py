from ._anvil_designer import xWord_formTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server

class xWord_form(xWord_formTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    anvil.server.call('import_dictionary')
    # Any code you write here will run when the form opens.


  def search_word_btn_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.pattern_matches_panel.items = anvil.server.call('import_dictionary')
    pass




