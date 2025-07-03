# Haunted Mansion Adventure Game
# By Karen Kishindo
# Featuring Odette, the French ghost
# 
# This code implements a simple text-based adventure game where the player explores a haunted
# mansion, interacts with a ghost named Odette, and collects items to escape.
# The game features a bag system, allowing the player to pick up and drop items
#
import os

# This function takes the player's input and executes the corresponding action.
def clear():
    os.system("cls")

class Player:
    def __init__(self, name):
        self.name = name
        self.position = 'Foyer'
        self.bag = []

    def add_item(self, item):
        if len(self.bag) < 4:
            self.bag.append(item)
            clear()
            print(f"You picked up the {item}.")
        else:
            clear()
            print("Your bag is full! You must drop something before picking up another item.")

    def remove_item(self, item):
        if item in self.bag:
            self.bag.remove(item)
            clear()
            print(f"You dropped the {item}.")
        else:
            clear()
            print(f"You don't have {item} in your bag.")

    def show_bag(self):
        if self.bag:
            clear()
            print("Items in your bag:", ', '.join(self.bag))
        else:
            clear()
            print(f"Your bag is empty.")

# Define the mansion map
mansion = {
    'Foyer': {
        'desc': "You are in the grand foyer. A chilly wind blows. Doors lead north, east, and west.",
        'moves': {'north': 'Library', 'east': 'Dining Room', 'west': 'Study'},
        'item': None,
        'person': None
    },
    'Library': {
        'desc': "Rows of dusty books. A silver key glimmers on a table. Doors south and east.",
        'moves': {'south': 'Foyer', 'east': 'Gallery'},
        'item': 'Silver key',
        'person': None
    },
    'Gallery': {
        'desc': "Portraits stare at you. There's a candle here. Doors west and south.",
        'moves': {'west': 'Library', 'south': 'Dining Room'},
        'item': 'Candle',
        'person': None
    },
    'Dining Room': {
        'desc': "A long table set for a feast. A locked door to the north, doors west and north.",
        'moves': {'west': 'Foyer', 'north': 'Gallery', 'east': 'Study'},
        'item': None,
        'person': None
    },
    'Study': {
        'desc': "A cozy study. An old map is on the desk. Doors east and north.",
        'moves': {'east': 'Foyer', 'north': 'Conservatory'},
        'item': 'Old map',
        'person': None
    },
    'Conservatory': {
        'desc': "Plants everywhere. A rusty key is on a bench. Doors south and east.",
        'moves': {'south': 'Study', 'east': 'Ballroom'},
        'item': 'Rusty key',
        'person': None
    },
    'Ballroom': {
        'desc': "A grand ballroom. A music box sits on a pedestal. Doors west and south.",
        'moves': {'west': 'Conservatory', 'south': 'Kitchen'},
        'item': 'Music box',
        'person': None
    },
    'Kitchen': {
        'desc': "The kitchen smells of old bread. A loaf is here. Doors north and east.",
        'moves': {'north': 'Ballroom', 'east': 'Cellar'},
        'item': 'Loaf of bread',
        'person': None
    },
    'Cellar': {
        'desc': "It's dark. You hear a whisper: 'Bonjour... I am Odette.' Odette the ghost floats here.",
        'moves': {'west': 'Kitchen', 'up': 'Secret Room'},
        'item': None,
        'person': 'Odette'
    },
    'Secret Room': {
        'desc': "A hidden chamber filled with treasures. You see the exit door here!",
        'moves': {'down': 'Cellar'},
        'item': 'Treasure',
        'person': None
    }
}

# List of all positions for win condition
final_room = 'Secret Room'

def interact_with_odette(player):
    print("\nOdette, the French ghost, smiles sadly.")
    print("'Bonjour, cher ami. I have been trapped here for centuries.'")
    if 'Music box' in player.bag:
        print("Odette notices the music box in your bag.")
        print("'Mon dieu! That music box... It belonged to me. May I have it?'")
        answer = input("Give Odette the music box? (yes/no): ").strip().lower()
        if answer == 'yes':
            player.remove_item('Music Box')
            print("Odette: 'Merci beaucoup! The secret passage opens for you.'")
            # Allow access to Secret Room
            mansion['Cellar']['moves']['up'] = 'Secret Room'
        else:
            print("Odette looks disappointed. 'Maybe another time...'")
    else:
        print("Odette: 'If only I could hear my music box again...'")

def main():
    print("Welcome to the Haunted Mansion Adventure!")
    name = input("Enter your character's name: ")
    player = Player(name)
    clear()
    print(f"\nGood luck, {player.name}!\n")

    while True:
        room = mansion[player.position]
        print(f"\n== {player.position} ==")
        print(room['desc'])
        if room['item']:
            print(f"You see a {room['item']} here.")
        if room['person'] == 'Odette':
            interact_with_odette(player)
        print("\nAvailable moves:", ', '.join(room['moves'].keys()))
        print("Type 'bag' to check your bag, 'pickup' to pick up an item, 'drop' to drop an item, or 'quit' to exit.")
        choice = input("What do you want to do? ").strip().lower()
        clear()

        if choice in room['moves']:
            player.position = room['moves'][choice]
            if player.position == final_room:
                print(f"\nCongratulations {player.name}! You've found the secret treasure and escaped the mansion!")
                break
        elif choice == 'pickup':
            if room['item']:
                player.add_item(room['item'])
                room['item'] = None
            else:
                clear()
                print(f"I am sorry {player.name}, but there is nothing to pick up here.")
        elif choice == 'drop':
            player.show_bag()
            item = input("Which item do you want to drop? ").strip()
            drop_item = item.capitalize()
            player.remove_item(drop_item)
        elif choice == 'bag':
            player.show_bag()
        elif choice == 'quit':
            print(f"Thanks for playing {player.name}!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()