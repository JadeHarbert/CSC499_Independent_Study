import enchant


def check_key_spelling(dictionary):
    nutrient_dict = enchant.PyPWL(r'C:\Users\Mike\Desktop\Computer Science Files\Independent Study\Python\Input '
                                  r'Files\nutrients_dict.txt')
    dict = dictionary.copy()
    for key, value in dictionary.items():
        words = key.split()
        k = ''
        for word in words:

            if not nutrient_dict.check(word):
                suggestions = nutrient_dict.suggest(word)
                correction = suggestions[0]
                k = k + " " + correction
        k = k.strip()
        dict[k] = dict.pop(key)

    for key, value in dict.items():
        print(key, ":", value)