import random
import os
from PIL import Image, ImageTk
from player import Adventurer, Gorn, Tribble


class gameLogic:

    def __init__(self, size, cell_size=80):
        self.size = size
        self.rows = int(size / 2)
        self.cols = int(size / 2)
        self.cell_size = cell_size
        self.Xpos = self.cols // 2    # The // is used for floor division, round number to the nearest whole integer
        self.Ypos = self.rows // 2    # Trying this out as an alternative to the cast to int as used above.  

        #Instance of our player in the game
        self.player = Adventurer(name="James T. Kirk", inventory=[], cell_size=cell_size)
        #This creates the 2d list for the game state
        self.gridState = [[[] for _ in range(self.cols)] for _ in range(self.rows)]
        self.gridState[self.Ypos][self.Xpos].append(self.player)
        corners = [
            (0, 0),
            (0, self.cols - 1),
            (self.rows - 1, 0),
            (self.rows - 1, self.cols - 1),
        ]
        
        exit_y, exit_x = random.choice(corners)
        
        #I chose to make the exit an object, of Exit class. Instatiate exit below.
        self.map_exit = Exit(isLocked=True, x=exit_x, y=exit_y, cell_size=cell_size)
        self.gridState[self.map_exit.location_y][self.map_exit.location_x].append(self.map_exit)

        self.placeHazards()
        self.game_over = False
        self.won = False

    def placeHazards(self):
        """Inner and outer loop used here to take the list of enemies and pop them out one by one into grid cells."""
        enemies = self.generateEnemies()
        for y in range(self.rows):
            for x in range(self.cols):
                cell = self.gridState[y][x]
                if self.player in cell or self.map_exit in cell:
                    continue
                if enemies:
                    enemy = enemies.pop()
                    if enemy != "empty":
                        cell.append(enemy)

    def generateEnemies(self):
        """Create objects of Gorn and Tribble, assign each an item. Return the list of objects."""
        enemy_items = [
            "a Key",
            "a Phaser",
            "Romulan Ale",
            "a Communicator",
            "Self-Sealing Stem Bolts",
            "Gold-Pressed Latinum",
            "a Tricorder",
            "Dilithium Crystals",
            "Isolinear Chips",
            "a Power Cell",
        ]
        random.shuffle(enemy_items)

        enemies = []
        for i in range(5):
            item = enemy_items.pop() if enemy_items else None
            enemies.append(Gorn(name=f"Gorn", guardingItem=item, cell_size=self.cell_size))
        for i in range(5):
            item = enemy_items.pop() if enemy_items else None
            enemies.append(Tribble(name=f"Tribble", guardingItem=item, cell_size=self.cell_size))

        total_cells = self.rows * self.cols             # We want place "empty" in cells that don't get an enemy.
        empty_needed = total_cells - len(enemies) - 2   # the number of available spaces are total -2, for the exit and player
        enemies += ["empty"] * max(0, empty_needed)
        random.shuffle(enemies)
        return enemies

    def try_move(self, dx, dy):
        """Moving player around the visible grid. Also contains logic for encountering other players, and the exit"""
        new_x = self.Xpos + dx
        new_y = self.Ypos + dy

        if not (0 <= new_x < self.cols and 0 <= new_y < self.rows):
            return {"ok": False, "message": "There is a wall here, it blocks your path."}

        # Remove player from old cell
        old_cell = self.gridState[self.Ypos][self.Xpos]
        if self.player in old_cell:
            old_cell.remove(self.player)

        # Update position
        self.Xpos = new_x
        self.Ypos = new_y
        new_cell = self.gridState[self.Ypos][self.Xpos]
        new_cell.append(self.player)

        result = {
            "ok": True,
            "x": new_x,
            "y": new_y,
            "found": "nothing",
            "item": None,
            "enemy": None,
            "at_exit": False,
            "message": "",
        }

        for entity in list(new_cell):
            if isinstance(entity, (Gorn, Tribble)) and not entity.defeated:
                result["found"] = entity.name
                result["enemy"] = entity
                result["item"] = entity.guardingItem


                if entity.guardingItem:
                    result["message"] = (
                        f"You are faced with a {entity.name}!\n"
                        f"You can see that it is Guarding a {entity.guardingItem}."
                    )
                else:
                    result["message"] = f"You are faced with a {entity.name}."

            elif isinstance(entity, Exit):
                result["at_exit"] = True
                if entity.isLocked:
                    if self.player.has_item("Key"):
                        entity.unlock()
                        self.won = True
                        self.game_over = True
                        result["message"] = (
                            "You use the key to unlock the door, and walk through.\n"
                            "You have won! Your quest is over."
                        )
                    else:
                        result["message"] = (
                            "You reach the exit door, but it is locked.\n"
                            "You need a Key to open it."
                        )

        if not result["message"]:
            result["message"] = f"Moved to ({new_x}, {new_y}). You can see there is nothing here."

        return result


class Exit:
    """I felt it would be easier to deal with the exit as an object. It does not inherit from other classes."""
    def __init__(self, isLocked, x, y, cell_size=80):
        self.isLocked = isLocked
        self.location_x = x
        self.location_y = y
        self.image = self.load_image("Module6assign1BLUM/assets/exitdoor.jpg", cell_size, "sienna")

    def isDoorLocked(self):
        """getter to check if door is locked."""
        return self.isLocked

    def unlock(self):
        """setter function to unlock the door"""
        self.isLocked = False

    def load_image(self, image_path, cell_size=80, fallback_color="crimson"):
        """Used only to load the images for players and exit"""
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