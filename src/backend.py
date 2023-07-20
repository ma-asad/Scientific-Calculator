import math
import sympy as sp


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

        if self.evaluated_output == " ":
            return

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
            self.top_output = top_value
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
        expression = ""
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
            self.top_output = expression
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
