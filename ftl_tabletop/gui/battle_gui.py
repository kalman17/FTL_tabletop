import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import random

# Import your attack logic
from ..logic.attacks import attack_ship_general, attack_ship_targeted

class BattleGUI:
    def __init__(self, root):
        self.root = root

        # Store some placeholders for inputs
        self.ship_evasion = 0
        self.num_rooms = 1
        self.enemy_hull = 1
        self.attacker_mod = 0

        self.create_setup_frame()

    def create_setup_frame(self):
        self.setup_frame = tk.Frame(self.root, padx=10, pady=10)
        self.setup_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.setup_frame, text="=== New Battle Setup ===", font=("Arial", 16)).grid(
            row=0, column=0, columnspan=2, pady=10
        )

        tk.Label(self.setup_frame, text="Enemy Ship Evasion:").grid(row=1, column=0, sticky=tk.E, pady=5)
        self.ship_evasion_entry = tk.Entry(self.setup_frame)
        self.ship_evasion_entry.grid(row=1, column=1, pady=5)

        tk.Label(self.setup_frame, text="Number of Rooms:").grid(row=2, column=0, sticky=tk.E, pady=5)
        self.num_rooms_entry = tk.Entry(self.setup_frame)
        self.num_rooms_entry.grid(row=2, column=1, pady=5)

        tk.Label(self.setup_frame, text="Enemy Hull (HP):").grid(row=3, column=0, sticky=tk.E, pady=5)
        self.enemy_hull_entry = tk.Entry(self.setup_frame)
        self.enemy_hull_entry.grid(row=3, column=1, pady=5)

        tk.Label(self.setup_frame, text="Your Attack Modifier:").grid(row=4, column=0, sticky=tk.E, pady=5)
        self.attacker_mod_entry = tk.Entry(self.setup_frame)
        self.attacker_mod_entry.grid(row=4, column=1, pady=5)

        tk.Button(self.setup_frame, text="Start Battle", command=self.start_battle).grid(
            row=5, column=0, columnspan=2, pady=10
        )

    def start_battle(self):
        try:
            self.ship_evasion = int(self.ship_evasion_entry.get())
            self.num_rooms = int(self.num_rooms_entry.get())
            self.enemy_hull = int(self.enemy_hull_entry.get())
            self.attacker_mod = int(self.attacker_mod_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid integers.")
            return

        if self.ship_evasion < 0 or self.num_rooms < 1 or self.enemy_hull < 1:
            messagebox.showerror("Invalid Input", "Evasion, Number of Rooms, and Hull must be positive.")
            return

        print(f"\nEnemy Ship Evasion: {self.ship_evasion}")
        T_near = self.ship_evasion + 10
        T_perfect_raw = T_near + 0.2 * self.ship_evasion
        T_perfect = max(T_perfect_raw, T_near + 5)
        print(f"\nT_near: {T_near},\nT_perfect: {T_perfect}\n")

        # Hide setup frame
        self.setup_frame.pack_forget()

        # Create battle frame
        self.battle_frame = tk.Frame(self.root, padx=10, pady=10)
        self.battle_frame.pack(fill=tk.BOTH, expand=True)

        # Enemy Hull display
        self.hull_label = tk.Label(
            self.battle_frame, text=f"Enemy Hull: {self.enemy_hull}", font=("Arial", 14)
        )
        self.hull_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Toggle for auto/manual
        self.auto_roll = tk.BooleanVar(value=True)
        self.auto_roll_checkbox = tk.Checkbutton(
            self.battle_frame, text="Automatic Roll", variable=self.auto_roll
        )
        self.auto_roll_checkbox.grid(row=1, column=0, sticky=tk.W)

        # Attack Buttons
        self.general_shot_button = tk.Button(
            self.battle_frame, text="General Shot", width=15, command=self.general_shot
        )
        self.general_shot_button.grid(row=2, column=0, pady=5)

        self.targeted_shot_button = tk.Button(
            self.battle_frame, text="Targeted Shot", width=15, command=self.show_targeted_ui
        )
        self.targeted_shot_button.grid(row=2, column=1, pady=5)

        # Place for log
        self.battle_log = tk.Text(self.battle_frame, height=15, width=60, state=tk.DISABLED, wrap=tk.WORD)
        self.battle_log.grid(row=4, column=0, columnspan=3, pady=10)

        # Hide targeted UI until needed
        self.targeted_ui_shown = False

    def log(self, text):
        self.battle_log.config(state=tk.NORMAL)
        self.battle_log.insert(tk.END, text + "\n\n")
        self.battle_log.see(tk.END)
        self.battle_log.config(state=tk.DISABLED)

    def general_shot(self):
        if self.auto_roll.get():
            roll_val = random.randint(1, 100)
            self.log(f"General Shot: Rolled {roll_val} + {self.attacker_mod} = {roll_val + self.attacker_mod}")
        else:
            roll_val = self.ask_for_roll()
            if roll_val is None:
                return  # user canceled or invalid

        result = attack_ship_general(roll_val, self.attacker_mod, self.ship_evasion, self.num_rooms)
        self.process_battle_result(result)

    def show_targeted_ui(self):
        if self.targeted_ui_shown:
            return
        self.targeted_ui_shown = True

        # We'll put a label + dropdown for choosing a room
        self.room_label = tk.Label(self.battle_frame, text="Target which room?")
        self.room_label.grid(row=3, column=0, sticky=tk.E, pady=5)
        self.room_combobox = ttk.Combobox(
            self.battle_frame, state="readonly", values=list(range(1, self.num_rooms + 1))
        )
        self.room_combobox.current(0)
        self.room_combobox.grid(row=3, column=1, sticky=tk.W, pady=5)

        # A button to fire
        self.fire_button = tk.Button(self.battle_frame, text="Fire Targeted Shot", command=self.targeted_shot)
        self.fire_button.grid(row=3, column=2, pady=5)

    def targeted_shot(self):
        if not self.targeted_ui_shown:
            return
        try:
            target_room = int(self.room_combobox.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Select a valid room.")
            return

        if self.auto_roll.get():
            roll_val = random.randint(1, 100)
            self.log(f"Targeted Shot at Room #{target_room}: Rolled {roll_val} + {self.attacker_mod} = {roll_val + self.attacker_mod}")
        else:
            roll_val = self.ask_for_roll()
            if roll_val is None:
                return

        result = attack_ship_targeted(
            roll_val=roll_val,
            attacker_mod=self.attacker_mod,
            ship_evasion=self.ship_evasion,
            num_rooms=self.num_rooms,
            target_room=target_room
        )
        self.process_battle_result(result)

    def process_battle_result(self, result):
        self.log(result)
        if "Hit" in result or "Near miss" in result:
            self.enemy_hull -= 1
            self.hull_label.config(text=f"Enemy Hull: {self.enemy_hull}")
            if self.enemy_hull <= 0:
                messagebox.showinfo("Victory", "The enemy ship is defeated!")
                self.reset_to_setup()

    def ask_for_roll(self):
        """
        Show a small prompt for the user to manually enter a roll.
        Return None if invalid or canceled, otherwise an int.
        """
        roll_str = simpledialog.askstring("Manual Roll", "Enter your d100 roll (1-100):")
        if roll_str is None:
            return None  # user canceled
        if not roll_str.isdigit():
            messagebox.showerror("Invalid Input", "Please enter a valid integer for the roll.")
            return
        roll_val = int(roll_str)
        self.log(f"Manual Roll: {roll_val} + {self.attacker_mod} = {roll_val + self.attacker_mod}")
        return roll_val

    def reset_to_setup(self):
        self.battle_frame.destroy()
        self.create_setup_frame()
