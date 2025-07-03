# Haunted Mansion Escape Game

## Project Overview

This is a text-based adventure game developed in Python as part of the Introduction to Programming with Python assessment. The game features a single-player exploration experience where the player navigates through a haunted mansion, collects items, and interacts with Odette, a French ghost, to ultimately escape.

## Table of Contents

1. [Game Requirements Analysis](#game-requirements-analysis)
2. [Success Criteria](#success-criteria)
3. [Game Design and Story](#game-design-and-story)
4. [Technical Implementation](#technical-implementation)
5. [Data Structures](#data-structures)
6. [Object-Oriented Design](#object-oriented-design)
7. [Module Structure](#module-structure)
8. [Installation Guide](#installation-guide)
9. [User Guide](#user-guide)
10. [Testing Strategy](#testing-strategy)
11. [Code Documentation](#code-documentation)

---

## Game Requirements Analysis

### Required Outcomes

Based on the assignment specification, the game must fulfill the following requirements:

1. **Single Player Game**: Allow user to enter character name ✓
2. **Inventory System**: Player has a bag to store up to 4 items ✓
3. **Interactive Interface**: Output current position and available choices ✓
4. **User Input Handling**: Accept and process player choices ✓
5. **Game Progression**: Player interacts until reaching end point ✓
6. **Modular Design**: Use modular approach for navigation ✓
7. **Class Implementation**: Use at least one class ✓
8. **World Structure**: Minimum 10 different positions ✓
9. **Item Collection**: Minimum 5 different collectible items ✓
10. **Movement System**: Allow movement between different game areas ✓

---

## Success Criteria

The following success criteria were established to evaluate the completed game:

### Functional Requirements
- [x] Player can create a character with a custom name
- [x] Game displays current location and available actions clearly
- [x] Player can navigate between at least 10 different rooms
- [x] Inventory system correctly manages up to 4 items
- [x] Player can collect at least 5 different items
- [x] Game provides meaningful choices and consequences
- [x] Player can complete the game by reaching the escape condition
- [x] Game handles invalid input gracefully

### Technical Requirements
- [x] Code uses object-oriented programming principles
- [x] Game implements proper modular design
- [x] Data structures are appropriate for their purpose
- [x] Code includes comprehensive error handling
- [x] Interface is clean and non-scrolling
- [x] Game state is properly maintained throughout

### User Experience Requirements
- [x] Game provides clear instructions and feedback
- [x] Story is engaging and atmospheric
- [x] Commands are intuitive and easy to understand
- [x] Game progression feels natural and rewarding

---

## Game Design and Story

### Story Concept

The player finds themselves trapped in a haunted mansion owned by Odette, a French ghost from the 18th century. To escape, the player must:

1. Explore the mansion's 10 rooms
2. Collect Odette's personal belongings
3. Interact with Odette to understand her story
4. Find the golden key to unlock the garden gate
5. Successfully escape the mansion

### Game World Layout

```
                    [Bedroom]
                        |
[Study] — [Staircase] — [Living Room] — [Kitchen] — [Pantry]
   |          |             |             |
[Library] — [Entrance] — [Dining Room] ——┘
             |
         [Garden]
```

### Room Descriptions

1. **Entrance Hall**: Grand entrance with dusty chandelier, starting point
2. **Living Room**: Elegant room with covered furniture, contains Silver Key
3. **Dining Room**: Formal dining room with watchful portraits, contains Holy Water
4. **Kitchen**: Old-fashioned kitchen with moving shadows, contains Music Box
5. **Library**: Vast library with scattered books, contains Old Diary
6. **Study**: Private study with papers and candlesticks
7. **Grand Staircase**: Magnificent staircase with whispers from above
8. **Pantry**: Locked storage room containing the Golden Key
9. **Bedroom**: Odette's preserved bedroom where she appears
10. **Garden**: Escape point with locked gate

### Items and Their Purposes

1. **Silver Key**: Unlocks the pantry door
2. **Golden Key**: Unlocks the garden gate (escape key)
3. **Candle**: Provides light in dark areas
4. **Holy Water**: Protection against evil spirits
5. **Portrait**: Odette's painting from when she was alive
6. **Music Box**: Antique music box with haunting melody
7. **Old Diary**: Contains Odette's memories and secrets

---

## Technical Implementation

### Programming Language and Libraries

- **Python 3.x**: Core programming language
- **os**: For cross-platform screen clearing
- **time**: For creating pauses and delays
- **random**: For potential future random events

### Code Structure

The game follows a modular, object-oriented approach with clear separation of concerns:

```python
# Main Classes
- Item: Represents collectible objects
- Player: Manages player state and inventory
- Room: Represents game locations
- HauntedMansionGame: Main game controller

# Key Methods
- setup_game(): Initialize game world
- game_loop(): Main game execution loop
- handle_player_input(): Process user commands
- move_player(): Handle room transitions
- encounter_odette(): Special NPC interaction
```

---

## Data Structures

### Primary Data Structures Used

1. **Dictionary (self.rooms)**
   - **Purpose**: Store all room objects with string keys
   - **Key-Value Pairs**: Room name → Room object
   - **Justification**: Provides O(1) lookup time for room access

2. **Dictionary (self.game_items)**
   - **Purpose**: Store all item objects for easy reference
   - **Key-Value Pairs**: Item name → Item object
   - **Justification**: Centralized item management and creation

3. **List (player.bag)**
   - **Purpose**: Store collected items in player's inventory
   - **Capacity**: Maximum 4 items
   - **Justification**: Ordered collection with dynamic sizing

4. **Dictionary (room.connections)**
   - **Purpose**: Define possible movements from each room
   - **Key-Value Pairs**: Direction → Destination room name
   - **Justification**: Flexible navigation system

5. **List (room.items)**
   - **Purpose**: Store items present in each room
   - **Justification**: Dynamic collection that can be modified

### Data Structure Relationships

```python
# Game World Hierarchy
HauntedMansionGame
├── Player (contains bag: List[Item])
├── rooms: Dict[str, Room]
│   └── Room (contains items: List[Item], connections: Dict[str, str])
└── game_items: Dict[str, Item]
```

---

## Object-Oriented Design

### Class Design Philosophy

The game implements a clean object-oriented design with each class having a single responsibility:

### Item Class
```python
class Item:
    """Represents collectible items in the game."""
    
    def __init__(self, name, description, use_description=""):
        self.name = name
        self.description = description  
        self.use_description = use_description
```

**Responsibility**: Encapsulate item properties and behavior
**Attributes**: Name, description, usage information
**Methods**: String representation

### Player Class
```python
class Player:
    """Manages player state and inventory."""
    
    def __init__(self, name):
        self.name = name
        self.current_room = "entrance_hall"
        self.bag = []  # List to store items
        self.bag_capacity = 4
        # ... other state variables
```

**Responsibility**: Track player state, manage inventory
**Key Methods**: 
- `add_item()`: Add items to inventory with capacity checking
- `remove_item()`: Remove items from inventory
- `has_item()`: Check if player possesses specific item
- `show_bag()`: Display inventory contents

### Room Class
```python
class Room:
    """Represents locations in the game world."""
    
    def __init__(self, name, description, items=None, connections=None):
        self.name = name
        self.description = description
        self.items = items or []
        self.connections = connections or {}
        self.visited = False
```

**Responsibility**: Represent game locations and their properties
**Key Methods**: 
- `get_available_directions()`: Return possible movement directions

### HauntedMansionGame Class
```python
class HauntedMansionGame:
    """Main game controller managing all game logic."""
    
    def __init__(self):
        self.player = None
        self.rooms = {}
        self.game_items = {}
        self.game_running = True
        self.setup_game()
```

**Responsibility**: Coordinate all game systems and handle game flow
**Key Methods**:
- `setup_game()`: Initialize game world
- `game_loop()`: Main execution loop
- `handle_player_input()`: Process commands
- `move_player()`: Handle navigation
- `encounter_odette()`: Special event handling

---

## Module Structure

### Decomposition into Subproblems

The game is broken down into the following logical modules:

1. **Game Initialization Module**
   - Setup game world (rooms, items, connections)
   - Create player character
   - Display welcome screen

2. **Input Processing Module**
   - Parse player commands
   - Validate input
   - Route to appropriate handlers

3. **Navigation Module**
   - Handle room transitions
   - Check movement restrictions
   - Update player location

4. **Inventory Management Module**
   - Item collection logic
   - Bag capacity management
   - Item usage system

5. **Game State Module**
   - Track game progress
   - Check win/lose conditions
   - Manage game flags

6. **Display Module**
   - Room information display
   - Interface management
   - Screen clearing functionality

7. **Event Handling Module**
   - Special encounters (Odette)
   - Locked door logic
   - Story progression

### Inter-Module Relationships

```
Game Initialization → Game State → Display
         ↓              ↓           ↓
Input Processing → Navigation → Inventory Management
         ↓              ↓           ↓
Event Handling ← — — — — — — — — — — —
```

---

## Installation Guide

### System Requirements

- Python 3.6 or higher
- Windows, macOS, or Linux operating system
- Terminal/Command Prompt access

### Installation Steps

1. **Download the Game**
   ```bash
   # Download the main.py file
   # Or clone from repository
   git clone https://github.com/sparechange679/haunted_mansion_game.git
   ```

2. **Verify Python Installation**
   ```bash
   python --version
   # or
   python3 --version
   ```

3. **Navigate to Game Directory**
   ```bash
   cd path/to/game/directory
   ```

4. **Run the Game**
   ```bash
   python haunted_mansion_game.py
   # or
   python3 haunted_mansion_game.py
   ```

### File Structure

```
haunted_mansion_game/
├── haunted_mansion_game.py    # Main game file
├── README.md                  # This documentation
└── test_results/              # Testing evidence
    ├── test_log.txt
    └── screenshots/
```

---

## User Guide

### Getting Started

1. **Launch the Game**: Run the Python script
2. **Enter Character Name**: Type your character's name when prompted
3. **Read the Story**: Follow the atmospheric introduction
4. **Begin Exploration**: Use commands to navigate and interact

### Basic Commands

| Command | Description | Example |
|---------|-------------|---------|
| `go [direction]` | Move to connected room | `go north` |
| `[direction]` | Direct movement | `east` |
| `pick up [item]` | Collect an item | `pick up silver key` |
| `take [item]` | Alternative pickup | `take candle` |
| `bag` | View inventory | `bag` |
| `check bag` | View inventory | `check bag` |
| `look around` | Examine room | `look around` |
| `use [item]` | Use an item | `use holy water` |
| `quit` | Exit game | `quit` |

### Gameplay Tips

1. **Explore Thoroughly**: Visit all rooms to find items
2. **Manage Inventory**: You can only carry 4 items at once
3. **Talk to Odette**: She provides important story information
4. **Find Keys**: Some doors require specific keys
5. **Read Descriptions**: Room descriptions contain important clues

### Win Condition

To escape the mansion, you must:
1. Collect the Golden Key from the Pantry
2. Gather several of Odette's belongings
3. Navigate to the Garden
4. Use the Golden Key to unlock the gate

---

## Testing Strategy

### Testing Approach

The game requires comprehensive testing across multiple dimensions:

### Unit Testing

**Player Class Tests**:
- Inventory management (add/remove items)
- Bag capacity enforcement
- Item existence checking
- Player state tracking

**Room Class Tests**:
- Room connections validation
- Item management within rooms
- Direction availability

**Item Class Tests**:
- Item creation and properties
- String representation

### Integration Testing

**Navigation System**:
- Room-to-room movement
- Locked door functionality
- Invalid direction handling

**Inventory System**:
- Item pickup from rooms
- Bag capacity limits
- Item usage mechanics

**Game State Management**:
- Win condition checking
- Game progression tracking
- State persistence

### System Testing

**Complete Gameplay Scenarios**:
- Full game completion path
- Alternative exploration routes
- Error condition handling

**User Interface Testing**:
- Command parsing accuracy
- Screen clearing functionality
- Information display clarity

### Test Data Categories

1. **Normal Data**:
   - Valid movement commands
   - Correct item names
   - Standard gameplay actions

2. **Extreme Data**:
   - Maximum inventory capacity
   - Visiting all rooms
   - Collecting all items

3. **Invalid Data**:
   - Non-existent directions
   - Invalid item names
   - Unrecognized commands

### Sample Test Log

| Test # | Purpose | Input | Expected Result | Actual Result | Status |
|--------|---------|-------|----------------|---------------|---------|
| 1 | Player creation | "Alice" | Player named Alice created | Player named Alice created | PASS |
| 2 | Basic movement | "go north" | Move to Living Room | Moved to Living Room | PASS |
| 3 | Item pickup | "pick up candle" | Candle added to bag | Candle added to bag | PASS |
| 4 | Bag capacity | Pick up 5 items | Error after 4th item | Error after 4th item | PASS |
| 5 | Invalid direction | "go up" from entrance | Error message | Error message displayed | PASS |
| 6 | Win condition | Reach garden with golden key | Victory message | Victory message shown | PASS |

---

## Code Documentation

### Function Documentation

#### Core Game Functions

**`setup_game()`**
- **Purpose**: Initialize all game components
- **Parameters**: None
- **Returns**: None
- **Side Effects**: Creates rooms, items, and connections
- **Libraries Used**: None

**`game_loop()`**
- **Purpose**: Main game execution cycle
- **Parameters**: None
- **Returns**: None
- **Side Effects**: Manages game state and user interaction
- **Libraries Used**: os (for screen clearing)

**`handle_player_input()`**
- **Purpose**: Process and route player commands
- **Parameters**: None
- **Returns**: None
- **Side Effects**: Modifies game state based on input
- **Libraries Used**: None

**`move_player(direction)`**
- **Purpose**: Handle player movement between rooms
- **Parameters**: direction (string) - Direction to move
- **Returns**: None
- **Side Effects**: Updates player location
- **Libraries Used**: time (for movement delays)

**`encounter_odette()`**
- **Purpose**: Handle special NPC interaction
- **Parameters**: None
- **Returns**: None
- **Side Effects**: Updates story progression flags
- **Libraries Used**: None

#### Utility Functions

**`clear_screen()`**
- **Purpose**: Clear terminal screen for clean interface
- **Parameters**: None
- **Returns**: None
- **Side Effects**: Clears terminal display
- **Libraries Used**: os (cross-platform screen clearing)

**`pick_up_item(item_name)`**
- **Purpose**: Handle item collection from rooms
- **Parameters**: item_name (string) - Name of item to collect
- **Returns**: None
- **Side Effects**: Moves item from room to player inventory
- **Libraries Used**: None

### Library Usage

1. **os Library**
   - **Functions Used**: `os.system()`, `os.name`
   - **Purpose**: Cross-platform screen clearing
   - **Implementation**: Detects OS and uses appropriate clear command

2. **time Library**
   - **Functions Used**: `time.sleep()`
   - **Purpose**: Create pauses for dramatic effect
   - **Implementation**: Brief delays during movement and events

3. **random Library**
   - **Functions Used**: Currently imported but not used
   - **Purpose**: Reserved for future random event implementation

### Error Handling

The game implements comprehensive error handling:

1. **Input Validation**: All user inputs are validated and sanitized
2. **Graceful Degradation**: Invalid commands result in helpful error messages
3. **State Protection**: Game state is protected from invalid modifications
4. **Resource Management**: Proper handling of inventory limits and room connections

### Code Quality Features

1. **Documentation**: Comprehensive docstrings for all classes and methods
2. **Type Hints**: Clear parameter and return type documentation
3. **Modular Design**: Logical separation of concerns
4. **Error Messages**: User-friendly error reporting
5. **Code Comments**: Inline explanations for complex logic

---

## Conclusion

The Haunted Mansion Escape Game successfully implements all required features from the assignment specification while providing an engaging and atmospheric gaming experience. The object-oriented design ensures maintainability and extensibility, while the comprehensive testing strategy validates functionality across all game systems.

The game demonstrates proficiency in:
- Object-oriented programming principles
- Modular software design
- User interface development
- Game state management
- Error handling and validation
- Code documentation and testing

Future enhancements could include:
- Graphics integration using libraries like Pygame
- Save/load game functionality
- Additional rooms and items
- Random event generation
- Multiplayer capabilities

---

**Author**: Blessings Kishindo Sabuni
**Course**: Introduction to Programming with Python  
**Institution**: NCC Education  
**Date**: 3 July 2025  
**Version**: 1.0