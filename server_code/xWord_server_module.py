import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

"""
  Title:   xWord_server_module
  Author:  Eoin Farrell
  DOC:     20/01/2021
  Updated: 11/02/2021
  Log: - Added API endpoints add, stats and pat.
"""

import anvil.google.auth
import anvil.google.drive
from anvil.google.drive import app_files
import anvil.server


@anvil.server.callable
def import_dictionary():
    """
    Imports the words_txt file through the Anvil Google Drive API.
    It then converts to bytes and casts to a string
    before applying the string-relevant functions to
    transform and return it as a list.
    """
    fStr = app_files.words_txt.get_bytes()
    fStr = str(fStr, "utf-8")
    fStr = fStr.split("\n")
    fSet = {line.replace("'s", "").lower() for line in fStr}
    fSet = sorted(fSet)[1::]
    return fSet


@anvil.server.callable
def find_possible_matches(pattern):
    """
    Given any pattern of the type "__a___b__c", this function
    looks up and returns all the potential matches for the
    pattern in the Linux dictionary of words.
    """
    dict_contents = import_dictionary()
    data_table_dict = [result["words"] for result in app_tables.new_words.search()]
    data_table_dict_lower = map(str.lower, data_table_dict)
    dict_contents.extend(data_table_dict_lower)

    def match_pattern(w, p):
        # Returns True if 'w' matches 'p', False otherwise.
        letters = {k: v for k, v in enumerate(p) if v != "_"}
        return not any([w[i] != p[i] for i in letters.keys()])

    pattern = pattern.lower()  # Just in case...
    matches = {
        word  # SELECT...
        for word in dict_contents  # FROM...
        if len(word) == len(pattern) and match_pattern(word, pattern)  # WHERE...
    }
    matches = sorted(list(matches))
    return matches


@anvil.server.http_endpoint("/stats")
def stats(**q):
    """
    Returns a dict/JSON structure object containing the information.
    """
    new_dict = {result["words"] for result in app_tables.new_words.search()}
    return {"New words: ": len(new_dict), "Old words: ": len(import_dictionary())}


@anvil.server.http_endpoint("/add", methods=["POST"], authenticate_users=False)
def add(**q):
    """
    add API endpoint allows the passing of a
    JSON object which is parsed to a dict new_words.
    A new list is built from the compliment set of
    new_words compared to the old dictionary (text file)
    and new dictionary (data table) contents.

    Provided the list is not null (i.e. at least one non-duplicate),
    it's contents are added to the new words dictionary table.
    """
    new_words = anvil.server.request.body_json["words"]
    new_dict = [result["words"] for result in app_tables.new_words.search()]
    new_words = [word for word in map(str.lower, new_words)]
    new_dict = [word for word in map(str.lower, new_dict)]
    old_dict = import_dictionary()
    valid_adds = [word for word in new_words if word not in new_dict and old_dict]
    """
    valid_adds = [
        word
        for word in new_words
        if word not in new_dict
    ]
    valid_adds.extend([
        word
        for word in valid_adds
        if word not in import_dictionary()
      ]
    )
    """

    if valid_adds:
        for word in valid_adds:
            app_tables.new_words.add_row(words=word)


@anvil.server.http_endpoint("/pattern/:pat")
def pattern(pat):
    """
    pattern API endpoint takes an argument passed in via the :pat
    variable and creates a dictionary of the results. That is returned
    as a
    """
    result = {"matches": find_possible_matches(pat)}
    return find_possible_matches(pat)
