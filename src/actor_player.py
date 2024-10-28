import tkinter as tk
from tkinter import ttk
from tkinter import Button, Frame, Label, Text, Entry, Menu, messagebox, simpledialog, END, NORMAL, DISABLED
import random
from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor

class PlayerInterface(DogPlayerInterface):
    def __init__(self, root):
        self.root = root
        self.root.title("Codenames")
        self.root.geometry("1100x400")
        
        menubar = Menu(self.root)
        game_menu = Menu(menubar, tearoff=0)
        game_menu.add_command(label="Start match", command=self.start_match)
        game_menu.add_command(label="Start game", command=self.start_game)
        menubar.add_cascade(label="Game", menu=game_menu)
        self.root.config(menu=menubar)

        self.card_frame = Frame(self.root, padx=10, pady=10)
        self.card_frame.grid(row=0, column=1, padx=10, pady=10)
        
        self.card_colors = ['red'] * 9 + ['blue'] * 8 + ['black'] * 1 + ['white'] * 7
        random.shuffle(self.card_colors)
        
        self.buttons = []
        for row in range(5):
            row_buttons = []
            for col in range(5):
                color = self.card_colors.pop(0)
                button = Button(self.card_frame, text="Palavra", width=15, height=3, relief="solid", borderwidth=1, bg=color)
                button.grid(row=row, column=col, padx=2, pady=2)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

        self.red_team_frame = Frame(self.root, padx=10, pady=10, bg="red")
        self.red_team_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.red_team_label = Label(self.red_team_frame, text="Time vermelho\ncartas restantes", bg="red", fg="black", font=("Arial", 16))
        self.red_team_label.pack()
        self.hint_display_left = Text(self.red_team_frame, height=4, width=20)
        self.hint_display_left.pack(pady=10)
        self.hint_display_left.config(state=DISABLED)
        self.skip_button_left = Button(self.red_team_frame, text="Passar turno", command=self.skip_turn)
        self.skip_button_left.pack(pady=5)

        self.blue_team_frame = Frame(self.root, padx=10, pady=10, bg="blue")
        self.blue_team_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
        self.blue_team_label = Label(self.blue_team_frame, text="Time azul\ncartas restantes", bg="blue", fg="black", font=("Arial", 16))
        self.blue_team_label.pack()
        self.hint_display_right = Text(self.blue_team_frame, height=4, width=20)
        self.hint_display_right.pack(pady=10)
        self.hint_display_right.config(state=DISABLED)
        self.skip_button_right = Button(self.blue_team_frame, text="Passar turno", command=self.skip_turn)
        self.skip_button_right.pack(pady=5)

        self.input_frame = Frame(self.root)
        self.input_frame.grid(row=1, column=1, pady=10)

        self.hint_label = Label(self.input_frame, text="Digite a dica")
        self.hint_label.pack(side=tk.LEFT)
        self.hint_entry = Entry(self.input_frame, width=30)
        self.hint_entry.pack(side=tk.LEFT, padx=5)

        self.number_selector = ttk.Combobox(self.input_frame, values=list(range(1, 10)), width=3)
        self.number_selector.set(1)
        self.number_selector.pack(side=tk.LEFT, padx=5)

        self.submit_button = Button(self.input_frame, text="Submit", command=self.submit_hint)
        self.submit_button.pack(side=tk.LEFT, padx=5)

        player_name = simpledialog.askstring(title="Player identification", prompt="Insira seu nome: ")
        self.dog_server_interface = DogActor()
        message = self.dog_server_interface.initialize(player_name, self)
        messagebox.showinfo(message=message)

    def submit_hint(self):
        hint = self.hint_entry.get()
        number = self.number_selector.get()
        self.hint_display_left.config(state=NORMAL)
        self.hint_display_right.config(state=NORMAL)
        
        self.hint_display_left.delete(1.0, END)
        self.hint_display_right.delete(1.0, END)
        
        self.hint_display_left.insert(END, f"{hint}\n{number}")
        self.hint_display_right.insert(END, f"{hint}\n{number}")
        
        self.hint_display_left.config(state=DISABLED)
        self.hint_display_right.config(state=DISABLED)
        
        self.hint_entry.delete(0, END)

    def skip_turn(self):
        self.hint_display_left.config(state=NORMAL)
        self.hint_display_right.config(state=NORMAL)
        
        self.hint_display_left.delete(1.0, END)
        self.hint_display_right.delete(1.0, END)
        
        self.hint_display_left.config(state=DISABLED)
        self.hint_display_right.config(state=DISABLED)

    def start_match(self):
        start_status = self.dog_server_interface.start_match(4)
        message = start_status.get_message()
        messagebox.showinfo(message=message)
    
    def start_game(self):
        print("starting game...")

    def receive_start(self, start_status):
        message = start_status.get_message()
        messagebox.showinfo(message=message)

if __name__ == "__main__":
    root = tk.Tk()
    player_interface = PlayerInterface(root)
    root.mainloop()
