import customtkinter as ck

WIDTH = 450
HEIGHT = 600
MAX_LENGTH = 16
BUTTONWIDTH = 85
BUTTONHEIGHT = 55


class Calculator(ck.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calculator")
        self.geometry("500x650")
        self.minsize(WIDTH, HEIGHT)
        self.maxsize(WIDTH, HEIGHT)

        self.bot_display_output = ck.CTkLabel(self, text="", font=("Arial", 40))
        self.bot_display_output.place(relx=0.95, rely=0.15, anchor="e")

        self.top_display_output = ck.CTkLabel(self, text="", font=("Arial", 30), text_color="grey")
        self.top_display_output.place(relx=0.95, rely=0.07, anchor="e")



        self.top_output = ""
        self.bot_output = ""
        self.eval_expression = None
        self.dot_placed = False

        self.button_0 = ck.CTkButton(self, text="0", width=BUTTONWIDTH, height=BUTTONHEIGHT,
                                     command=lambda: self.ButtonPressed("0"))
        self.button_1 = ck.CTkButton(self, text="1", width=BUTTONWIDTH, height=BUTTONHEIGHT,
                                     command=lambda: self.ButtonPressed("1"))
        self.button_2 = ck.CTkButton(self, text="2", width=BUTTONWIDTH, height=BUTTONHEIGHT,
                                     command=lambda: self.ButtonPressed("2"))
        self.button_3 = ck.CTkButton(self, text="3", width=BUTTONWIDTH, height=BUTTONHEIGHT,
                                     command=lambda: self.ButtonPressed("3"))
        self.button_4 = ck.CTkButton(self, text="4", width=BUTTONWIDTH, height=BUTTONHEIGHT,
                                     command=lambda: self.ButtonPressed("4"))
        self.button_5 = ck.CTkButton(self, text="5", width=BUTTONWIDTH, height=BUTTONHEIGHT,
                                     command=lambda: self.ButtonPressed("5"))
        self.button_6 = ck.CTkButton(self, text="6", width=BUTTONWIDTH, height=BUTTONHEIGHT,
                                     command=lambda: self.ButtonPressed("6"))
        self.button_7 = ck.CTkButton(self, text="7", width=BUTTONWIDTH, height=BUTTONHEIGHT,
                                     command=lambda: self.ButtonPressed("7"))
        self.button_8 = ck.CTkButton(self, text="8", width=BUTTONWIDTH, height=BUTTONHEIGHT,
                                     command=lambda: self.ButtonPressed("8"))
        self.button_9 = ck.CTkButton(self, text="9", width=BUTTONWIDTH, height=BUTTONHEIGHT,
                                     command=lambda: self.ButtonPressed("9"))
        self.button_dot = ck.CTkButton(self, text=".", width=BUTTONWIDTH, height=BUTTONHEIGHT,
                                       command=lambda: self.ButtonPressed("."))
        self.button_change_sign = ck.CTkButton(self, text="+/-", width=BUTTONWIDTH, height=BUTTONHEIGHT,
                                               command=lambda: self.ButtonPressed("+/-"))
        self.button_plus = ck.CTkButton(self, text="+", width=BUTTONWIDTH, height=BUTTONHEIGHT,
                                        command=lambda: self.ButtonPressed("+"))
        self.button_minus = ck.CTkButton(self, text="-", width=BUTTONWIDTH, height=BUTTONHEIGHT,
                                         command=lambda: self.ButtonPressed("-"))
        self.button_multi = ck.CTkButton(self, text="x", width=BUTTONWIDTH, height=BUTTONHEIGHT,
                                         command=lambda: self.ButtonPressed("*"))
        self.button_div = ck.CTkButton(self, text="/", width=BUTTONWIDTH, height=BUTTONHEIGHT,
                                       command=lambda: self.ButtonPressed("/"))
        self.button_equal = ck.CTkButton(self, text="=", width=BUTTONWIDTH, height=BUTTONHEIGHT,
                                         command=lambda: self.ButtonPressed("="))
        self.button_bkspc = ck.CTkButton(self, text="←", width=BUTTONWIDTH, height=BUTTONHEIGHT,
                                         command=lambda: self.ButtonPressed("←"))
        self.button_sqrt = ck.CTkButton(self, text="√x", width=BUTTONWIDTH, height=BUTTONHEIGHT,
                                        command=lambda: self.ButtonPressed("√x"))
        self.button_C = ck.CTkButton(self, text="C", width=BUTTONWIDTH, height=BUTTONHEIGHT,
                                     command=lambda: self.ButtonPressed("C"))
        self.button_CE = ck.CTkButton(self, text="CE", width=BUTTONWIDTH, height=BUTTONHEIGHT,
                                      command=lambda: self.ButtonPressed("CE"))
        self.button_sqr = ck.CTkButton(self, text="x²", width=BUTTONWIDTH, height=BUTTONHEIGHT,
                                       command=lambda: self.ButtonPressed("x²"))
        self.button_perc = ck.CTkButton(self, text="%", width=BUTTONWIDTH, height=BUTTONHEIGHT,
                                        command=lambda: self.ButtonPressed("%"))
        self.button_inv = ck.CTkButton(self, text="1/x", width=BUTTONWIDTH, height=BUTTONHEIGHT,
                                       command=lambda: self.ButtonPressed("1/x"))

        # scientific buttons
        self.button_sin = ck.CTkButton(self, text="sin", width=BUTTONWIDTH, height=BUTTONHEIGHT,
                                       command=lambda: self.ButtonPressed("sin"))
        self.button_cos = ck.CTkButton(self, text="cos", width=BUTTONWIDTH, height=BUTTONHEIGHT,
                                       command=lambda: self.ButtonPressed("cos"))
        self.button_tan = ck.CTkButton(self, text="tan", width=BUTTONWIDTH, height=BUTTONHEIGHT,
                                       command=lambda: self.ButtonPressed("tan"))
        self.button_log = ck.CTkButton(self, text="log", width=BUTTONWIDTH, height=BUTTONHEIGHT,
                                       command=lambda: self.ButtonPressed("log"))
        self.button_ln = ck.CTkButton(self, text="ln", width=BUTTONWIDTH, height=BUTTONHEIGHT,
                                      command=lambda: self.ButtonPressed("ln"))
        self.button_exp = ck.CTkButton(self, text="exp", width=BUTTONWIDTH, height=BUTTONHEIGHT,
                                       command=lambda: self.ButtonPressed("exp"))
        self.button_factorial = ck.CTkButton(self, text="!", width=BUTTONWIDTH, height=BUTTONHEIGHT,
                                             command=lambda: self.ButtonPressed("!"))
        self.button_pi = ck.CTkButton(self, text="π", width=BUTTONWIDTH, height=BUTTONHEIGHT,
                                      command=lambda: self.ButtonPressed("π"))
        self.button_e = ck.CTkButton(self, text="e", width=BUTTONWIDTH, height=BUTTONHEIGHT,
                                     command=lambda: self.ButtonPressed("e"))

        self.PlaceButtonSimple()

        # # Create the sidebar
        # self.sidebar = ck.CTkFrame(self, width=200)
        # self.sidebar.pack(side=ck.LEFT, fill=ck.Y)
        #
        # # Add buttons to the sidebar
        # self.standard_button = ck.CTkButton(self.sidebar, text='Standard', command=self.switch_to_standard)
        # self.standard_button.pack(fill=ck.X)
        # self.scientific_button = ck.CTkButton(self.sidebar, text='Scientific', command=self.switch_to_scientific)
        # self.scientific_button.pack(fill=ck.X)
        #
        # # Hide the sidebar initially
        # self.sidebar.pack_forget()
        #
        # # Create a hamburger button
        # self.hamburger_button = ck.CTkButton(self, text='≡', command=self.toggle_sidebar)
        # self.hamburger_button.pack(anchor=ck.NW)
        #
        # # Create a mode label
        # self.mode_label = ck.CTkLabel(self, text='')
        # self.mode_label.pack(anchor=ck.N)

    def PlaceButtonSimple(self):
        self.button_equal.place(relx=0.885, rely=0.90, anchor="center")
        self.button_plus.place(relx=0.885, rely=0.80, anchor="center")
        self.button_minus.place(relx=0.885, rely=0.70, anchor="center")
        self.button_multi.place(relx=0.885, rely=0.60, anchor="center")
        self.button_div.place(relx=0.885, rely=0.50, anchor="center")
        self.button_bkspc.place(relx=0.885, rely=0.40, anchor="center")

        self.button_dot.place(relx=0.69, rely=0.90, anchor="center")
        self.button_3.place(relx=0.69, rely=0.80, anchor="center")
        self.button_6.place(relx=0.69, rely=0.70, anchor="center")
        self.button_9.place(relx=0.69, rely=0.60, anchor="center")
        self.button_sqrt.place(relx=0.69, rely=0.50, anchor="center")
        self.button_C.place(relx=0.69, rely=0.40, anchor="center")

        self.button_0.place(relx=0.495, rely=0.90, anchor="center")
        self.button_2.place(relx=0.495, rely=0.80, anchor="center")
        self.button_5.place(relx=0.495, rely=0.70, anchor="center")
        self.button_8.place(relx=0.495, rely=0.60, anchor="center")
        self.button_sqr.place(relx=0.495, rely=0.50, anchor="center")
        self.button_CE.place(relx=0.495, rely=0.40, anchor="center")

        self.button_change_sign.place(relx=0.3, rely=0.90, anchor="center")
        self.button_1.place(relx=0.299, rely=0.80, anchor="center")
        self.button_4.place(relx=0.299, rely=0.70, anchor="center")
        self.button_7.place(relx=0.299, rely=0.60, anchor="center")
        self.button_inv.place(relx=0.299, rely=0.50, anchor="center")
        self.button_perc.place(relx=0.299, rely=0.40, anchor="center")

        self.button_sin.place(relx=0.1, rely=0.2, anchor="center")
        self.button_cos.place(relx=0.1, rely=0.3, anchor="center")
        self.button_tan.place(relx=0.1, rely=0.4, anchor="center")
        self.button_log.place(relx=0.1, rely=0.5, anchor="center")
        self.button_ln.place(relx=0.1, rely=0.6, anchor="center")
        self.button_exp.place(relx=0.1, rely=0.7, anchor="center")
        self.button_factorial.place(relx=0.1, rely=0.8, anchor="center")
        self.button_pi.place(relx=0.1, rely=0.9, anchor="center")
        self.button_e.place(relx=0.1, rely=1.0, anchor="center")

        # Bind the Key event
        self.bind('<Key>', self.keyboard_input)

    # def toggle_sidebar(self):
    #     # This method is called when the hamburger button is clicked
    #     if self.sidebar.winfo_viewable():
    #         # If the sidebar is currently visible, hide it
    #         self.sidebar.pack_forget()
    #     else:
    #         # If the sidebar is currently hidden, show it
    #         self.sidebar.pack(side=ck.LEFT, fill=ck.Y)

    # def switch_to_standard(self):
    #     # This method is called when the 'Standard' button is clicked
    #     self.mode_label['text'] = 'Standard'
    #
    # def switch_to_scientific(self):
    #     # This method is called when the 'Scientific' button is clicked
    #     self.mode_label['text'] = 'Scientific'

    def ButtonPressed(self, value):
        if value == "1" or value == "2" or value == "3" or value == "4" or value == "5" or value == "6" or value == "7" \
                or value == "8" or value == "9" or value == "0":

            if len(self.bot_output) <= 15:
                self.bot_output += value
                self.DisplayBottomText()

        elif value == "+" or value == "*" or value == "-" or value == "/":
            if len(self.top_output) > 0:
                temp_num = self.top_output[len(self.top_output) - 1]
            else:
                temp_num = None
            if temp_num == "+" or temp_num == "-" or temp_num == "/" or temp_num == "x":
                self.top_output = self.top_output[:-1] + value
                self.bot_output = ""
                self.DisplayUpperText()
            else:
                self.top_output = self.bot_output + " " + value
                self.bot_output = ""
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

    # allow user to use keyboard
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

    def DisplayBottomText(self):
        self.bot_display_output.configure(text=self.bot_output)

    def DisplayUpperText(self):
        self.top_display_output.configure(text=self.top_output)

    def EvaluateExpression(self):
        output = self.top_output + " " + self.bot_output
        eval_output = eval(output)
        self.top_output = str(eval_output)
        self.top_display_output.configure(text=output + " =")
        self.bot_display_output.configure(text=eval_output)

    def test(self):
        pass


def Main():
    new_app = Calculator()
    new_app.mainloop()


Main()
