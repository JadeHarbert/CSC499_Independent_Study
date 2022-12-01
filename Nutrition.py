import re
from SpellChecker import check_key_spelling


def get_dictionary(text_file):
    amount_regex = '[0-9]+[c-m]+'
    double_amount_regex = '[0-9]+[c-m]+.*?[0-9]+[c-m]+'
    o_to_0_regex = 'O[c-m]*g|o[c-m]*g'
    correct_9_to_g_regex = '[0-9]+9'
    i_to_1_regex = 'i[c-m]*g'

    file = open(text_file, 'r')
    lines = file.readlines()
    nutritional_content = {

    }
    corrected_lines = []

    for line in lines:
        newline = False
        # Searches for O's that should be zeros and corrects them
        z = re.search(o_to_0_regex, line)
        x = re.search(correct_9_to_g_regex, line)
        y = re.search(i_to_1_regex, line)
        if z:
            words = z.string.split()
            for word in words:
                if re.search(o_to_0_regex, word):
                    characters = '0' + word[1:]
                    ln = line.replace(word, characters)
                    corrected_lines.append(ln)
                    newline = True

        if x:
            words = x.string.split()
            for word in words:
                if re.search(correct_9_to_g_regex, word):
                    characters = word[:-1] + 'g'
                    ln = line.replace(word, characters)
                    corrected_lines.append(ln)
                    newline = True
        if y:
            words = y.string.split()
            for word in words:
                if re.search(i_to_1_regex, word):
                    characters = '1' + word[1:]
                    ln = line.replace(word, characters)
                    corrected_lines.append(ln)
                    newline = True

        if not newline:
            corrected_lines.append(line)

    for line in corrected_lines:
        # x = re.search('[0-9]+[c-m]+', line)
        x = False
        y = re.search(double_amount_regex, line)
        if y:
            words = y.string.split()
            # print('Printing: ' + line)
            name = ''
            amount = ''
            percentage = ''
            words2 = words.copy()
            for word in words:
                word = word.strip()
                if word.isalpha():
                    name = name + " " + word
                    words2.remove(word)
                elif word.endswith("%"):
                    percentage = word
                    words2.remove(word)
                    break
                else:
                    amount = word
                    words2.remove(word)

            name = name.strip()
            nutritional_content.update({name: (amount, percentage)})
            name = ''
            amount = ''
            percentage = ''
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
            words = x.string.split()
            name = ''
            amount = ''
            percentage = ''
            for word in words:
                word = word.strip()
                if word[0] == '(':
                    word = word[1:]
                if word[-1] == ')':
                    word = word[:-1]

                if word.isalpha():
                    name = name + " " + word
                elif word.endswith("%"):
                    percentage = word
                elif re.search(amount_regex, word):
                    amount = word
            name = name.strip()

            nutritional_content.update({name: (amount, percentage)})

    nut = nutritional_content.copy()
    for key, value in nutritional_content.items():
        words = key.split()
        new_key = ''
        for word in words:
            if word == "Serving" or word == 'size' or word == 'cup':
                nut.pop(key)
                break

    nutritional_content = nut
    for key, value in nutritional_content.items():
        print(key, ":", value)

    check_key_spelling(nutritional_content)
    return nutritional_content


# nutrition = get_dictionary(r"C:\Users\Mike\Desktop\Computer Science Files\Independent "
#                            r"Study\Python\Output Files\Recognized Words.txt")

