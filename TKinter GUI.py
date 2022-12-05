"""
Main application for a nutrition calculator. Prompts the user to select an image that is of a nutrition table. OpenCV
is used to detect text. OCR is used to convert image to string. Regex and spellchecking is then used to correct names

Jade Harbert
"""
import _tkinter
import tkinter as tk
from tkinter.filedialog import askopenfilename

from TextDetection import detect_text

total_nutrition = {}


def calculate_new_servings(nutrition, num_servings):
    """
    Calculates the new amounts and percentages by multiplying all the values by num_servings
    :param nutrition: dict
        Represents the nutrition items with the format being {name : (amount, percentage)}
    :param num_servings: int
        Number to multiple all the servings by
    :return: dict
        Nutritional items with their new percentage and amount
    """

    nutritional_content = {}

    # Calculate new amounts for each nutrition item
    for key, value in nutrition.items():
        val = value
        amount = val[0]
        chars = amount[0:]
        weight = ''
        unit = ''
        isfloat = False
        # Loop through the characters in amount
        for char in chars:
            # If the character is a digit, append it to weight
            if char.isdigit():
                weight = weight + char
            # If the character is a . then append it to weight and set isFloat to true so we can do float arithmetic
            elif char == '.':
                weight = weight + char
                isfloat = True
            # The leftover characters are the unit
            else:
                unit = unit + char

        # Convert the weight to float or int
        if isfloat:
            weight = float(weight)
        else:
            weight = int(weight)

        # Round the number to 2 decimal places for floating point arithmetic
        new_weight = round(num_servings * weight, 2)
        # Keep the equality signs
        if unit[0] == "<" or unit[0] == ">":
            new_weight = unit[0] + str(new_weight) + unit[1:]
        else:
            new_weight = str(new_weight) + unit

        # Calculate new percentage
        try:
            percentage = val[1]
            num = ''
            chars = percentage[0:]
            # Get the numbers in percentage
            for char in chars:
                if char.isdigit():
                    num = num + char
            num = int(num)

            new_percentage = round(num_servings * num, 2)
            new_percentage = str(new_percentage) + '%'
            # Update the dictionary item to represent new weight and percentage
            nutritional_content.update({key: (new_weight, new_percentage)})
        # Throws a ValueError when percentage is empty
        except ValueError:
            nutritional_content.update({key: (new_weight, val[1])})
    return nutritional_content


def generate_nutrition_dictionary(path):
    """
    Generates a dictionary representing nutrition at the specified path
    :param path: pathlib.WindowsPath
        Path to file
    :return: dict
        Dictionary that holds the values of the new servings
    """
    # OCR is done using two different methods because they can produce different results
    nutrition1 = detect_text(path, method=1)
    nutrition2 = detect_text(path, method=2)
    nutrition = None

    # We get the result that has more keys because it is more accurate
    if len(nutrition1) >= len(nutrition2):
        nutrition = nutrition1
    elif len(nutrition1) < len(nutrition2):
        nutrition = nutrition2

    for key, value in nutrition.items():
        print(key, ":", value)
    print("Number of items:", len(nutrition))

    # Get number of servings from user
    while True:
        num_servings = input("How many servings?\n")
        try:
            num_servings = int(num_servings)
            break
        except ValueError:
            print("Please enter an integer\n")

    # Calculate the new nutrition amounts based on the num_servings
    return calculate_new_servings(nutrition, num_servings)


def input_file():
    """
    Prompts the user to select a file from the directory.
    :return: null
    """
    global file_path
    f_types = [('JPG Files', "*.jpg"), ("PNG Files", "*.png")]
    file_path = askopenfilename(
        filetypes=f_types
    )
    if not file_path:
        return
    # Detect the text on the image at the specific path and return a dictionary representing the nutrition items
    else:
        global window
        try:
            window.destroy()
        except _tkinter.TclError:
            pass
        end_program = False

        new_nutrition = generate_nutrition_dictionary(file_path)
        # Print new nutritional values
        print("Current Nutrition:\n")
        for key, value in new_nutrition.items():
            print(key, ":", value)

        # Base case for recursion
        global total_nutrition
        if len(total_nutrition) == 0:
            total_nutrition = new_nutrition

        # Update total_nutrition to reflect adding new nutrition
        else:
            tot = total_nutrition.copy()
            for key, value in new_nutrition.items():

                try:
                    val = total_nutrition.get(key)
                    amount1 = value[0]
                    percent1 = value[1]
                    amount2 = val[0]
                    percent2 = val[1]

                    weight1 = ''
                    weight2 = ''
                    unit = ''
                    chars1 = amount1[0:]
                    chars2 = amount2[0:]
                    isFloat = False
                    for char in chars1:
                        # If the character is a digit, append it to weight
                        if char.isdigit():
                            weight1 = weight1 + char
                        # If the character is a . then append it to weight and set isFloat to true, so we can do float
                        # arithmetic
                        elif char == '.':
                            weight1 = weight1 + char
                            isFloat = True
                        # The leftover characters are the unit
                        else:
                            unit = unit + char

                    for char in chars2:
                        # If the character is a digit, append it to weight
                        if char.isdigit():
                            weight2 = weight2 + char
                        # If the character is a . then append it to weight and set isFloat to true, so we can do float
                        # arithmetic
                        elif char == '.':
                            weight2 = weight2 + char
                            isFloat = True
                    if isFloat:
                        weight1 = float(weight1)
                        weight2 = float(weight2)
                    else:
                        weight1 = int(weight1)
                        weight2 = int(weight2)
                    total_weight = weight1 + weight2
                    total_weight = str(total_weight) + unit

                    try:
                        num1 = ''
                        chars = percent1[0:]
                        # Get the numbers in percentage
                        for char in chars:
                            if char.isdigit():
                                num1 = num1 + char
                        num1 = int(num1)

                        num2 = ''
                        chars = percent2[0:]
                        # Get the numbers in percentage
                        for char in chars:
                            if char.isdigit():
                                num2 = num2 + char
                        num2 = int(num2)
                        # Add the two percentages
                        total_percent = num1 + num2
                        total_percent = str(total_percent) + "%"

                        tot[key] = (total_weight, total_percent)
                    except ValueError:
                        tot[key] = (total_weight, value)
                except KeyError:
                    tot.update({key: value})
                except TypeError:
                    tot.update({key: value})
            total_nutrition = tot

        print("Total Nutrition:\n\n")
        for key, value in total_nutrition.items():
            print(key, ":", value)

        while True:
            keep_going = input("Add new item? <yes> <no>\n")
            if keep_going == "yes":
                # Restart function to take input again
                input_file()
                break
            elif keep_going == "no":
                break
            else:
                print("Please enter yes or no\n")


# Tkinter setup
window = tk.Tk()
window.geometry('700x400')
window.title("Nutrition Label Scanner")
window.resizable(width=False, height=False)
label = tk.Label(text='Welcome')
label.pack()

file_path = None

button = tk.Button(text='Upload File',
                   width=10,
                   height=2,
                   bg='grey',
                   command=input_file)

button.pack()
window.mainloop()
