import customtkinter as ck
import math
import sympy as sp
import threading

# Constants for the GUI size
WIDTH = 350
HEIGHT = 500
MAX_LENGTH = 16
BUTTONWIDTH = 60
BUTTONHEIGHT = 10


class CalculatorBackend:
    """
    The CalculatorBackend class is responsible for all mathematical operations and
    maintaining the state of the calculator.
    """

    def __init__(self):
        self.second_state = False
        self.trig_second_state = False
        self.deg_states = ['DEG', 'RAD']
        self.deg_index = 0

        self.trig_menu_open = False
        self.trig_frame = None

        self.bool_top_display = False
        self.bool_bot_display = False

        # Initialize the calculator state
        self.additional_argument = ""
        self.top_output = " "
        self.bot_output = ""
        self.evaluated_output = ""
        self.last_str = " "
        self.state_calc = ""
        self.finish_input = False
        self.eval_expression = None
        self.dot_placed = False
        self.dual_inputs = False

    def add_digits_constants(self, value):
        """
        Handle digit or constant input by adding it to the current expression.

        :param value: The digit or constant to be added to the current expression.
        """

        if len(self.bot_output) < 16:
            if value == "π":
                self.bot_output = str(math.pi)
            elif value == "e":
                self.bot_output = str(math.e)
            else:
                self.bot_output = self.bot_output + value

        self.bool_bot_display = True
        self.evaluated_output = self.bot_output

    def handle_backspace(self):
        if self.evaluated_output[-1] == ".":
            self.dot_placed = False

        self.evaluated_output = self.evaluated_output[0: len(self.evaluated_output) - 1]
        self.bot_output = self.evaluated_output
        self.bool_bot_display = True

    def handle_signs(self, value):
        """
        Handle mathematical operator input by adding it to the current expression.

        :param value: The mathematical operator to be added to the current expression.
        """

        self.dot_placed = False
        last_value = self.top_output[-1]

        if self.state_calc != "":
            self.finish_input = True
            self.handle_states()
        if last_value == "+" or last_value == "-" or last_value == "*" or last_value == "/":
            self.top_output = self.top_output.replace(last_value, value)
        else:
            self.top_output = self.evaluated_output + " " + value
        self.bot_output = ""
        self.bool_bot_display = True
        self.bool_top_display = True

    def handle_math_functions(self, value):
        """ Handle math function input by adding it to the current expression."""

        if self.check_sign(self.top_output[-1]):
            self.additional_argument = self.top_output

        if value == "1/x":
            eq = f"1/float(self.evaluated_output)"
            self.transform_number(eq, "1/")

        elif value == "x²":
            eq = f"math.pow(float(self.evaluated_output),2)"
            self.transform_number(eq, "^ 2")

        elif value == "√x":
            eq = f"math.sqrt(float(self.evaluated_output))"
            self.transform_number(eq, "sqrt(")

        elif value == "log":
            eq = f"math.log10(float(self.evaluated_output))"
            self.transform_number(eq, "log")

        elif value == "ln":
            eq = f"math.log(float(self.evaluated_output))"
            self.transform_number(eq, "ln")

        elif value == "%":
            eq = f"float(self.evaluated_output)/ 100"
            self.transform_number(eq, "%")
        elif value == "|x|":
            eq = f"abs(float(self.evaluated_output))"
            self.transform_number(eq, "abs(")
        elif value == "n!":
            if '.' not in self.evaluated_output:
                eq = f"math.factorial(int(self.evaluated_output))"
                self.transform_number(eq, "!")
        elif value == "2^x":
            eq = f"math.pow(2,float(self.evaluated_output))"
            self.transform_number(eq, "2 ^")
        elif value == "e^x":
            eq = f"math.pow(math.e,float(self.evaluated_output))"
            self.transform_number(eq, "e ^")
        elif value == "exp":
            self.top_output = self.evaluated_output + " E"
            self.display_multi_input_operator()
            self.state_calc = "exp"
        elif value == "log_y":
            self.top_output = self.evaluated_output + " log base"
            self.display_multi_input_operator()
            self.state_calc = "log_y"
        elif value == "mod":
            self.top_output = self.evaluated_output + " mod "
            self.display_multi_input_operator()
            self.state_calc = "mod"
        elif value == "nPr":
            self.top_output = self.evaluated_output + "P"
            self.display_multi_input_operator()
            self.state_calc = "nPr"
        elif value == "nCr":
            self.top_output = self.evaluated_output + "C"
            self.display_multi_input_operator()
            self.state_calc = "nCr"
        elif value == "x^y":
            self.top_output = self.evaluated_output + " ^ "
            self.display_multi_input_operator()
            self.state_calc = "x^y"
        elif value == "y√x":
            self.top_output = self.evaluated_output + " √ "
            self.display_multi_input_operator()
            self.state_calc = "y√x"

    def handle_trig_functions(self, value):
        """Handles trigonometric functions input by adding it to the current expression.
        :param value: The trigonometric function to be added to the current expression."""

        if value in ["sin", "cos", "tan"]:
            if self.deg_index == 0:
                # Degrees mode
                angle = math.radians(float(self.evaluated_output))
            else:
                # Radians mode
                angle = float(self.evaluated_output)
        else:
            angle = float(self.evaluated_output)

        if value == "sin":
            eq = f"round(math.sin({angle}),10)"
            self.transform_number(eq, "sin")
        elif value == "cos":
            eq = f"round(math.cos({angle}),10)"
            self.transform_number(eq, "cos")
        elif value == "tan":
            eq = f"round(math.tan({angle}),10)"
            self.transform_number(eq, "tan")
        elif value == "sin^-1":
            eq = f"round(math.asin({angle}),10)"
            self.transform_number(eq, "asin")
        elif value == "cos^-1":
            eq = f"round(math.acos({angle}),10)"
            self.transform_number(eq, "acos")
        elif value == "tan^-1":
            eq = f"round(math.atan({angle}),10)"
            self.transform_number(eq, "atan")

        if value in ["sin^-1", "cos^-1", "tan^-1"] and self.deg_index == 0:
            convert_to_degrees = float(self.evaluated_output)
            self.evaluated_output = str(round(math.degrees(convert_to_degrees), 2))
            self.bot_output = self.evaluated_output

    def handle_states(self):
        if self.state_calc == "mod":
            eq = f"float(self.top_output) % float(self.evaluated_output)"
            self.transform_number(eq, "mod")

        elif self.state_calc == "x^y":
            eq = f"math.pow(float(self.top_output), float(self.evaluated_output))"
            self.transform_number(eq, "^")

        elif self.state_calc == "y√x":
            eq = f"float(self.evaluated_output) ** (1 / float(self.top_output))"
            self.transform_number(eq, "√")

        elif self.state_calc == "log_y":
            eq = f"math.log(float(self.top_output),float(self.evaluated_output))"
            self.transform_number(eq, "log base")

        elif self.state_calc == "exp":
            if "." not in self.evaluated_output:
                eq = f"float(self.top_output) * math.pow(10, int(self.evaluated_output))"
                self.transform_number(eq, "E")
            else:
                self.finish_input = False
        elif self.state_calc == "nPr":
            if "." not in self.evaluated_output and "." not in self.top_output:
                eq = f"math.perm(int(self.top_output), int(self.evaluated_output))"
                self.transform_number(eq, "P")
            else:
                self.finish_input = False
        elif self.state_calc == "nCr":
            if "." not in self.evaluated_output and "." not in self.top_output:
                eq = f"math.comb(int(self.top_output), int(self.evaluated_output))"
                self.transform_number(eq, "C")
            else:
                self.finish_input = False

    def clear_all(self):
        """Clears all the variables and resets the calculator to its initial state."""

        self.evaluated_output = " "
        self.bot_output = ""
        self.top_output = " "
        self.state_calc = ""
        self.dot_placed = False
        self.finish_input = False
        self.dual_inputs = False
        self.bool_top_display = True
        self.bool_bot_display = True

    def display_multi_input_operator(self):
        """Displays the top output and the evaluated output in the bottom output."""
        self.dot_placed = False
        self.bool_top_display = True
        self.bot_output = ""

    def transform_number(self, eq, value):
        """Transforms the current expression to the new expression. Handles errors and exceptions.
        :param eq: The new expression to be evaluated.
        :param value: The new expression to be displayed in the top output."""

        self.state_calc = ""
        self.finish_input = False
        if self.num_before(value):
            top_value = self.additional_argument + " " + self.evaluated_output + " " + value
        elif self.num_bef_aft(value):
            top_value = self.additional_argument + " " + self.top_output + " " + value + " " + self.evaluated_output
        else:
            top_value = self.additional_argument + " " + value + " " + self.evaluated_output
        eq = self.additional_argument + eq
        self.additional_argument = ""
        if value[-1] == "(":
            top_value = top_value + " )"
        top_value = top_value + " ="

        try:
            evaluated_value = eval(eq)
            evaluated_value = str(sp.sympify(evaluated_value))
            if self.check_sign(self.top_output[-1]):
                final_eq = self.top_output + " " + evaluated_value
                self.top_output = self.top_output + " " + top_value
                self.evaluated_output = str(eval(final_eq))
            else:
                self.top_output = top_value
                self.evaluated_output = evaluated_value

            string = self.evaluated_output
            without_trailing_zeros = string.rstrip(
                '0').rstrip('.') if '.' in string else string

            self.evaluated_output = without_trailing_zeros
            self.bot_output = self.evaluated_output
            self.bool_top_display = True
            self.bool_bot_display = True
        except SyntaxError:
            pass
        # check down
        except (TypeError, ValueError, sp.SympifyError, OverflowError, ZeroDivisionError):
            # Handle specific exceptions that can occur during evaluation
            self.bot_output = "MATH ERROR"
            self.bool_top_display = True
            self.bool_bot_display = True

    def num_bef_aft(self, value):
        """Checks if the operator requires a number before and after it."""

        if value in ["mod", "E", "P", "C", "^", "√", "log base"]:
            return True
        return False

    def num_before(self, value):
        """Checks if the operator requires a number before it."""
        if value in ["^ 2", "%", "!"]:
            return True
        return False

    def calculate_up_bot(self):
        """Calculates the expression in the top output and displays the result in the bottom output.
        Handles errors and exceptions."""

        try:
            expression = self.top_output + " " + self.bot_output
            eval_expression = eval(self.top_output + self.bot_output)
            eval_expression = sp.sympify(eval_expression)
            self.top_output = expression + " ="
            string = str(eval_expression)

            without_trailing_zeros = string.rstrip(
                '0').rstrip('.') if '.' in string else string

            self.evaluated_output = without_trailing_zeros
            self.bot_output = self.evaluated_output

            self.bot_output = without_trailing_zeros
            self.bool_bot_display = True
            self.bool_top_display = True
        except SyntaxError:
            pass
        except (TypeError, ValueError, sp.SympifyError, OverflowError, ZeroDivisionError):
            # Handle specific exceptions that can occur during evaluation
            self.bot_output = "MATH ERROR"
            self.bool_top_display = True
            self.bool_bot_display = True

    def check_sign(self, value):
        if value == "+" or value == "*" or value == "-" or value == "/":
            return True
        return False

    def check_equation(self):
        if self.check_sign(self.top_output[-1]):
            return True
        return False


