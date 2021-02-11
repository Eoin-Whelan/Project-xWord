import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
"""
  Title:   xWord_server_module
  Author:  Eoin Farrell
  DOC:     20/01/2021
"""

import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server


@anvil.server.callable
def import_dictionary():
    """
    Imports the words_txt file through the Anvil Google Drive API.
    It then converts to bytes and casts to a string before applying the string-relevant
    functions to transform and return it as a list.
    """
    fStr = app_files.words_txt.get_bytes()
    fStr = str(fStr, "utf-8")
    fStr = fStr.split('\n')
    fSet = {line.replace("'s", "").lower() for line in fStr}
    fSet = sorted(fSet)[1::]
    return fSet


@anvil.server.callable
def find_possible_matches(pattern):
    """Given any pattern of the type "__a___b__c", this function
    looks up and returns all the potential matches for the
    pattern in the Linux dictionary of words."""
    dict_contents = import_dictionary()
    dict_contents.extend([result["words"] for result in app_tables.new_words.search()])
    def match_pattern(w, p):
        # Returns True if 'w' matches 'p', False otherwise.
        letters = {k: v for k, v in enumerate(p) if v != "_"}
        return not any([w[i] != p[i] for i in letters.keys()])

    pattern = pattern.lower()  # Just in case...
    matches = {
        word  ## SELECT...
        for word in dict_contents  ## FROM...
        if len(word) == len(pattern) and match_pattern(word, pattern)  ## WHERE...
    }
    matches = sorted(list(matches))
    return matches
  
@anvil.server.http_endpoint('/stats')
def stats(**q):
  new_words = len({result['words'] for result in app_tables.new_words.search()})
  return {"New words added": new_words, "Old words:": len(import_dictionary())}

@anvil.server.http_endpoint('/add', methods=["POST"], authenticate_users=False)
def add(**q):
  new_words = anvil.server.request.body_json['words']
  old_dict = import_dictionary()
  new_dict = [result["words"] for result in app_tables.new_words.search()]
  valid_adds = [word for word in map(str.lower,new_words) if word not in map(str.lower,new_dict) and word not in import_dictionary()]
  print(valid_adds)
  if(valid_adds):
    for word in valid_adds:
      app_tables.new_words.add_row(words=word)
    

@anvil.server.http_endpoint('/pattern/:pat')
def stats(**q):
  new_words = len({result['words'] for result in app_tables.new_words.search()})
  return {"New words added": new_words, "Old words:": len(import_dictionary())}