from ._anvil_designer import pattern_resultsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files

class pattern_results(pattern_resultsTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    
    # When the item is created, the text of the label is set to the name of the item itself.
    self.pattern_content_label.text = self.item
