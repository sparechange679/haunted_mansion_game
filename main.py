"""
Haunted Mansion Escape Game
A text-based adventure game where the player explores a haunted mansion,
interacts with Odette the French ghost, and collects items to escape.

Author: Karen Wanga Kishindo
Date: 7/3/2025
Version: 1.4 - Fixed garden escape win condition
"""

import random
import time
import os


class Item:
    """Class to represent items that can be collected in the game."""
    
    def __init__(self, name, description, use_description=""):
        self.name = name
        self.description = description
        self.use_description = use_description
    
    def __str__(self):
        return f"{self.name}: {self.description}"


class Player:
    """Class to represent the player character."""
    
    def __init__(self, name):
        self.name = name
        self.current_room = "entrance_hall"
        self.bag = []  # List to store collected items (max 4)
        self.bag_capacity = 4
        self.has_spoken_to_odette = False
        self.game_complete = False
    
    def add_item(self, item):
        """Add an item to the player's bag if there's space."""
        if len(self.bag) < self.bag_capacity:
            self.bag.append(item)
            return True
        return False
    
    def remove_item(self, item_name):
        """Remove an item from the player's bag."""
        for item in self.bag:
            if item.name.lower() == item_name.lower():
                self.bag.remove(item)
                return item
        return None
    
    def has_item(self, item_name):
        """Check if player has a specific item."""
        return any(item.name.lower() == item_name.lower() for item in self.bag)
    
    def show_bag(self):
        """Display the contents of the player's bag."""
        if not self.bag:
            print("Your bag is empty.")
        else:
            print(f"Your bag contains ({len(self.bag)}/{self.bag_capacity}):")
            for i, item in enumerate(self.bag, 1):
                print(f"  {i}. {item}")


class Room:
    """Class to represent rooms in the mansion."""
    
    def __init__(self, name, description, items=None, connections=None):
        self.name = name
        self.description = description
        self.items = items or []
        self.connections = connections or {}
        self.visited = False
    
    def get_available_directions(self):
        """Get list of available directions from this room."""
        return list(self.connections.keys())


