from spellchecker import SpellChecker
# import jamspell


def check_key_spelling(dictionary):
    spell = SpellChecker()
    for key, value in dictionary.items():
        words = key.split()
        misspelled = spell.unknown(words)
        for word in misspelled:
            print("Old Word: " + word)
            # correct = spell.correction(word)
            try:
                print("New Word: " + spell.correction(word))
            except TypeError:
                print("Word is correct")

    # corrector = jamspell.TSpellCorrector()
