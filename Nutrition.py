import re
from SpellChecker import check_key_spelling


def get_dictionary(text_file):
    print(text_file)
    file = open(text_file, 'r')
    lines = file.readlines()
    info = file.read()
    print(info)
    nutritional_content = {

    }

    # Regex for name, grammy business, and percentage
    for line in lines:
        z = re.search('O[c-m]+g|o[c-m]+g', line)
        if z:
            ln = line
            words = z.string.split()
            for word in words:
                if re.search('O[c-m]+g|o[c-m]+g', word):
                    characters = '0' + word[1:]
                    print("Old Line: " + ln)
                    ln.replace(word, characters)
                    ln.replace('Omcg', '0mcg')
                    print("New Line: " + ln)

    for line in lines:
        # x = re.search('[0-9]+[c-m]+', line)
        x = False
        y = re.search('[0-9]+[c-m]+.*?[0-9]+[c-m]+', line)
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
            x = re.search('[0-9]+[c-m]+', line)
        if x:
            print(x.string)
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
                elif re.search('[0-9]+[c-m]+', word):
                    amount = word
            name = name.strip()

            # print('Name: ' + name[1:])
            # print('Amount: ' + amount)
            # print('Percentage: ' + percentage + '\n\n')

            nutritional_content.update({name: (amount, percentage)})

    nut = nutritional_content.copy()
    for key, value in nutritional_content.items():
        words = key.split()
        for word in words:
            if word == "Serving" or word == 'size' or word == 'cup':
                nut.pop(key)
                break

    nutritional_content = nut
    for key, value in nutritional_content.items():
        print(key, ":", value)

    # check_key_spelling(nutritional_content)
    return nutritional_content


# nutrition = get_dictionary(r"C:\Users\Mike\Desktop\Computer Science Files\Independent "
#                            r"Study\Python\Output Files\Recognized Words.txt")

