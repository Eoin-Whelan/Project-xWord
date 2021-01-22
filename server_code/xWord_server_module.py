"""
  Title:   xWord_server_module
  Author:  Eoin Farrell
  DOC:     20/01/2021
"""

import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.server

@anvil.server.callable
def import_dictionary():
  fStr = app_files.words_txt.get_bytes()
  fStr = str(fStr, "utf-8")
  fStr = fStr.split()
  fSet = {line.strip("'s").lower() for line in fStr}
  fSet = sorted(fSet)[1::]
  print(fSet[:30])
  return fSet[:30]
  

def find_possible_matches(pattern):
  
    """Given any pattern of the type "__a___b__c", this function
       looks up and returns all the potential matches for the
       pattern in the Linux dictionary of words."""
    fStr = app_files.words_txt.get_bytes()
    fStr = str(fStr, "utf-8")
    fStr = fStr.split()
    fSet = {line.strip("'s").lower() for line in fStr}
    fSet = sorted(fSet)[1::]
    def match_pattern(w, p):
        """Returns True if 'w' matches 'p', False otherwise."""
        letters = {k: v for k, v in enumerate(p) if v != "_"}
        return not any([w[i] != p[i] for i in letters.keys()])

    pattern = pattern.lower()  # Just in case...
    matches = {
        word  ## SELECT...
        for word in words  ## FROM...
        if len(word) == len(pattern) and match_pattern(word, pattern)  ## WHERE...
    }
    return matches
  
word_dict = import_dictionary()