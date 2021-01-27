"""
  Title:   pattern_results
  Author:  Eoin Farrell
  DOC:     23/01/2021
"""

from ._anvil_designer import pattern_resultsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files


class pattern_results(pattern_resultsTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

        # When the panel is created, the text label is set to the name of the item itself.
        self.pattern_content_label.text = self.item
