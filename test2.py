import customtkinter as ck
import math
import sympy as sp


# Constants for the GUI size
WIDTH = 400
HEIGHT = 600
MAX_LENGTH = 16
BUTTONWIDTH = 80
BUTTONHEIGHT = 50
DROPDOWNWIDTH = 50
DROPDOWNHEIGHT = 30


class Calculator(ck.CTk):
    def __init__(self):
        super().__init__()

        # GUI setup
        self.function_buttons = []
        self.title("Calculator")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.minsize(WIDTH, HEIGHT)

        # Initialize states
        self.second_state = False
        self.trig_second_state = False
        self.deg_states = ['DEG', 'RAD']
        self.deg_index = 0

        self.trig_menu_open = False
        self.var_menu_open = False
        self.trig_frame = None
        self.var_frame = None

        # Configure rows and columns for grid
        for i in range(5):
            self.grid_columnconfigure(i, weight=1)
        for i in range(10):
            self.grid_rowconfigure(i, weight=1)

        # Display outputs
        self.top_display_output = ck.CTkLabel(self, text="", font=("Arial", 15), text_color="grey", anchor="e")
        self.top_display_output.grid(row=1, column=0, columnspan=7, sticky="nsew")

        self.bot_display_output = ck.CTkLabel(self, text="", font=("Arial", 35), anchor="e")
        self.bot_display_output.grid(row=2, column=0, columnspan=7, sticky="nsew")

        # Initialize the calculator state
        self.top_output = " "
        self.bot_output = ""
        self.evaluated_output = ""
        self.last_str = " "
        self.state_calc = ""
        self.finish_input = False
        self.eval_expression = None
        self.dot_placed = False

        # Define buttons according to the provided layout
        self.define_buttons()

        # Place the buttons on the grid
        self.place_buttons()

    def define_buttons(self):
        # Define the button properties

        self.button_trig = self.create_button("Trig")
        self.button_var = self.create_button("Var")

        self.button_2nd = self.create_button("2nd")
        self.button_pi = self.create_button("π")
        self.button_e = self.create_button("e")
        self.button_C = self.create_button("C")
        self.button_bkspc = self.create_button("←")

        self.button_x2 = self.create_button("x²")
        self.button_1_x = self.create_button("1/x")
        self.button_pctg = self.create_button("%")
        self.button_deg = self.create_button(self.deg_states[self.deg_index])
        self.button_mod = self.create_button("mod")

        self.button_sqrt = self.create_button("√x")
        self.button_lparen = self.create_button("(")
        self.button_rparen = self.create_button(")")
        self.button_fact = self.create_button("n!")
        self.button_div = self.create_button("/")

        self.button_pc = self.create_button("nPr")
        self.button_7 = self.create_button("7")
        self.button_8 = self.create_button("8")
        self.button_9 = self.create_button("9")
        self.button_mul = self.create_button("*")

        self.button_exp = self.create_button("exp")
        self.button_4 = self.create_button("4")
        self.button_5 = self.create_button("5")
        self.button_6 = self.create_button("6")
        self.button_sub = self.create_button("-")

        self.button_log = self.create_button("log")
        self.button_1 = self.create_button("1")
        self.button_2 = self.create_button("2")
        self.button_3 = self.create_button("3")
        self.button_add = self.create_button("+")

        self.button_ln = self.create_button("ln")
        self.button_pm = self.create_button("+/-")
        self.button_0 = self.create_button("0")
        self.button_dot = self.create_button(".")
        self.button_equal = self.create_button("=")

        # Bind the Key event
        self.bind('<Key>', self.keyboard_input)

    def create_button(self, text):
        # Helper function to create a button
        return ck.CTkButton(self, text=text, width=BUTTONWIDTH, height=BUTTONHEIGHT,
                            command=lambda: self.ButtonPressed(text))

    def place_buttons(self):
        # Place the buttons on the grid
        self.button_trig.grid(row=3, column=0, sticky="nsew", padx=1, pady=1)
        self.button_var.grid(row=3, column=1, sticky="nsew", padx=1, pady=1)

        self.button_2nd.grid(row=4, column=0, sticky="nsew", padx=1, pady=1)
        self.button_pi.grid(row=4, column=1, sticky="nsew", padx=1, pady=1)
        self.button_e.grid(row=4, column=2, sticky="nsew", padx=1, pady=1)
        self.button_C.grid(row=4, column=3, sticky="nsew", padx=1, pady=1)
        self.button_bkspc.grid(row=4, column=4, sticky="nsew", padx=1, pady=1)

        self.button_x2.grid(row=5, column=0, sticky="nsew", padx=1, pady=1)
        self.button_1_x.grid(row=5, column=1, sticky="nsew", padx=1, pady=1)
        self.button_pctg.grid(row=5, column=2, sticky="nsew", padx=1, pady=1)
        self.button_deg.grid(row=5, column=3, sticky="nsew", padx=1, pady=1)
        self.button_mod.grid(row=5, column=4, sticky="nsew", padx=1, pady=1)

        self.button_sqrt.grid(row=6, column=0, sticky="nsew", padx=1, pady=1)
        self.button_lparen.grid(row=6, column=1, sticky="nsew", padx=1, pady=1)
        self.button_rparen.grid(row=6, column=2, sticky="nsew", padx=1, pady=1)
        self.button_fact.grid(row=6, column=3, sticky="nsew", padx=1, pady=1)
        self.button_div.grid(row=6, column=4, sticky="nsew", padx=1, pady=1)

        self.button_pc.grid(row=7, column=0, sticky="nsew", padx=1, pady=1)
        self.button_7.grid(row=7, column=1, sticky="nsew", padx=1, pady=1)
        self.button_8.grid(row=7, column=2, sticky="nsew", padx=1, pady=1)
        self.button_9.grid(row=7, column=3, sticky="nsew", padx=1, pady=1)
        self.button_mul.grid(row=7, column=4, sticky="nsew", padx=1, pady=1)

        self.button_exp.grid(row=8, column=0, sticky="nsew", padx=1, pady=1)
        self.button_4.grid(row=8, column=1, sticky="nsew", padx=1, pady=1)
        self.button_5.grid(row=8, column=2, sticky="nsew", padx=1, pady=1)
        self.button_6.grid(row=8, column=3, sticky="nsew", padx=1, pady=1)
        self.button_sub.grid(row=8, column=4, sticky="nsew", padx=1, pady=1)

        self.button_log.grid(row=9, column=0, sticky="nsew", padx=1, pady=1)
        self.button_1.grid(row=9, column=1, sticky="nsew", padx=1, pady=1)
        self.button_2.grid(row=9, column=2, sticky="nsew", padx=1, pady=1)
        self.button_3.grid(row=9, column=3, sticky="nsew", padx=1, pady=1)
        self.button_add.grid(row=9, column=4, sticky="nsew", padx=1, pady=1)

        self.button_ln.grid(row=10, column=0, sticky="nsew", padx=1, pady=1)
        self.button_pm.grid(row=10, column=1, sticky="nsew", padx=1, pady=1)
        self.button_0.grid(row=10, column=2, sticky="nsew", padx=1, pady=1)
        self.button_dot.grid(row=10, column=3, sticky="nsew", padx=1, pady=1)
        self.button_equal.grid(row=10, column=4, sticky="nsew", padx=1, pady=1)

    # Fix issue with very large numbers eg(50000000000000000000000000000000)
    # Fix issue with errors, 1/0, overflow errors etc
    # Fix issue with 0.05 ^ 2 floating error
    # Fix issue with doing 5 E 10 + 5 E 10 < issue occurs with all self.calc_state math functions ლ(╹◡╹ლ)
    # Threading (✿◡‿◡)
    def ButtonPressed(self, value):
        # if user inputs a digit
        if value in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'π', 'e']:

            if len(self.bot_output) < 16:
                if value == "π":
                    self.bot_output = str(math.pi)
                elif value == "e":
                    self.bot_output = str(math.e)
                else:
                    self.bot_output = self.bot_output + value

            self.DisplayBottomText()
            self.evaluated_output = self.bot_output

        elif self.CheckSign(value) and self.evaluated_output != " ":
            self.dot_placed = False
            last_value = self.top_output[-1]
            if last_value == "+" or last_value == "-" or last_value == "*" or last_value == "/":

                self.top_output = self.top_output.replace(last_value, value)

            else:
                self.top_output = self.evaluated_output + " " + value

            self.bot_output = ""
            self.DisplayBottomText()
            self.DisplayUpperText()
        elif value == "2nd":
            # Toggle the '2nd' state
            self.second_state = not self.second_state
            # Update the functionalities of the affected buttons
            self.update_second_state()
        elif value == "C":
            self.evaluated_output = " "
            self.bot_output = ""
            self.top_output = " "
            self.state_calc = ""
            self.dot_placed = False
            self.finish_input = False
            self.DisplayUpperText()
            self.DisplayBottomText()
        # elif value == "CE":
        #     self.bot_output = ""
        #     self.DisplayBottomText()
        elif value == "←" and self.evaluated_output != "":
            if self.evaluated_output[-1] == ".":
                self.dot_placed = False

            self.evaluated_output = self.evaluated_output[0: len(self.evaluated_output) - 1]
            self.bot_output = self.evaluated_output
            self.DisplayBottomText()
        elif value == "." and self.dot_placed is False:
            self.dot_placed = True
            self.evaluated_output = self.evaluated_output + "."
            self.bot_output = self.evaluated_output
            self.DisplayBottomText()
        elif value == "+/-" and len(self.bot_output) > 0 and self.bot_output[0] == "-":
            self.evaluated_output = self.evaluated_output[1:]
            self.bot_output = self.evaluated_output
            self.DisplayBottomText()
        elif value == "+/-":
            self.evaluated_output = "-" + self.evaluated_output
            self.bot_output = self.evaluated_output
            self.DisplayBottomText()
        elif value == "=" and self.bot_output != " " and self.top_output != " ":
            if self.state_calc == "":
                self.CalculateUpBot()
            else:
                self.finish_input = True
        elif len(self.evaluated_output) > 0:
            if value == "1/x":
                eq = f"1/float(self.evaluated_output)"
                self.TransformNumber(eq, "1/")
            elif value == "x²":
                eq = f"math.pow(float(self.evaluated_output),2)"
                self.TransformNumber(eq, "^ 2")
            elif value == "√x":
                eq = f"math.sqrt(float(self.evaluated_output))"
                self.TransformNumber(eq, "sqrt(")
            elif value == "log":
                eq = f"math.log10(float(self.evaluated_output))"
                self.TransformNumber(eq, "log")
            elif value == "ln":
                eq = f"math.log(float(self.evaluated_output))"
                self.TransformNumber(eq, "ln")
            elif value == "%":
                eq = f"float(self.evaluated_output)/ 100"
                self.TransformNumber(eq, "%")
            elif value == "n!":
                if '.' not in self.evaluated_output:
                    eq = f"math.factorial(int(self.evaluated_output))"
                    self.TransformNumber(eq, "!")
            elif value == "exp":
                self.top_output = self.evaluated_output + " E"
                self.DisplayUpperText()
                self.top_output = self.evaluated_output
                self.evaluated_output = ""
                self.bot_output = ""
                self.state_calc = "exp"

            elif value == "mod":
                self.top_output = self.evaluated_output + " mod "
                self.DisplayUpperText()
                self.top_output = self.evaluated_output
                self.evaluated_output = ""
                self.bot_output = ""
                self.state_calc = "mod"

            elif value == "nPr":
                self.top_output = self.evaluated_output + "P"
                self.DisplayUpperText()
                self.top_output = self.evaluated_output
                self.evaluated_output = ""
                self.bot_output = ""
                self.state_calc = "nPr"

        if self.evaluated_output != "" and self.finish_input:
            if self.state_calc == "mod":
                eq = f"float(self.top_output) % float(self.evaluated_output)"
                self.TransformNumber(eq, "mod")
                self.top_output = " "
            elif self.state_calc == "exp":
                if "." not in self.evaluated_output:
                    eq = f"float(self.top_output) * math.pow(10, int(self.evaluated_output))"
                    self.TransformNumber(eq, "E")
                    self.top_output = " "
                else:
                    self.finish_input = False
            elif self.state_calc == "nPr":
                if "." not in self.evaluated_output and "." not in self.top_output:
                    eq = f"math.perm(int(self.top_output), int(self.evaluated_output))"
                    self.TransformNumber(eq, "P")
                    self.top_output = " "
                else:
                    self.finish_input = False

    def TransformNumber(self, eq, value):
        self.state_calc = ""
        self.finish_input = False
        self.dot_placed = False
        if self.NumBefore(value):
            top_value = self.evaluated_output + " " + value
        elif self.NumBefAft(value):
            top_value = self.top_output + " " + value + " " + self.evaluated_output
        else:
            top_value = value + " " + self.evaluated_output

        if value[-1] == "(":
            top_value = top_value + " )"

        evaluated_value = str(eval(eq))

        if self.CheckSign(self.top_output[-1]):
            final_eq = self.top_output + " " + evaluated_value
            self.top_output = self.top_output + " " + top_value
            self.evaluated_output = str(eval(final_eq))
        else:
            self.top_output = top_value
            self.evaluated_output = evaluated_value

        string = self.evaluated_output
        without_trailing_zeros = string.rstrip(
            '0').rstrip('.') if '.' in string else string

        self.bot_output = without_trailing_zeros

        self.DisplayUpperText()
        self.DisplayBottomText()
        self.bot_output = ""

    def NumBefAft(self, value):
        if value in ["mod", "E", "P"]:
            return True
        return False

    def NumBefore(self, value):
        if value in ["^ 2", "%", "!"]:
            return True
        return False

    def CalculateUpBot(self):
        expression = self.top_output + " " + self.bot_output
        eval_expression = sp.sympify(self.top_output + self.bot_output)
        self.top_output = expression + " ="
        string = str(eval_expression)
        without_trailing_zeros = string.rstrip(
            '0').rstrip('.') if '.' in string else string
        self.evaluated_output = without_trailing_zeros
        self.bot_output = self.evaluated_output

        self.bot_output = without_trailing_zeros
        self.DisplayBottomText()
        self.DisplayUpperText()

        self.top_output = " "
        self.bot_output = ""

    def PrintAll(self):
        print(self.bot_output)
        print(self.top_output)
        print(self.evaluated_output)

    def CheckSign(self, value):
        if value == "+" or value == "*" or value == "-" or value == "/":
            return True
        return False

    def CheckEquation(self):
        if self.CheckSign(self.top_output[-1]):
            return True
        return False

    def DisplayBottomText(self):
        self.bot_display_output.configure(text=self.bot_output)

    def DisplayUpperText(self):
        self.top_display_output.configure(text=self.top_output)

    def test(self):
        pass

    def keyboard_input(self, event):

        if event.char in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "+", "*", "-", "/", ".", "\\r", "\\x08"]:
            self.ButtonPressed(event.char)

        # if event.char == "1" or event.char == "2" or event.char == "3" or event.char == "4" or event.char == "5" \
        #         or event.char == "6" or event.char == "7" or event.char == "8" or event.char == "9" or event.char == "0":
        #     self.ButtonPressed(event.char)

        elif event.char == "+" or event.char == "*" or event.char == "-" or event.char == "/":
            self.ButtonPressed(event.char)
        elif event.char == ".":
            self.ButtonPressed(event.char)
        elif event.char == "\r":
            self.ButtonPressed("=")
        elif event.char == "\x08":
            self.ButtonPressed("←")

    def toggle_second(self):
        # Toggle the '2nd' state
        self.second_state = not self.second_state

        # Update the functionalities of the affected buttons
        self.update_second_state()

    def update_second_state(self):
        # Update the functionalities of the affected buttons based on the '2nd' state
        if self.second_state:
            # Change the button texts to their '2nd' mode functions
            self.button_x2.configure(text='x^y')
            self.button_sqrt.configure(text='y√x')
            self.button_pc.configure(text='nCr')
            self.button_exp.configure(text='2^x')
            self.button_log.configure(text='log_y')
            self.button_ln.configure(text='e^x')

        else:
            # Change the button texts back to their normal mode functions
            self.button_x2.configure(text='x²')
            self.button_sqrt.configure(text='√x')
            self.button_pc.configure(text='nPr')
            self.button_exp.configure(text='exp')
            self.button_log.configure(text='log')
            self.button_ln.configure(text='ln')


# Create an instance of the Calculator class and start the GUI
def main():
    new_app = Calculator()
    new_app.mainloop()


main()
