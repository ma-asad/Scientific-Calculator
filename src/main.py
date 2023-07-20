from frontend import *
from backend import *


def main():
    """
    Create instances of the CalculatorBackend, CalculatorFrontend, and Keyboard classes,
    bind the keyboard to the GUI, and start the calculator.
    """

    calc_back = CalculatorBackend()
    calc_front = CalculatorFrontend(calc_back)

    keyboard = Keyboard(calc_front)

    keyboard_thread = threading.Thread(target=calc_front.bind, args=("<Key>", keyboard.keyboard_input))
    keyboard_thread.daemon = True
    keyboard_thread.start()

    calc_front.initialise()


if __name__ == "__main__":
    try:
        # Your main program code here
        main()
    except KeyboardInterrupt:
        # Code to execute when the program is manually stopped
        print("Program was stopped manually")
