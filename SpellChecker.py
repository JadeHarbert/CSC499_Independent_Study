"""
Corrects spelling of keys of a dictionary off a dictionary text file at specified path
Author: Jade Harbert
"""
import enchant


def check_key_spelling(dictionary, key_dictionary_path):
    """
        Uses enchant to create a dictionary based off of the text file at key_dictionary_path and spellchecks the keys.
        Also removes checks to see if there are additional errors with amount
    :param dictionary: dict
        Represents the nutrition items that we want to spellcheck
    :param key_dictionary_path: pathlib.WindowsPath
        Path to the input file
    :return: dict
        Represents the properly spelled nutrition items
    """
    # Creates a dictionary to check the keys against
    nutrient_dict = enchant.PyPWL(key_dictionary_path)
    d = dictionary.copy()

    # Loops through all the keys in the dictionary
    for key, value in dictionary.items():
        words = key.split()
        k = ''
        # Spell checks all the words to see if they are spelled correctly
        for word in words:
            if not nutrient_dict.check(word):
                suggestions = nutrient_dict.suggest(word)
                correction = suggestions[0]
                k = k + " " + correction
            else:
                k = k + " " + word
        k = k.strip()
        # Replaces the key with potentially incorrectly spelled words to a correctly spelled key
        d[k] = d.pop(key)

        # Checks to see if amount has a trailing character that isn't g and removes it
        val = value[0]
        if val[-1] != 'g':
            new_val = val[:-1]
            d[k] = (new_val, value[1])
    return d
