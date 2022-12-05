"""
Uses regex to generate a dictionary representing the nutrition items and corrects improperly identified characters
Author: Jade Harbert
"""
import re
from pathlib import Path

from SpellChecker import check_key_spelling


def get_dictionary(text_file_path):
    """
    Uses regex to correct improperly identified character with OCR and then uses regex to pick out the items. Creates
    dictionaries based on those items with the format of {name : (amount, percentage)}
    :param text_file_path: pathlib.WindowsPath
        Path to the input file
    :return:
        dict Items along with their amounts and percentages
    """
    # Regex values that are going to be used later

    # Looks for any amount
    amount_regex = '[0-9]+[c-m]+'
    # Looks for two amounts on one line
    double_amount_regex = '[0-9]+[c-m]+.*?[0-9]+[c-m]+'
    # Looks for an o that should be a 0
    o_to_0_regex = 'O[c-m]*g|o[c-m]*g'
    # Looks for a 9 that should be a g
    correct_9_to_g_regex = '[0-9]+9'
    # Looks for an i that should be a 1
    i_to_1_regex = 'i[c-m]*g'
    # Looks for pipes
    pipe_regex = '\|'

    file = open(text_file_path, 'r')
    lines = file.readlines()
    nutritional_content = {

    }
    corrected_lines = []

    # Loops through all the lines
    for line in lines:
        newLine = False
        q = re.search(pipe_regex, line)
        # If a pipe exists, then we throw it and everything after it away
        if q:
            string = q.string
            index = string.index('|')
            correct = line[:index]
            ln = line.replace(line, correct)
            corrected_lines.append(ln)
            newLine = True

        if not newLine:
            corrected_lines.append(line)

    lines = corrected_lines
    corrected_lines = []

    # Reads all the lines in Recognized Words.txt
    for line in lines:
        newline = False
        z = re.search(o_to_0_regex, line)
        x = re.search(correct_9_to_g_regex, line)
        y = re.search(i_to_1_regex, line)

        # If the line contains a 9 that should be a g, then we correct it
        if x:
            words = x.string.split()
            for word in words:
                if re.search(correct_9_to_g_regex, word):
                    characters = word[:-1] + 'g'
                    ln = line.replace(word, characters)
                    corrected_lines.append(ln)
                    newline = True
        # If the line contains an i that should be a 1, then we correct it
        if y:
            words = y.string.split()
            for word in words:
                if re.search(i_to_1_regex, word):
                    characters = '1' + word[1:]
                    ln = line.replace(word, characters)
                    corrected_lines.append(ln)
                    newline = True
        # If the line contains an o that should be a 0, then we correct it
        if z:
            words = z.string.split()
            for word in words:
                if re.search(o_to_0_regex, word):
                    characters = '0' + word[1:]
                    ln = line.replace(word, characters)
                    corrected_lines.append(ln)
                    newline = True
        if not newline:
            corrected_lines.append(line)

    # Regex is used to search every line to see if it is a nutrient item
    for line in corrected_lines:
        x = False
        y = re.search(double_amount_regex, line)

        # We first look to see if two nutrient items are on a single line
        if y:
            # We split the line to have access to each individual piece
            words = y.string.split()
            name = ''
            amount = ''
            percentage = ''

            # We duplicate words, so we can remove the first item from the list
            words2 = words.copy()

            for word in words:
                word = word.strip()
                # If the word only contains alphabetic characters then add it to name
                if word.isalpha():
                    name = name + " " + word
                    words2.remove(word)
                # If the word ends with % then we add it to percentage
                elif word.endswith("%"):
                    percentage = word
                    words2.remove(word)
                    # We stop looking at other words because we know we're at the end of the first item
                    break
                # The leftover word is amount
                else:
                    amount = word
                    words2.remove(word)

            name = name.strip()

            # Add item to dictionary
            nutritional_content.update({name: (amount, percentage)})
            name = ''
            amount = ''
            percentage = ''
            # Rinse and repeat for the second item
            for word in words2:
                word = word.strip()
                if word.isalpha():
                    name = name + " " + word
                elif word.endswith("%"):
                    percentage = word
                    break
                else:
                    amount = word
            name = name.strip()
            nutritional_content.update({name: (amount, percentage)})
        else:
            x = re.search(amount_regex, line)
        if x:
            # First, we split the line into words
            words = x.string.split()
            name = ''
            amount = ''
            percentage = ''
            # Second, we go through each word to see what the word represents
            for word in words:
                word = word.strip()

                # We check to see if the word has parenthesis around it and remove them
                if word[0] == '(':
                    word = word[1:]
                if word[-1] == ')':
                    word = word[:-1]

                # If the word is an alphabetic string, then we add it to name
                if word.isalpha():
                    name = name + " " + word
                # If the word ends with %, then it's a percentage
                elif word.endswith("%"):
                    percentage = word
                # If the word fulfills the amount_regex, then it's an amount
                elif re.search(amount_regex, word):
                    amount = word
            name = name.strip()

            # Add the item to the dictionary
            nutritional_content.update({name: (amount, percentage)})

    nut = nutritional_content.copy()

    # Search through the keys to see if it contains "Serving", 'size', or 'cup' and remove it as it is unused
    for key, value in nutritional_content.items():
        words = key.split()
        for word in words:
            if word == "Serving" or word == 'size' or word == 'cup':
                nut.pop(key)
                break

        # Checks to see if there is an item that is empty and deletes it
        if value[0] == "" and value[1] == "":
            nut.pop(key)

    nutritional_content = nut

    key_dictionary_path = Path.cwd().joinpath("Input Files/nutrients_dict.txt")
    # Correct the spelling of the keys
    nutritional_content = check_key_spelling(nutritional_content, key_dictionary_path)

    return nutritional_content
