import customtkinter as ck
import tkinter as tk
import math
import sympy as sp

# Constants for the GUI size
WIDTH = 400
HEIGHT = 600
MAX_LENGTH = 16
BUTTONWIDTH = 50
BUTTONHEIGHT = 50
DROPDOWNWIDTH = 50
DROPDOWNHEIGHT = 30

# Constants color for the GUI
TOPCOLOR = '#212121'


class Calculator(ck.CTk):
    def __init__(self):
        super().__init__()

        # GUI setup
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
        for i in range(11):
            self.grid_rowconfigure(i, weight=1)

        # Display outputs
        output_frame = ck.CTkFrame(self, fg_color='#292929')
        output_frame.grid(row=0, column=0, rowspan=3, columnspan=7, sticky="nsew")

        # Display outputs
        self.top_display_output = ck.CTkLabel(output_frame, text="", font=("Arial", 30), text_color="grey", anchor="e")
        self.top_display_output.pack(fill='x', side='top')

        self.bot_display_output = ck.CTkLabel(output_frame, text="", font=("Arial", 40), anchor="e")
        self.bot_display_output.pack(fill='x', side='bottom')

        # Initialize the calculator state
        self.top_output = ""
        self.bot_output = ""
        self.eval_expression = None
        self.dot_placed = False

        # Define buttons according to the provided layout
        self.define_buttons()

        # Place the buttons on the grid
        self.place_buttons()

    def define_buttons(self):
        # Define the button properties

        # self.button_trig = ck.CTkButton(self, text="Trig", width=BUTTONWIDTH, height=40,
        #                                 command=lambda: self.ButtonPressed("Trig"), fg_color='#21211f', hover_color='#474747')
        # self.button_var = ck.CTkButton(self, text="Var", width=BUTTONWIDTH, height=40,
        #                                command=lambda: self.ButtonPressed("Var"), fg_color='#21211f', hover_color='#474747')

        self.button_2nd = self.create_button("2nd")
        self.button_pi = self.create_button("π")
        self.button_e = self.create_button("e")
        self.button_C = self.create_button("C")
        self.button_bkspc = self.create_button("←")

        self.button_x2 = self.create_button("x²")
        self.button_1_x = self.create_button("1/x")
        self.button_pctg = self.create_button("%")
        self.button_mod = self.create_button("mod")
        self.button_deg = self.create_button(self.deg_states[self.deg_index])

        self.button_sqrt = self.create_button("√x")
        self.button_lparen = self.create_button("(")
        self.button_rparen = self.create_button(")")
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
                            command=lambda: self.ButtonPressed("="), fg_color='#16638a', hover_color='#0f4561')
        # Bind the Key event
        self.bind('<Key>', self.keyboard_input)

    def create_button(self, text):
        # Helper function to create a button
        return ck.CTkButton(self, text=text, width=BUTTONWIDTH, height=BUTTONHEIGHT,
                            command=lambda: self.ButtonPressed(text), fg_color='#333332', hover_color='#474747')

    def create_num_button(self, text):
        # Helper function to create a button
        return ck.CTkButton(self, text=text, width=BUTTONWIDTH, height=BUTTONHEIGHT,
                            command=lambda: self.ButtonPressed(text), fg_color='#474747', hover_color='#333332')

    def place_buttons(self):
        # Place the buttons on the grid

        # self.button_trig.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=1, pady=1)
        # self.button_var.grid(row=3, column=2, columnspan=2, sticky="nsew", padx=1, pady=1)

        self.button_2nd.grid(row=4, column=0, sticky="nsew", padx=1, pady=1)
        self.button_pi.grid(row=4, column=1, sticky="nsew", padx=1, pady=1)
        self.button_e.grid(row=4, column=2, sticky="nsew", padx=1, pady=1)
        self.button_C.grid(row=4, column=3, sticky="nsew", padx=1, pady=1)
        self.button_bkspc.grid(row=4, column=4, sticky="nsew", padx=1, pady=1)

        self.button_x2.grid(row=5, column=0, sticky="nsew", padx=1, pady=1)
        self.button_1_x.grid(row=5, column=1, sticky="nsew", padx=1, pady=1)
        self.button_pctg.grid(row=5, column=2, sticky="nsew", padx=1, pady=1)
        self.button_mod.grid(row=5, column=3, sticky="nsew", padx=1, pady=1)
        self.button_deg.grid(row=5, column=4, sticky="nsew", padx=1, pady=1)

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

        # Define the trig option menu
        trig_options = ["sin", "cos", "tan", "hyp", "sin^-1", "cos^-1", "tan^-1"]
        self.trig_optionmenu_var = ck.StringVar(value="Trig")
        self.trig_optionmenu = ck.CTkOptionMenu(self, values=trig_options, command=self.ButtonPressed,
                                                variable=self.trig_optionmenu_var, fg_color='#21211f', button_color='#21211f', button_hover_color='#474747')
        self.trig_optionmenu.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=1, pady=1)

        # Define the var option menu
        var_options = ["a", "b", "c", "d", "e"]
        self.var_optionmenu_var = ck.StringVar(value="Var")
        self.var_optionmenu = ck.CTkOptionMenu(self, values=var_options, command=self.ButtonPressed,
                                               variable=self.var_optionmenu_var, fg_color='#21211f', button_color='#21211f', button_hover_color='#474747')
        self.var_optionmenu.grid(row=3, column=2, columnspan=2, sticky="nsew", padx=1, pady=1)

    # TODO: Implement the logic of each button press
    def ButtonPressed(self, value):
        if value in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']:
            if len(self.bot_output) <= 15:
                self.bot_output += value
                self.DisplayBottomText()

        elif value in ['+', '-', '*', '/']:
            if len(self.top_output) > 0:
                temp_num = self.top_output[len(self.top_output) - 1]
            else:
                temp_num = None
            if temp_num in ['+', '-', '/', '*']:
                self.top_output = self.top_output[:-1] + value
                self.bot_output = ""
                self.DisplayUpperText()
                self.DisplayUpperText()
            else:
                self.top_output += self.bot_output + " " + value
                self.bot_output = ""
                self.DisplayUpperText()

        elif value == "sin":
            self.top_output += "sin("
            self.DisplayUpperText()
        elif value == "cos":
            self.top_output += "cos("
            self.DisplayUpperText()
        elif value == "tan":
            self.top_output += "tan("
            self.DisplayUpperText()
        elif value == "x^2":
            if self.bot_output != "":
                self.top_output += self.bot_output + " ** 2 "
                self.bot_output = ""
                self.DisplayUpperText()
            else:
                self.top_output += " ** 2 "
                self.DisplayUpperText()

        elif value == "x^y":
            if self.bot_output != "":
                self.top_output += self.bot_output + " ** "
                self.bot_output = ""
                self.DisplayUpperText()
            else:
                self.top_output += " ** "
                self.DisplayUpperText()

        elif value == "√x":
            self.top_output += "sqrt("
            self.DisplayUpperText()

        elif value == "C":
            self.bot_output = ""
            self.top_output = ""
            self.DisplayBottomText()
            self.DisplayUpperText()
        elif value == "CE":
            self.bot_output = ""
            self.DisplayBottomText()
        elif value == "←" and len(self.bot_output) > 0:
            if self.bot_output[len(self.bot_output) - 1] == ".":
                self.dot_placed = False
            self.bot_output = self.bot_output[:-1]
            self.DisplayBottomText()
        elif value == "." and self.dot_placed is False:
            self.dot_placed = True
            self.bot_output = self.bot_output + "."
            self.DisplayBottomText()
        elif value == "+/-" and len(self.bot_output) > 0 and self.bot_output[0] == "-":
            self.bot_output = self.bot_output[1:]
            self.DisplayBottomText()
        elif value == "+/-":
            self.bot_output = "-" + self.bot_output
            self.DisplayBottomText()
        elif value == "=":
            self.EvaluateExpression()

            # Bind the Key event
            self.bind('<Key>', self.keyboard_input)

        elif value == "2nd":
            # Toggle the '2nd' state
            self.second_state = not self.second_state
            # Update the functionalities of the affected buttons
            self.update_second_state()

        elif value == "Trig":
            # Show the trigonometry dropdown menu
            if value in ["sin", "cos", "tan", "sin^-1", "cos^-1", "tan^-1"]:
                self.top_output += value + "("
                self.DisplayUpperText()

        elif value == "Var":
            # Show the variable dropdown menu
            # Handle variables
            if value in ["a", "b", "c", "d", "e"]:  # add more variables if needed
                self.bot_output += value
                self.DisplayBottomText()

        elif value == "DEG":
            # Cycle to the next 'DEG' state
            self.deg_index = (self.deg_index + 1) % 2
            self.button_deg.configure(text=self.deg_states[self.deg_index])

            # Handle trig functions

            # # Bind the Key event
            # self.bind('<Key>', self.keyboard_input)

    # allow user to use keyboard
    def keyboard_input(self, event):

        if event.char in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "+", "*", "-", "/", ".", "\\r", "\\x08"]:
            self.ButtonPressed(event.char)

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
            self.button_x2.configure(text='x^2')
            self.button_sqrt.configure(text='sqrt')
            self.button_pc.configure(text='nPr')
            self.button_exp.configure(text='exp')
            self.button_log.configure(text='log')
            self.button_ln.configure(text='ln')



    # def trig_update_second_state(self):
    #     # Update the functionalities of the trigonometry buttons based on the '2nd' state
    #     if self.trig_second_state:
    #         # Change the button texts to their inverse functions
    #         self.button_sin.configure(text='sin^-1')
    #         self.button_cos.configure(text='cos^-1')
    #         # Continue for the other trigonometric functions
    #     else:
    #         # Change the button texts back to their normal mode functions
    #         self.button_sin.configure(text='sin')
    #         self.button_cos.configure(text='cos')
    #         # Continue for the other trigonometric functions

    # def show_trig_menu(self):
    #     if self.trig_menu_open:
    #         # Destroy the frame and set the state to False
    #         self.trig_frame.destroy()
    #         self.trig_menu_open = False
    #     else:
    #         # Create a new Frame widget
    #         self.trig_frame = ck.CTkFrame(self, fg_color='white')
    #
    #         # Define the new function buttons within this frame
    #         self.button_second = ck.CTkButton(self.trig_frame, text='2nd', width=DROPDOWNWIDTH, height=DROPDOWNHEIGHT,
    #                                           command=self.toggle_trig_second, fg_color='grey')
    #         self.button_sin = ck.CTkButton(self.trig_frame, text='sin', width=DROPDOWNWIDTH, height=DROPDOWNHEIGHT,
    #                                        command=lambda: self.ButtonPressed('sin'), fg_color='grey')
    #         self.button_cos = ck.CTkButton(self.trig_frame, text='cos', width=DROPDOWNWIDTH, height=DROPDOWNHEIGHT,
    #                                        command=lambda: self.ButtonPressed('cos'), fg_color='grey')
    #         # TODO: Continue for the other trigonometric functions
    #
    #         # Place the new function buttons on the grid within the frame
    #         self.button_second.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
    #         self.button_sin.grid(row=0, column=1, sticky="nsew", padx=1, pady=1)
    #         self.button_cos.grid(row=0, column=2, sticky="nsew", padx=1, pady=1)
    #
    #         # TODO: Continue for the other trigonometric functions
    #
    #         # Place the frame over the existing grid
    #         self.trig_frame.place(x=self.button_trig.winfo_x(),
    #                               y=self.button_trig.winfo_y() + 30)
    #
    #         # Set the state to True
    #         self.trig_menu_open = True

    # def toggle_trig_second(self):
    #     # Toggle the '2nd' state for the trigonometry functions
    #     self.trig_second_state = not self.trig_second_state
    #
    #     # Update the functionalities of the affected buttons
    #     self.trig_update_second_state()
    #
    # def show_var_menu(self):
    #     if self.var_menu_open:
    #         # Destroy the frame and set the state to False
    #         self.var_frame.destroy()
    #         self.var_menu_open = False
    #     else:
    #         # Create a new Frame widget
    #         self.var_frame = ck.CTkFrame(self, fg_color='white')
    #
    #         # Define the new function buttons within this frame
    #         button_a = ck.CTkButton(self.var_frame, text='a', width=DROPDOWNWIDTH, height=DROPDOWNHEIGHT,
    #                                 command=lambda: self.ButtonPressed('a'), fg_color='grey')
    #         button_b = ck.CTkButton(self.var_frame, text='b', width=DROPDOWNWIDTH, height=DROPDOWNHEIGHT,
    #                                 command=lambda: self.ButtonPressed('b'), fg_color='grey')
    #         # TODO: Continue for the other functions
    #
    #         # Place the new function buttons on the grid within the frame
    #         button_a.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
    #         button_b.grid(row=0, column=1, sticky="nsew", padx=1, pady=1)
    #         # TODO: Continue for the other functions
    #
    #         # Place the frame over the existing grid
    #         self.var_frame.place(x=self.button_var.winfo_x(),
    #                              y=self.button_var.winfo_y() + 30)
    #
    #         # Set the state to True
    #         self.var_menu_open = True

    def DisplayBottomText(self):
        self.bot_display_output.configure(text=self.bot_output)

    def DisplayUpperText(self):
        self.top_display_output.configure(text=self.top_output)

    def EvaluateExpression(self):
        if len(self.top_output) > 0 and self.top_output[-1] in ['sin(', 'cos(', 'tan(', 'sqrt(', '**', 'log10(', 'log(',
                                                                'factorial(']:
            self.top_output += self.bot_output + ")"
        else:
            self.top_output += " " + self.bot_output
        output = self.top_output
        try:
            eval_output = sp.sympify(output)
            # Check if the decimal part has a long tail of zeros
            if eval_output.is_real and eval_output != int(eval_output):
                str_output = str(eval_output.evalf())
                if len(str_output.split('.')[1].rstrip('0')) < 10:
                    eval_output = round(eval_output, 5)
            eval_output = str(eval_output)
        except:
            eval_output = "Math Error"
        self.top_output = ""
        self.bot_display_output.configure(text=eval_output)
        self.bot_output = eval_output

    def test(self):
        pass


# Create an instance of the Calculator class and start the GUI
def main():
    new_app = Calculator()
    new_app.mainloop()


main()
