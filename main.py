import tkinter as tk
from ftl_tabletop.gui.battle_gui import BattleGUI

def main():
    root = tk.Tk()
    root.title("FTL Tabletop Combat System")  # If you want a window title here
    print("Starting FTL Tabletop Combat System...")
    app = BattleGUI(root)
    print("GUI initialized.")
    root.mainloop()

if __name__ == "__main__":
    main()