class HauntedMansionGame:
    """Main game class that handles the game logic and flow."""
    
    def __init__(self):
        self.player = None
        self.rooms = {}
        self.game_items = {}
        self.game_running = True
        self.command_list = []
        # Track door states - True means unlocked, False means locked
        self.door_states = {
            "pantry": False,  # Pantry door starts locked
            "garden": False   # Garden gate starts locked
        }
        self.setup_game()
    
    def clear_screen(self):
        """Clear the screen for a cleaner interface."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def setup_game(self):
        """Initialize the game world, rooms, and items."""
        # Create game items
        self.game_items = {
            "silver_key": Item("Silver Key", "An ornate silver key with intricate engravings", 
                             "Opens locked doors in the mansion"),
            "golden_key": Item("Golden Key", "A heavy golden key that gleams in the light",
                             "Opens the main door to escape"),
            "candle": Item("Candle", "A flickering candle that provides light",
                          "Illuminates dark areas"),
            "holy_water": Item("Holy Water", "A small vial of blessed water",
                              "Protects against evil spirits"),
            "portrait": Item("Portrait", "A painting of a young French woman",
                           "Odette's portrait from when she was alive"),
            "music_box": Item("Music Box", "An antique music box with a dancing figure",
                            "Plays a haunting melody"),
            "old_diary": Item("Old Diary", "Odette's personal diary from long ago",
                            "Contains Odette's memories and secrets")
        }
        
        # Create rooms
        self.rooms = {
            "entrance_hall": Room(
                "Entrance Hall",
                "A grand entrance hall with a dusty chandelier hanging overhead. "
                "The air is thick with the scent of old roses and decay. "
                "Moonlight filters through stained glass windows.",
                items=[self.game_items["candle"]],
                connections={"north": "living_room", "east": "dining_room", "west": "library", "south": "garden"}
            ),
            "living_room": Room(
                "Living Room",
                "A once-elegant living room with covered furniture and cobwebs. "
                "A cold fireplace dominates one wall. The atmosphere feels heavy.",
                items=[self.game_items["silver_key"]],
                connections={"south": "entrance_hall", "east": "kitchen", "north": "staircase"}
            ),
            "dining_room": Room(
                "Dining Room",
                "A formal dining room with a long table set for dinner, "
                "though the food has long since turned to dust. "
                "Portraits line the walls, their eyes seeming to follow you.",
                items=[self.game_items["holy_water"]],
                connections={"west": "entrance_hall", "north": "kitchen"}
            ),
            "kitchen": Room(
                "Kitchen",
                "An old-fashioned kitchen with copper pots and pans hanging from hooks. "
                "The hearth is cold and dark. Something moves in the shadows.",
                items=[self.game_items["music_box"]],
                connections={"west": "living_room", "south": "dining_room", "north": "pantry"}
            ),
            "library": Room(
                "Library",
                "A vast library with towering bookshelves reaching to the ceiling. "
                "Books are scattered on the floor, and the air smells of old paper. "
                "A reading chair sits by the window.",
                items=[self.game_items["old_diary"]],
                connections={"east": "entrance_hall", "north": "study"}
            ),
            "study": Room(
                "Study",
                "A private study with a large desk covered in papers. "
                "Candlesticks and ink bottles are scattered about. "
                "This feels like a place where important decisions were made.",
                items=[],
                connections={"south": "library", "east": "staircase"}
            ),
            "staircase": Room(
                "Grand Staircase",
                "A magnificent staircase curves upward to the second floor. "
                "The banister is carved with intricate details. "
                "You can hear faint whispers echoing from above.",
                items=[],
                connections={"south": "living_room", "west": "study", "up": "bedroom"}
            ),
            "pantry": Room(
                "Pantry",
                "A small pantry with empty shelves and broken jars. "
                "The air is stale and musty. Something glitters on the floor.",
                items=[self.game_items["golden_key"]],
                connections={"south": "kitchen"}
            ),
            "bedroom": Room(
                "Odette's Bedroom",
                "A beautifully preserved bedroom with French furniture. "
                "The room feels different from the rest of the mansion - warmer, lived-in. "
                "A spectral figure sits by the window, humming softly.",
                items=[self.game_items["portrait"]],
                connections={"down": "staircase"}
            ),
            "garden": Room(
                "Garden",
                "A moonlit garden behind the mansion. The exit gate stands before you, "
                "but it's locked with a heavy chain. Freedom is so close...",
                items=[],
                connections={"north": "entrance_hall"}
            )
        }
    
    def is_door_accessible(self, from_room, to_room):
        """Check if a door between rooms is accessible."""
        if to_room == "pantry":
            return self.door_states["pantry"]
        elif to_room == "garden":
            return self.door_states["garden"]
        return True  # All other doors are always accessible
    
    def get_door_key(self, door_name):
        """Get the key needed for a specific door."""
        if door_name == "pantry":
            return "silver_key"
        elif door_name == "garden":
            return "golden_key"
        return None
    
    def toggle_door(self, door_name):
        """Toggle the state of a door (lock/unlock)."""
        if door_name in self.door_states:
            self.door_states[door_name] = not self.door_states[door_name]
            return True
        return False
    
    def get_door_status_message(self, door_name):
        """Get a message describing the current door status."""
        if door_name not in self.door_states:
            return ""
        
        if self.door_states[door_name]:
            return f"The {door_name} is currently unlocked."
        else:
            return f"The {door_name} is currently locked."
    
    def start_game(self):
        """Start the game and get player's name."""
        self.clear_screen()
        print("=" * 60)
        print("    WELCOME TO THE HAUNTED MANSION ESCAPE GAME")
        print("=" * 60)
        print("\nYou find yourself standing before an old, imposing mansion.")
        print("The wind howls through the trees, and lightning flashes overhead.")
        print("You must enter and find a way to escape...")
        print("\nBut beware - you are not alone in this place.")
        print("Odette, a French spirit, haunts these halls.")
        print("She may help you... or she may not.")
        print("\n" + "=" * 60)
        
        player_name = input("\nEnter your character's name: ").strip()
        if not player_name:
            player_name = "Adventurer"
        
        self.player = Player(player_name)
        print(f"\nWelcome, {self.player.name}! Your adventure begins now...")
        input("\nPress Enter to continue...")
        self.game_loop()
    
    def game_loop(self):
        """Main game loop."""
        while self.game_running and not self.player.game_complete:
            self.clear_screen()
            self.display_room_info()
            
            # Check if player has won after room display
            if self.check_win_condition():
                self.end_game_victory()
                break
                
            self.show_choices()
            self.handle_player_input()
        
        if not self.player.game_complete:
            print("\nThank you for playing the Haunted Mansion Escape Game!")
    
    def display_room_info(self):
        """Display information about the current room."""
        current_room = self.rooms[self.player.current_room]
        print("\n" + "=" * 50)
        print(f"LOCATION: {current_room.name.upper()}")
        print("=" * 50)
        
        # Special handling for Garden description
        if current_room.name == "Garden":
            if self.door_states["garden"]:
                print("A moonlit garden behind the mansion. The exit gate stands open before you! Freedom is within reach...")
            else:
                print("A moonlit garden behind the mansion. The exit gate stands before you, but it's locked with a heavy chain.")
        else:
            print(current_room.description)
        
        # Check for special room events
        if current_room.name == "Odette's Bedroom" and not self.player.has_spoken_to_odette:
            self.encounter_odette()
        
        # Show door status for relevant rooms
        if self.player.current_room == "kitchen":
            print(f"\n{self.get_door_status_message('pantry')}")
        elif self.player.current_room == "entrance_hall":
            print(f"\n{self.get_door_status_message('garden')}")
        
        # Show items in the room
        if current_room.items:
            print(f"\nYou can see the following items here:")
            for item in current_room.items:
                print(f"  - {item.name}: {item.description}")
        
        current_room.visited = True
    
    def show_choices(self):
        """Display available choices to the player with numbers."""
        current_room = self.rooms[self.player.current_room]
        print("\n" + "-" * 30)
        print("WHAT WOULD YOU LIKE TO DO?")
        print("-" * 30)
        
        # Reset command list for each display
        self.command_list = []
        
        # Movement options
        directions = current_room.get_available_directions()
        if directions:
            print("Movement options:")
            for direction in directions:
                destination = self.rooms[current_room.connections[direction]]
                command = f"Go {direction} to {destination.name}"
                self.command_list.append(("move", direction, command))
                print(f"  {len(self.command_list)}. {command}")
        
        # Item options
        if current_room.items:
            print("\nItem options:")
            for item in current_room.items:
                command = f"Pick up {item.name}"
                self.command_list.append(("pickup", item.name, command))
                print(f"  {len(self.command_list)}. {command}")
        
        # General options
        print("\nGeneral options:")
        self.command_list.append(("bag", None, "Check bag"))
        print(f"  {len(self.command_list)}. Check bag")
        
        self.command_list.append(("look", None, "Look around"))
        print(f"  {len(self.command_list)}. Look around")
        
        self.command_list.append(("use", None, "Use item"))
        print(f"  {len(self.command_list)}. Use item")
        
        self.command_list.append(("remove", None, "Remove item"))
        print(f"  {len(self.command_list)}. Remove item")
        
        self.command_list.append(("quit", None, "Quit game"))
        print(f"  {len(self.command_list)}. Quit game")
    
    def handle_player_input(self):
        """Handle player input using numbered commands."""
        try:
            choice = input("\nEnter the number of your choice: ").strip()
            if not choice:
                print("Please enter a valid number.")
                input("\nPress Enter to continue...")
                return
            
            choice_index = int(choice) - 1
            
            if choice_index < 0 or choice_index >= len(self.command_list):
                print("Invalid choice number. Please try again.")
                input("\nPress Enter to continue...")
                return
            
            action_type, data, command = self.command_list[choice_index]
            
            if action_type == "move":
                self.move_player(data)
            elif action_type == "pickup":
                self.pick_up_item(data)
                input("\nPress Enter to continue...")
            elif action_type == "bag":
                self.player.show_bag()
                input("\nPress Enter to continue...")
            elif action_type == "look":
                self.look_around()
                input("\nPress Enter to continue...")
            elif action_type == "use":
                self.use_item_menu()
            elif action_type == "remove":
                self.remove_item_from_bag()
            elif action_type == "quit":
                self.game_running = False
        except ValueError:
            print("Please enter a valid number.")
            input("\nPress Enter to continue...")
    
    def use_item_menu(self):
        """Display a menu for using items."""
        if not self.player.bag:
            print("Your bag is empty.")
            input("\nPress Enter to continue...")
            return
        
        print("\nItems in your bag:")
        for i, item in enumerate(self.player.bag, 1):
            print(f"  {i}. {item.name}")
        
        try:
            choice = input("\nEnter the number of the item to use (or '0' to cancel): ").strip()
            if choice == "0":
                return
            
            choice_index = int(choice) - 1
            
            if choice_index < 0 or choice_index >= len(self.player.bag):
                print("Invalid item number.")
                input("\nPress Enter to continue...")
                return
            
            item = self.player.bag[choice_index]
            self.use_item(item.name)
        except ValueError:
            print("Please enter a valid number.")
            input("\nPress Enter to continue...")
    
    def move_player(self, direction):
        """Move the player to a new room."""
        current_room = self.rooms[self.player.current_room]
        
        if direction in current_room.connections:
            new_room_name = current_room.connections[direction]
            
            # Check if the door is accessible
            if not self.is_door_accessible(self.player.current_room, new_room_name):
                if new_room_name == "pantry":
                    print("The pantry door is locked. You need to use the silver key to unlock it.")
                elif new_room_name == "garden":
                    print("The garden gate is locked with a heavy chain. You need to use the golden key to unlock it.")
                input("\nPress Enter to continue...")
                return
            
            self.player.current_room = new_room_name
            print(f"\nYou move {direction}...")
            time.sleep(1)
        else:
            print("You can't go that way.")
            input("\nPress Enter to continue...")
    
    def pick_up_item(self, item_name):
        """Pick up an item from the current room."""
        current_room = self.rooms[self.player.current_room]
        
        for item in current_room.items:
            if item.name == item_name:
                if self.player.add_item(item):
                    current_room.items.remove(item)
                    print(f"You picked up the {item.name}.")
                else:
                    print(f"Your bag is full! (Maximum {self.player.bag_capacity} items)")
                    print("You need to remove an item first.")
                return
        
        print("There's no such item here.")
    
    def use_item(self, item_name):
        """Use an item from the player's bag with specific interactions."""
        item = None
        for bag_item in self.player.bag:
            if bag_item.name.lower() == item_name.lower():
                item = bag_item
                break
        
        if not item:
            print("You don't have that item.")
            return
        
        current_room = self.rooms[self.player.current_room]
        print(f"\nYou use the {item.name}...")
        
        # Door toggle functionality
        if item.name.lower() == "silver key":
            if self.player.current_room == "kitchen":
                current_state = self.door_states["pantry"]
                if self.toggle_door("pantry"):
                    if current_state:  # Was unlocked, now locked
                        print("The silver key turns in the pantry door lock.")
                        print("You hear a heavy click as the door locks.")
                        print("The pantry is now locked!")
                    else:  # Was locked, now unlocked
                        print("The silver key fits perfectly in the pantry door lock.")
                        print("You hear a satisfying click as the lock turns.")
                        print("The pantry is now unlocked!")
                else:
                    print("The key doesn't seem to work on anything here.")
            else:
                print("The silver key doesn't seem to do anything useful here.")
                print("Try using it near the pantry door.")
        
        elif item.name.lower() == "golden key":
            if self.player.current_room == "entrance_hall":
                current_state = self.door_states["garden"]
                if self.toggle_door("garden"):
                    if current_state:  # Was unlocked, now locked
                        print("The golden key turns in the garden gate lock.")
                        print("The heavy chain falls back into place with a clang.")
                        print("The garden gate is now locked!")
                    else:  # Was locked, now unlocked
                        print("The golden key fits the heavy chain lock on the garden gate.")
                        print("With a rusty creak, the chain falls away.")
                        print("The garden gate is now unlocked!")
                else:
                    print("The key doesn't seem to work on anything here.")
            else:
                print("The golden key doesn't seem to do anything useful here.")
                print("Try using it near the garden gate.")
        
        # Other item usage logic
        elif item.name.lower() == "portrait" and self.player.current_room == "Odette's Bedroom":
            print("You show Odette her portrait from when she was alive.")
            print("Odette: 'Mon portrait! You found it!'")
            print("The ghost seems pleased and fades away with a smile.")
        elif item.name.lower() == "holy water":
            print("You sprinkle the holy water around you.")
            print("A faint hissing sound comes from the shadows as they retreat.")
            print("You feel safer for now.")
        elif item.name.lower() == "candle":
            print("The candle's flickering light pushes back the darkness.")
            print("The shadows seem less threatening now.")
        else:
            print(f"The {item.name} doesn't seem to do anything useful here.")
        
        input("\nPress Enter to continue...")
    
    def remove_item_from_bag(self):
        """Allow player to remove an item from their bag."""
        if not self.player.bag:
            print("Your bag is already empty.")
            input("\nPress Enter to continue...")
            return
        
        print("\nCurrent bag contents:")
        for i, item in enumerate(self.player.bag, 1):
            print(f"  {i}. {item.name}")
        
        try:
            choice = input("\nEnter the number of the item to remove (or '0' to cancel): ").strip()
            if choice == "0":
                return
            
            choice_index = int(choice) - 1
            
            if choice_index < 0 or choice_index >= len(self.player.bag):
                print("Invalid item number.")
                input("\nPress Enter to continue...")
                return
            
            removed_item = self.player.bag[choice_index]
            self.player.bag.remove(removed_item)
            current_room = self.rooms[self.player.current_room]
            current_room.items.append(removed_item)
            print(f"You removed the {removed_item.name} from your bag and left it here.")
            input("\nPress Enter to continue...")
        except ValueError:
            print("Please enter a valid number.")
            input("\nPress Enter to continue...")
    
    def look_around(self):
        """Provide additional details about the current room."""
        current_room = self.rooms[self.player.current_room]
        print(f"\nYou take a closer look around the {current_room.name}...")
        
        # Room-specific details
        if current_room.name == "Odette's Bedroom":
            print("The room is filled with the scent of roses. You sense a presence watching you.")
        elif current_room.name == "kitchen":
            print("You hear the sound of pots and pans rattling, though no one is there.")
            print(f"The pantry door to the north is {('unlocked' if self.door_states['pantry'] else 'locked')}.")
        elif current_room.name == "entrance_hall":
            print("The grand entrance feels both welcoming and ominous.")
            print(f"The garden gate to the south is {('unlocked' if self.door_states['garden'] else 'locked')}.")
        elif current_room.name == "library":
            print("The books seem to whisper secrets as you pass by them.")
        else:
            print("The shadows seem to move on their own, and you feel a chill in the air.")
    
    def encounter_odette(self):
        """Special encounter with Odette the French ghost."""
        print("\n" + "*" * 50)
        print("SUPERNATURAL ENCOUNTER")
        print("*" * 50)
        print("A translucent figure materializes before you...")
        print("It's a young woman in an elegant 18th-century dress.")
        print("She speaks with a soft French accent:")
        print("\nOdette: 'Bonjour, mon ami... You have entered my domain.'")
        print("Odette: 'I have been waiting so long for someone to find me.'")
        print("Odette: 'If you wish to escape, you must help me first.'")
        print("Odette: 'Find my belongings scattered throughout the mansion.'")
        print("Odette: 'Bring them to me, and I will give you the key to freedom.'")
        print("\nShe points to a portrait on the dresser.")
        print("Odette: 'Start with my portrait, but you'll need more than that...'")
        print("\nThe ghost fades away, leaving you alone with your thoughts.")
        print("*" * 50)
        
        self.player.has_spoken_to_odette = True
        input("\nPress Enter to continue...")
    
    def check_win_condition(self):
        """Check if the player has won the game."""
        if (self.player.current_room == "garden" and 
            self.door_states["garden"] and  # Garden gate must be unlocked
            self.player.has_spoken_to_odette):  # Must have spoken to Odette
            return True
        return False
    
    def end_game_victory(self):
        """Handle the victory condition."""
        self.clear_screen()
        print("\n" + "=" * 60)
        print("CONGRATULATIONS! YOU HAVE ESCAPED THE HAUNTED MANSION!")
        print("=" * 60)
        print("\nWith the garden gate unlocked,")
        print("you step toward freedom...")
        print("\nOdette appears one last time...")
        print("\nOdette: 'Merci beaucoup, mon ami. You have helped me find peace.'")
        print("Odette: 'You used the keys wisely and proved your worth.'")
        print("Odette: 'Now go, you have earned your freedom.'")
        print("\nThe ghost smiles and fades away into the moonlight.")
        print("You step through the unlocked gate and into the world beyond.")
        print(f"\nWell done, {self.player.name}! You successfully escaped the haunted mansion!")
        print("=" * 60)
        
        self.player.game_complete = True
        self.game_running = False
        input("\nPress Enter to exit...")


def main():
    """Main function to start the game."""
    game = HauntedMansionGame()
    game.start_game()


if __name__ == "__main__":
    main()