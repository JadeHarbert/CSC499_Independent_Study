import tkinter as tk
from tkinter.filedialog import askopenfilename

from TextDetection2 import detect_text

window = tk.Tk()
window.geometry('700x400')
window.title("Nutrition Label Scanner")
window.resizable(width=False, height=False)
label = tk.Label(text='Welcome')
label.pack()

file_path = None


def input_file():
    global file_path
    f_types = [('JPG Files', "*.jpg"), ("PNG Files", "*.png")]
    file_path = askopenfilename(
        filetypes=f_types
    )
    if not file_path:
        return
    else:
        nutrition = detect_text(file_path)

        # Get number of servings from user
        while True:
            num_servings = input("How many servings?\n")
            try:
                num_servings = int(num_servings)
                break
            except ValueError:
                print("Please enter an integer\n")

        nutritional_content = {}

        # Calculate new amounts for each nutrition item
        for key, value in nutrition.items():
            k = key
            val = value
            amount = val[0]
            chars = amount[0:]
            weight = ''
            unit = ''
            isfloat = False
            for char in chars:
                if char.isdigit():
                    weight = weight + char
                elif char == '.':
                    weight = weight + char
                    isfloat = True
                else:
                    unit = unit + char

            if isfloat:
                weight = float(weight)
            else:
                weight = int(weight)

            new_weight = num_servings * weight
            if unit[0] == "<" or unit[0] == ">":
                new_weight = unit[0] + str(new_weight) + unit[1:]
            else:
                new_weight = str(new_weight) + unit
            # print("Old Weight: " + str(weight) + "\nNew Weight: " + str(new_weight))

            # Calculate new percentage
            try:
                percentage = val[1]
                num = ''
                chars = percentage[0:]
                for char in chars:
                    if char.isdigit():
                        num = num + char
                num = int(num)

                new_percentage = num_servings * num
                new_percentage = str(new_percentage) + '%'
                nutritional_content.update({key: (new_weight, new_percentage)})
            except ValueError:
                nutritional_content.update({key: (new_weight, val[1])})

        # Print new nutritional values
        for key, value in nutritional_content.items():
            print(key, ":", value)

    global window
    window.destroy()


button = tk.Button(text='Upload File',
                   width=10,
                   height=2,
                   bg='grey',
                   command=input_file)

button.pack()
window.mainloop()
