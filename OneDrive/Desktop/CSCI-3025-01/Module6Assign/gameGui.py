import tkinter as tk
import random
from gameLogic import gameLogic
from player import Gorn, Tribble


class gameGui:

    def __init__(self, root, size=10):
        self.root = root
        self.size = size
        self.cell_size = 80
        self.logic = gameLogic(size, cell_size=self.cell_size)       # Tying the game logic to self.logic,so I can use it in GUI

    
        self.grid_frame = tk.Frame(root, bg="white", bd=2)               #Creating the grid window
        self.grid_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.log_display = tk.Label(
            root,
            text=f"Welcome to the game, {self.logic.player.name}!",
            font=("Arial", 11),
            bg="#f0f0f0",
            fg="#333333",
            bd=1,
            relief="sunken",
            height=4,
            anchor="nw",
            justify="left",
            padx=10,
            pady=5,
            wraplength=420,
        )
        self.log_display.pack(fill="x", padx=10, pady=(0, 5))

        # Inventory display
        self.inventory_label = tk.Label(
            root,
            text="Inventory: (empty)",
            font=("Arial", 10),
            bg="#e8e8e8",
            anchor="w",
            padx=10,
            pady=3,
        )
        self.inventory_label.pack(fill="x", padx=10, pady=(0, 5))

        # D-pad controls
        self.control_frame = tk.Frame(root, pady=5)
        self.control_frame.pack(fill="x")

        self.widget_grid = [[None for _ in range(self.logic.cols)] for _ in range(self.logic.rows)]

        self.create_grid()
        self.create_controls()
        self.full_render()
        self.update_inventory()

    def create_grid(self):                  # Creating the grid, and populating it with cells.
        for x in range(self.logic.cols):
            self.grid_frame.columnconfigure(x, weight=1, minsize=self.cell_size, uniform="square")
        for y in range(self.logic.rows):
            self.grid_frame.rowconfigure(y, weight=1, minsize=self.cell_size, uniform="square")

        for y in range(self.logic.rows):
            for x in range(self.logic.cols):
                lbl = tk.Label(self.grid_frame, bg="white", relief="raised", bd=1)
                lbl.grid(row=y, column=x, sticky="nsew", padx=1, pady=1)
                self.widget_grid[y][x] = lbl

    def create_controls(self):              
        """Create buttons for North, South, East, West controls"""
        for i in range(3):
            self.control_frame.columnconfigure(i, weight=1)
            self.control_frame.rowconfigure(i, weight=1)

        btn_style = {
            "width": 4,
            "height": 2,
            "font": ("Arial", 10, "bold"),
            "bg": "lightgray",
            "activebackground": "#d0d0d0",
        }

        tk.Button(self.control_frame, text="N", command=lambda: self.move(0, -1), **btn_style).grid(row=0, column=1)
        tk.Button(self.control_frame, text="W", command=lambda: self.move(-1, 0), **btn_style).grid(row=1, column=0)
        tk.Button(self.control_frame, text="E", command=lambda: self.move(1, 0), **btn_style).grid(row=1, column=2)
        tk.Button(self.control_frame, text="S", command=lambda: self.move(0, 1), **btn_style).grid(row=2, column=1)

        # Keyboard bindings - can also use directional keys on keyboard to move around
        self.root.bind("<Up>",    lambda e: self.move(0, -1))
        self.root.bind("<Down>",  lambda e: self.move(0, 1))
        self.root.bind("<Left>",  lambda e: self.move(-1, 0))
        self.root.bind("<Right>", lambda e: self.move(1, 0))

    def clear_cell(self, y, x):
        """setter to return cell to empty"""
        cell = self.widget_grid[y][x]
        cell.config(image="", text="", bg="white")
        cell.image = None

    def render_entity(self, y, x, entity):
        """Adds the image of the object to the GUI cell."""
        if entity is None or not hasattr(entity, "image") or entity.image is None:
            return
        cell = self.widget_grid[y][x]
        cell.config(image=entity.image, bg="white")
        cell.image = entity.image  # keep a reference so Tk doesn't garbage-collect it

    def full_render(self):
        """Used to redraw the entire gamegrid from the current gridState"""
        for y in range(self.logic.rows):
            for x in range(self.logic.cols):
                self.clear_cell(y, x)
                cell_contents = self.logic.gridState[y][x]

                player = next((e for e in cell_contents if e is self.logic.player), None)
                exit_obj = next((e for e in cell_contents if type(e).__name__ == "Exit"), None)

                if player:
                    self.render_entity(y, x, player)
                elif exit_obj:
                    self.render_entity(y, x, exit_obj)

    def update_inventory(self):
        """setter to add an object to player inventory"""
        items = self.logic.player._inventory
        if items:
            text = self.logic.player
            #text = "Inventory: " + ", ".join(str(i) for i in items)
            #debugging for str print
            #print(self.logic.player)

        else:
            text = "Inventory: (empty)"
        self.inventory_label.config(text=text)

    def log_message(self, text):
        """Pass text to this function, to display it in the GUI status area"""
        self.log_display.config(text=text)

    def show_encounter_popup(self, enemy):
        """All of the code for the battle sequence, gui and logic lives here."""

        popup = tk.Toplevel(self.root)
        popup.title("Encounter!")
        popup.resizable(False, False)
        popup.transient(self.root)
        popup.grab_set()

        # Center over main window
        popup.update_idletasks()
        main_x = self.root.winfo_rootx()
        main_y = self.root.winfo_rooty()
        main_w = self.root.winfo_width()
        main_h = self.root.winfo_height()
        pop_w, pop_h = 440, 360
        x = main_x + (main_w - pop_w) // 2 -10  #This is a bit of a hack to restore centering
        #y = main_y + (main_h - pop_h) // 2 
        y = main_y + 20                     #Move the popup upward, so it doesn't block the message log area
        popup.geometry(f"{pop_w}x{pop_h}+{x}+{y}")

        player = self.logic.player

        # Title
        title = tk.Label(
            popup,
            text=f"You are battling with a {enemy.name}!",
            font=("Arial", 14, "bold"),
            pady=8,
        )
        title.pack()

        images_frame = tk.Frame(popup)
        images_frame.pack(pady=6)

        # Left side, Adventurer
        left_frame = tk.Frame(images_frame)
        left_frame.pack(side="left", padx=20)
        adv_img = tk.Label(left_frame, image=player.image)
        adv_img.image = player.image
        adv_img.pack()
        tk.Label(left_frame, text=player.name, font=("Arial", 10)).pack()

        player_hp_label = tk.Label(
            left_frame,
            text=f"HP: {player.health}",
            font=("Arial", 10, "bold"),
            fg="#27ae60",
        )
        player_hp_label.pack()

    
        tk.Label(images_frame, text="VS", font=("Arial", 16, "bold"), padx=10).pack(side="left")

        # Right side, Opponent class here
        right_frame = tk.Frame(images_frame)
        right_frame.pack(side="left", padx=20)
        enemy_img = tk.Label(right_frame, image=enemy.image)
        enemy_img.image = enemy.image
        enemy_img.pack()
        tk.Label(right_frame, text=enemy.name, font=("Arial", 10)).pack()

        enemy_hp_label = tk.Label(
            right_frame,
            text=f"HP: {enemy.health}",
            font=("Arial", 10, "bold"),
            fg="#c0392b",
        )
        enemy_hp_label.pack()

        # Guarding item info
        if enemy.guardingItem:
            tk.Label(
                popup,
                text=f"Guarding: {enemy.guardingItem}",
                font=("Arial", 10, "italic"),
                fg="#555555",
            ).pack()

        # Combat log inside the popup
        combat_log = tk.Label(
            popup,
            text="Choose Attack!",
            font=("Arial", 10),
            fg="#333333",
            wraplength=400,
            justify="left",
            height=3,
        )
        combat_log.pack(pady=6)

        btn_frame = tk.Frame(popup)
        btn_frame.pack(pady=8)

        def refresh_hp():
            player_hp_label.config(text=f"HP: {player.health}")
            enemy_hp_label.config(text=f"HP: {enemy.health}")
            if player.health <= 30:
                player_hp_label.config(fg="#c0392b")
            if enemy.health <= 30:
                enemy_hp_label.config(fg="#e67e22")

        def end_combat(message):
            """Disable button, show final message, then close after a short delay."""
            attack_btn.config(state="disabled")
            combat_log.config(text=message)
            self.log_message(message)
            popup.after(1200, popup.destroy)

        def check_end():
            """Return True if combat is over."""
            if enemy.health <= 0:
                enemy.defeated = True

                # Take the enemy's item and add it to inventory
                if enemy.guardingItem:
                    player.add_item(enemy.guardingItem)
                    item_msg = f"You took: {enemy.guardingItem}"
                    enemy.guardingItem = None
                else:
                    item_msg = "It had nothing."        #This isn't likely to be used. All enemies should have at least one item.

                end_combat(f"You defeated a {enemy.name}!\n{item_msg}")
                self.update_inventory()
                return True

            if player.health <= 0:
                player.alive = False
                self.logic.game_over = True
                end_combat(f"You were defeated by a {enemy.name}...\nYour quest has ended!\nGame over.")
                return True
            return False

       # def enemy_strike():
       #     """Enemy attack"""
       #     # 30% likelihood that the enemy will miss. 
       #     if random.random() < 0.30:
       #         return 0, f"{enemy.name} misses!"#
       #
       #     dmg = enemy.damage
       #     return dmg, f"The {enemy.name} hits you for {dmg} damage!"

        def on_attack():
            #Player attacks first
            player.attack(enemy)
            msg = f"You hit the {enemy.name} for {player.damage} damage!"

            refresh_hp()
            if check_end():
                return

            #Enemy attacks Second.
            dmg, enemy_msg = enemy.enemy_attack(player)
            #if dmg > 0:
            #    player.health -= dmg
            #    player.health = max(player.health, 0)
            msg += f"\n{enemy_msg}"

            refresh_hp()
            combat_log.config(text=msg)
            check_end()

        attack_btn = tk.Button(
            btn_frame,
            text="Attack",
            width=12,
            font=("Arial", 10, "bold"),
            bg="#c0392b",
            fg="white",
            command=on_attack,
        )
        attack_btn.pack(anchor="center")

        # This is needed to hold until the window closes
        self.root.wait_window(popup)

    def move(self, dx, dy):
        """Calls the try_move, and refreshes the grid. Call popup if Enemy is here! """
        if self.logic.game_over:
            return

        result = self.logic.try_move(dx, dy)

        if not result["ok"]:
            self.log_message(result["message"])
            return

        # Refresh the whole grid (player + exit only)
        self.full_render()
        self.update_inventory()
        self.log_message(result["message"])

        # If an enemy was encountered, show the popup
        if result.get("enemy") is not None:
            self.show_encounter_popup(result["enemy"])
