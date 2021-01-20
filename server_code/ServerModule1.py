import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.server
from anvil.google.drive import app_files

file = app_fil

@anvil.server.callable
def determine_cheats():
    session["previous"] = pattern = request.form["pattern"]
    session["count"] = 0
    matches = xword.find_possible_matches(pattern)
    return render_template(
        "results.html", the_title="Here are your results", data=sorted(matches)
    )
  
def find_possible_matches(pattern):
    """Given any pattern of the type "__a___b__c", this function
       looks up and returns all the potential matches for the
       pattern in the Linux dictionary of words."""

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