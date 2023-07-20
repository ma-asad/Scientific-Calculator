import customtkinter as ck
import threading

# Constants for the GUI size
WIDTH = 350
HEIGHT = 500
MAX_LENGTH = 16
BUTTONWIDTH = 60
BUTTONHEIGHT = 10


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

        ck.set_appearance_mode("dark")
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

        if event.char in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "+", "*", "-", "/", ".", "%", "\\r",
                          "\\x08"]:
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
