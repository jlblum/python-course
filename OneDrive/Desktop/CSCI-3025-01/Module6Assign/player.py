from PIL import Image, ImageTk
import os
import random

class Player:
    """Player is the base class others will inherit from."""
    def __init__(self, name):
        self.name = name
        self.image = None
        self.health = 100
        self.damage = 20
        self.alive = True

    def attack(self, target):
        """This serves as the attack function for all the classes of Player"""
        target.health -= self.damage
        target.health = max(target.health, 0)
       # print(f"{self.name} dealt {self.damage} damage to {target.name}")
       # Leave above for console debugging purposes.

    def enemy_attack(self,target):
        """Enemy attack"""
        # 30% likelihood that the enemy will miss. 
        #print("Calling the player class enemy attack method")
        if random.random() < 0.30:
            return 0, f"{self.name} misses!"#
           
        target.health -= self.damage
        target.health = max(target.health, 0)
        return self.damage, f"The {self.name} hits you for {self.damage} damage!"

    def load_image(self, image_path, cell_size=80, fallback_color="crimson"):
        """Load images, with a fallback if can't load. This is here until I figure out how to call it from somewhere else."""
        render_dim = int(cell_size - 4)
        try:
            raw_img = Image.open(image_path)
            resized_img = raw_img.resize((render_dim, render_dim), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(resized_img)
        except (FileNotFoundError, OSError) as error:
            print(f"Failed to load '{image_path}': {error}")
            print(f" -> Creating procedural {fallback_color} placeholder instead...")
            fallback_img = Image.new("RGB", (render_dim, render_dim), color=fallback_color)
            return ImageTk.PhotoImage(fallback_img)


class Opponent(Player):
    """Opponent class inherits from the Player class"""
    def __init__(self, name, guardingItem):
        super().__init__(name)
        self.guardingItem = guardingItem
        self.defeated = False


class Adventurer(Player):
    """Adventurer class inherits from the Player class"""
    def __init__(self, name: str, inventory: list = None, cell_size=80):
        super().__init__(name)
        self._inventory = inventory if inventory is not None else []
        self.damage = 20  # Adventurer damage
        self.image = self.load_image("Module6assign1BLUM/assets/adventurer.jpg", cell_size, "dodgerblue")

    def has_item(self, item_name: str) -> bool:
        """getter to check if the player has an item in inventory"""
        return any(item_name.lower() in str(i).lower() for i in self._inventory)

    def add_item(self, item):
        """setter to add an item to the player inventory"""
        if item and item not in self._inventory:
            self._inventory.append(item)


class Gorn(Opponent):
    """Gorn class inherits from Oppenent."""
    def __init__(self, name, guardingItem, cell_size=80):
        super().__init__(name, guardingItem)
        self.damage = 15  # Gorn damage
        self.image = self.load_image("Module6assign1BLUM/assets/gorn.jpg", cell_size, "darkgreen")


class Tribble(Opponent):
    """Tribble class inherits from Opponent."""
    def __init__(self, name, guardingItem, cell_size=80):
        super().__init__(name, guardingItem)
        self.damage = 10  # Tribble damage
        self.health = 70  # Override initial health, would otherwise be 100 inherited from Player
        self.image = self.load_image("Module6assign1BLUM/assets/tribble.jpg", cell_size, "saddlebrown")