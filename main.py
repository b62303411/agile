# This is a sample Python script.
from flask import Flask

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

app = Flask(__name__)
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