class CalculatorFrontend(ck.CTk):
    """
    The CalculatorFrontend class is responsible for managing the GUI of the calculator
    and for handling user interactions.
    """

    def __init__(self, backend):
        """
        Initialize CalculatorFrontend with a CalculatorBackend instance to handle calculations.

        :param backend: An instance of CalculatorBackend to handle calculations.
        """
        super().__init__()

        # GUI setup
        self.backend = backend

        self.title("Calculator")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.minsize(WIDTH, HEIGHT)

        # buttons
        self.output_frame = None
        self.top_display_output = None
        self.bot_display_output = None

        self.trig_optionmenu_trig = None
        self.trig_optionmenu = None

        self.button_2nd = None
        self.button_abs = None
        self.button_ce = None
        self.button_C = None
        self.button_bkspc = None

        self.button_x2 = None
        self.button_1_x = None
        self.button_pctg = None
        self.button_mod = None
        self.button_deg = None

        self.button_sqrt = None
        self.button_pi = None
        self.button_e = None
        self.button_fact = None
        self.button_div = None

        self.button_pc = None
        self.button_7 = None
        self.button_8 = None
        self.button_9 = None
        self.button_mul = None

        self.button_exp = None
        self.button_4 = None
        self.button_5 = None
        self.button_6 = None
        self.button_sub = None

        self.button_log = None
        self.button_1 = None
        self.button_2 = None
        self.button_3 = None
        self.button_add = None

        self.button_ln = None
        self.button_pm = None
        self.button_0 = None
        self.button_dot = None
        self.button_equal = None

        for i in range(5):
            self.grid_columnconfigure(i, weight=1)
        for i in range(11):
            self.grid_rowconfigure(i, weight=1)

    def initialise(self):
        # Define buttons
        self.define_buttons()

        # Place the buttons on the grid
        self.place_buttons()

        self.mainloop()

    def define_buttons(self):

        self.output_frame = ck.CTkFrame(self, fg_color='#292929')
        self.top_display_output = ck.CTkLabel(self.output_frame, text="", font=("Arial", 25), text_color="grey",
                                              anchor="e")
        self.bot_display_output = ck.CTkLabel(self.output_frame, text="", font=("Arial", 32), anchor="e")

        # Define the trig option menu
        trig_options = ["sin", "cos", "tan", "sin^-1", "cos^-1", "tan^-1"]
        self.trig_optionmenu_trig = ck.StringVar(value="Trig")
        self.trig_optionmenu = ck.CTkOptionMenu(self, values=trig_options, command=self.button_pressed,
                                                variable=self.trig_optionmenu_trig, fg_color='#21211f',
                                                button_color='#21211f', button_hover_color='#474747')

        # Define the button properties
        self.button_2nd = self.create_button("2nd")
        self.button_abs = self.create_button("|x|")
        self.button_ce = self.create_button("CE")
        self.button_C = self.create_button("C")
        self.button_bkspc = self.create_button("←")

        self.button_x2 = self.create_button("x²")
        self.button_1_x = self.create_button("1/x")
        self.button_pctg = self.create_button("%")
        self.button_mod = self.create_button("mod")
        self.button_deg = self.create_button(self.backend.deg_states[self.backend.deg_index])

        self.button_sqrt = self.create_button("√x")
        self.button_pi = self.create_button("π")
        self.button_e = self.create_button("e")
        self.button_fact = self.create_button("n!")
        self.button_div = self.create_button("/")

        self.button_pc = self.create_button("nPr")
        self.button_7 = self.create_num_button("7")
        self.button_8 = self.create_num_button("8")
        self.button_9 = self.create_num_button("9")
        self.button_mul = self.create_button("*")

        self.button_exp = self.create_button("exp")
        self.button_4 = self.create_num_button("4")
        self.button_5 = self.create_num_button("5")
        self.button_6 = self.create_num_button("6")
        self.button_sub = self.create_button("-")

        self.button_log = self.create_button("log")
        self.button_1 = self.create_num_button("1")
        self.button_2 = self.create_num_button("2")
        self.button_3 = self.create_num_button("3")
        self.button_add = self.create_button("+")

        self.button_ln = self.create_button("ln")
        self.button_pm = self.create_num_button("+/-")
        self.button_0 = self.create_num_button("0")
        self.button_dot = self.create_num_button(".")
        self.button_equal = ck.CTkButton(self, text="=", width=BUTTONWIDTH, height=BUTTONHEIGHT,
                                         command=lambda: self.button_pressed("="), fg_color='#16638a',
                                         hover_color='#0f4561')

    def create_button(self, text):
        # Helper function to create a button
        return ck.CTkButton(self, text=text, width=BUTTONWIDTH, height=BUTTONHEIGHT,
                            command=lambda: self.button_pressed(text), fg_color='#333332', hover_color='#474747')

    def create_num_button(self, text):
        # Helper function to create a button
        return ck.CTkButton(self, text=text, width=BUTTONWIDTH, height=BUTTONHEIGHT,
                            command=lambda: self.button_pressed(text), fg_color='#474747', hover_color='#333332')

    def place_buttons(self):

        self.output_frame.grid(row=0, column=0, rowspan=3, columnspan=7, sticky="nsew")
        self.top_display_output.pack(fill='x', side='top')
        self.bot_display_output.pack(fill='x', side='bottom')

        self.trig_optionmenu.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=1, pady=1)

        # Place the buttons on the grid
        self.button_2nd.grid(row=4, column=0, sticky="nsew", padx=1, pady=1)
        self.button_abs.grid(row=4, column=1, sticky="nsew", padx=1, pady=1)
        self.button_ce.grid(row=4, column=2, sticky="nsew", padx=1, pady=1)
        self.button_C.grid(row=4, column=3, sticky="nsew", padx=1, pady=1)
        self.button_bkspc.grid(row=4, column=4, sticky="nsew", padx=1, pady=1)

        self.button_x2.grid(row=5, column=0, sticky="nsew", padx=1, pady=1)
        self.button_1_x.grid(row=5, column=1, sticky="nsew", padx=1, pady=1)
        self.button_pctg.grid(row=5, column=2, sticky="nsew", padx=1, pady=1)
        self.button_mod.grid(row=5, column=3, sticky="nsew", padx=1, pady=1)
        self.button_deg.grid(row=5, column=4, sticky="nsew", padx=1, pady=1)

        self.button_sqrt.grid(row=6, column=0, sticky="nsew", padx=1, pady=1)
        self.button_pi.grid(row=6, column=1, sticky="nsew", padx=1, pady=1)
        self.button_e.grid(row=6, column=2, sticky="nsew", padx=1, pady=1)
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

    def button_pressed(self, value):
        # if user inputs a digit
        if value in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'π', 'e']:
            self.backend.add_digits_constants(value)
        elif self.backend.check_sign(value) and self.backend.evaluated_output != " ":
            self.backend.handle_signs(value)
        elif value == "2nd":
            # Toggle the '2nd' state
            self.backend.second_state = not self.backend.second_state
            # Update the functionalities of the affected buttons
            self.update_second_state()
        elif value in ["sin", "cos", "tan", "sin^-1", "cos^-1", "tan^-1"]:
            self.backend.handle_trig_functions(value)
        elif value == "C":
            self.backend.clear_all()
        elif value == "CE":
            self.backend.bot_output = ""
            self.backend.bool_bot_display = True
        elif value == "←" and self.backend.evaluated_output != "":
            self.backend.handle_backspace()
        elif value == "DEG":
            # Cycle to the next 'DEG' state
            self.backend.deg_index = (self.backend.deg_index + 1) % 2
            self.button_deg.configure(text=self.backend.deg_states[self.backend.deg_index])

        elif value == ".":
            self.backend.bool_bot_display = True
            if self.backend.dot_placed is False:
                self.backend.dot_placed = True
                self.backend.evaluated_output = self.backend.evaluated_output + "."
                self.backend.bot_output = self.backend.evaluated_output

        elif value == "+/-" and len(self.backend.evaluated_output) > 0:
            if self.backend.evaluated_output[0] == "-":
                self.backend.evaluated_output = self.backend.evaluated_output[1:]
            else:
                self.backend.evaluated_output = "-" + self.backend.evaluated_output
            self.backend.bool_top_display = True
            self.backend.bool_bot_display = True
            self.backend.bot_output = self.backend.evaluated_output
            self.backend.bool_bot_display = True
            self.output()

        elif value == "=" and self.backend.evaluated_output != "":
            if self.backend.state_calc == "":
                # Start a new thread for the calculation
                calc_thread = threading.Thread(target=self.backend.calculate_up_bot)
                calc_thread.start()
                self.output()
                self.backend.top_output = " "
                self.backend.bot_output = ""
            else:
                self.backend.finish_input = True

        elif len(self.backend.evaluated_output) > 0:
            self.backend.handle_math_functions(value)
            self.math_functions_display()

        if self.backend.evaluated_output != "" and self.backend.finish_input:
            self.backend.handle_states()

        self.output()

    def math_functions_display(self):
        """Display the math functions on the top display"""

        self.backend.bool_bot_display = True
        self.backend.bool_top_display = True
        self.output()
        if self.backend.state_calc != "":
            self.backend.top_output = self.backend.evaluated_output
            self.backend.bot_output = ""
        else:

            self.backend.bot_output = ""
            self.backend.top_output = " "

    def output(self):
        if self.backend.bool_top_display:
            self.display_upper_text()
            self.backend.bool_top_display = False
        if self.backend.bool_bot_display:
            self.display_bottom_text()
            self.backend.bool_bot_display = False

    def toggle_second(self):
        # Toggle the '2nd' state
        self.backend.second_state = not self.backend.second_state

        # Update the functionalities of the affected buttons
        self.update_second_state()

    def update_second_state(self):
        # Update the functionalities of the affected buttons based on the '2nd' state
        if self.backend.second_state:
            # Change the button texts to their '2nd' mode functions
            self.button_x2.configure(text='x^y', command=lambda: self.button_pressed('x^y'))
            self.button_sqrt.configure(text='y√x', command=lambda: self.button_pressed('y√x'))
            self.button_pc.configure(text='nCr', command=lambda: self.button_pressed('nCr'))
            self.button_exp.configure(text='2^x', command=lambda: self.button_pressed('2^x'))
            self.button_log.configure(text='log_y', command=lambda: self.button_pressed('log_y'))
            self.button_ln.configure(text='e^x', command=lambda: self.button_pressed('e^x'))

        else:
            # Change the button texts back to their normal mode functions
            self.button_x2.configure(text='x²', command=lambda: self.button_pressed('x²'))
            self.button_sqrt.configure(text='√x', command=lambda: self.button_pressed('√x'))
            self.button_pc.configure(text='nPr', command=lambda: self.button_pressed('nPr'))
            self.button_exp.configure(text='exp', command=lambda: self.button_pressed('exp'))
            self.button_log.configure(text='log', command=lambda: self.button_pressed('log'))
            self.button_ln.configure(text='ln', command=lambda: self.button_pressed('ln'))

    def display_bottom_text(self):
        self.bot_display_output.configure(text=self.backend.bot_output)

    def display_upper_text(self):
        self.top_display_output.configure(text=self.backend.top_output)


class Keyboard:
    """
    The Keyboard class allows for interaction with the calculator using the keyboard.
    """

    def __init__(self, frontend):

        """
        Initialize Keyboard with a CalculatorFrontend instance to handle user interactions.

        :param frontend: An instance of CalculatorFrontend to handle user interactions.
        """
        self.calc_front = frontend

    def keyboard_input(self, event):

        """
        Bind keyboard keys to their corresponding calculator functions.

        :param event: The keyboard event to be handled.
        """

        if event.char in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "+", "*", "-", "/", ".","%", "\\r", "\\x08"]:
            self.calc_front.button_pressed(event.char)
        elif event.char == ".":
            self.calc_front.button_pressed(event.char)
        elif event.char == "\r" or event.char == "=":
            self.calc_front.button_pressed("=")
        elif event.char == "\x08":
            self.calc_front.button_pressed("←")
        elif event.char == "s" or event.char == "S":
            self.calc_front.button_pressed("sin")
        elif event.char == "c" or event.char == "C":
            self.calc_front.button_pressed("cos")
        elif event.char == "t" or event.char == "T":
            self.calc_front.button_pressed("tan")
        elif event.state & 0x0001:
            self.calc_front.button_pressed("C")


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
    main()
