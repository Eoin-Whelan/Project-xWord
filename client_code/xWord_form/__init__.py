from ._anvil_designer import xWord_formTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server

class xWord_form(xWord_formTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)


  def search_word_btn_click(self, **event_args):
    """search_word_btn_click populates pattern_results repeating panel with items matching entered pattern from word_pattern_box."""
    
    # Assigns the items of the repeating panel with the value of
    self.pattern_matches_panel.items = anvil.server.call('find_possible_matches', self.word_pattern_box.text)




