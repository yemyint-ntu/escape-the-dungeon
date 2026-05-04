import game
import random

class GameState:
    NOT_STARTED = "not_started"
    CHAR_CREATION = "character_creation"
    EXPLORATION = "exploration"
    COMBAT = "combat"
    COMPLETED = "completed"
    GAME_OVER = "game_over"

    def __init__(self):
        self.available_actions = []

    def get_available_actions(self) -> str:
        return f"Available actions: {', '.join(self.available_actions)}"

    def response_to_command(self, command: str) -> dict:
        # This method will process the player's command based on the current game state
        pass

class NotStartedState(GameState):
    def __init__(self):
        self.available_actions = ["start"]

    def response_to_command(self, command: str) -> dict:
        if command == "start":
            # transition to character creation state
            return {"game_response": "Welcome to Escape the Dungeon! Your adventure begins now..."}
        else:
            return {"game_response": "Please type 'start' to begin the game."}
        
class CharacterCreationState(GameState):
    def __init__(self):
        self.available_actions = []

    def response_to_command(self, command: str) -> dict:
        # Handle character creation commands
        pass

class ExplorationState(GameState):
    def __init__(self):
        self.available_actions = ["go [direction]", "take [item]", "use [item]", "inventory", "equip [weapon/armor]"]

    def response_to_command(self, command: str) -> dict:
        # Handle exploration commands
        if command.startswith('go '):
            direction = command.split()[1].lower()
            return self._go_to(direction)

        elif command.startswith('take '):
            item = command.removeprefix('take ').lower()
            return self._take(item)
        
        elif command.startswith('use '):
            item = command.removeprefix('use ') 
            return self._use(item)
        
        elif command == 'inventory':
            return self._inventory()
        
        elif command.startswith('equip '):
            equip_item = command.removeprefix('equip ').lower()
            return self._equip(equip_item)
    
    def _go_to(self, direction: str) -> dict:
        # Handle movement logic
        pass

    def _take(self, item: str) -> dict:
        # Handle item pickup logic
        pass

    def _use(self, item: str) -> dict:
        # Handle item usage logic
        pass

    def _inventory(self) -> dict:
        # Handle inventory display logic
        pass

    def _equip(self, equip_item: str) -> dict:
        # Handle equip logic
        pass

class GameEngine:
    # states
    NOT_STARTED = "not_started"
    CHAR_CREATION = "character_creation"
    EXPLORATION = "exploration"
    COMBAT = "combat"
    COMPLETED = "completed"
    GAME_OVER = "game_over"

    def __init__(self):
        self.player = None
        self.current_room = 'Cell'
        self.rooms = {
            'Cell': {
                'description': 'A cold, dark cell. The door is locked.',
                'east': 'Hallway (locked)',
                'item': 'key'
            },
            'Hallway': {
                'description': 'A dim hallway. A heavy gate blocks the north path.',
                'west': 'Cell',
                'encounter': True,
                'north': 'Armory'
            },
            'Armory': {
                'description': 'A room full of rusty weapons and a glowing staff.',
                'south': 'Hallway',
                'item': 'magic staff',
                'encounter': True,
                'east': 'Exit'
            },
            'Exit': {
                'description': 'A magical door that needs a spell to open.',
                'west': 'Armory'
            }
        }
        
        # Monsters
        skeleton_monster = game.NonplayerCharacter("skeleton", "Undead", game.Attribute(4, 2, 0))
        skeleton_monster.equip_armor(game.Armor("leather armor", "leather armor"))
        skeleton_monster.equip_weapon(game.Weapon("iron sword", "1d6"))

        zombie_monster = game.NonplayerCharacter("zombie", "Undead", game.Attribute(5, 1, 0))
        zombie_monster.equip_armor(game.Armor("cloth armor", "cloth armor"))
        zombie_monster.equip_weapon(game.Weapon("claws", "1d4"))

        goblin_monster = game.NonplayerCharacter("goblin", "Beast", game.Attribute(3, 4, 0))
        goblin_monster.equip_armor(game.Armor("leather armor", "leather armor"))
        goblin_monster.equip_weapon(game.Weapon("club", "1d6"))
        
        self.monsters = [ skeleton_monster, zombie_monster, goblin_monster, skeleton_monster, zombie_monster, skeleton_monster ]
        self.state = self.NOT_STARTED
        self.enemy = None

    def response_to_command(self, command: str) -> dict:
        command = command.strip().lower()

        # This method will process the player's command based on the current game state
        if self.state == self.NOT_STARTED:
            if command == "start":
                self.state = self.CHAR_CREATION
                # default character creation for now, can be expanded to allow player choice later
                self.player = game.PlayerCharacter("Adventurer", "Warrior", game.Attribute(8, 4, 2))
                self.player.equip_armor(game.Armor("chainmail armor", "chainmail"))
                self.player.equip_weapon(game.Weapon("longsword", "1d8"))

                # learn a starting skill
                power_strike_skill = game.Skill("Power Strike", "2d6", 150)
                self.player.learn_skill(power_strike_skill)

                self.state = self.EXPLORATION
                response = "Welcome to Escape the Dungeon! Your adventure begins now..."

                room_status = f"You are in the {self.current_room}.\n\n{self.rooms[self.current_room]['description']}"
                if 'item' in self.rooms[self.current_room]:
                    room_status += f"\nYou see a {self.rooms[self.current_room]['item']} here."

                response += "\n\nAvailable actions: go [direction], take [item], use [item], stats, inventory, equip [weapon/armor], exit."
                response += "\n\nWhat do you want to do?"

                return {
                    "game_response": response,
                    "status_update": room_status,
                    "character_update": self.player.get_status()
                }
            else:
                return {"game_response": "Please type 'start' to begin the game."}
        elif self.state == self.EXPLORATION:
            # Handle exploration commands
            if command.startswith('go '):
                direction = command.split()[1].lower()
                if direction in self.rooms[self.current_room]:
                    if self.rooms[self.current_room][direction].lower().endswith('(locked)'):
                        return {"game_response": "The path is locked. You need a key to proceed."}
                    else:
                        self.current_room = self.rooms[self.current_room][direction]
                        response = f"You move {direction} to the {self.current_room}."

                        room_status = f"You are in the {self.current_room}.\n\n{self.rooms[self.current_room]['description']}"

                        if 'encounter' in self.rooms[self.current_room] and self.rooms[self.current_room]['encounter'] == True:
                            self.state = self.COMBAT
                            self.enemy = random.choice(self.monsters)
                            response += f"\n\nAs you enter the {self.current_room}, you encounter a {self.enemy.name}!"
                            return {
                                "game_response": response,
                                "status_update": room_status
                            }

                        if self.current_room == 'Exit':
                            self.state = self.COMPLETED
                            response += "\n\nCongratulations, brave adventurer! You have escaped the dungeon."
                            return {"game_response": response}

                        
                        if 'item' in self.rooms[self.current_room]:
                            room_status += f"\nYou see a {self.rooms[self.current_room]['item']} here."

                        response += "\n\nAvailable actions: go [direction], take [item], use [item], stats, inventory, equip [weapon/armor], exit."
                        response += "\n\nWhat do you want to do?"

                        return {
                            "game_response": response,
                            "status_update": room_status
                        }
            elif command.startswith('take '):
                item = command.removeprefix('take ').lower()
                if 'item' in self.rooms[self.current_room] and item == self.rooms[self.current_room]['item']:
                    self.player.inventory.append(game.QuestItem(self.rooms[self.current_room].pop('item')))
                    return {
                            "game_response": f"You have taken the {item}.",
                            "character_update": self.player.get_status()
                        }
                else:
                    return {"game_response": "Invalid item, try again."}
            elif command.startswith('use '):
                item = command.removeprefix('use ') 
                if self.player.is_in_inventory(item):
                    if item.lower() == 'key' and self.current_room == 'Cell':
                        self.player.use_item('key')
                        self.rooms['Cell']['east'] = 'Hallway'
                        self.rooms['Cell']['description'] = self.rooms['Cell']['description'].replace('locked', 'unlocked')
                        return {
                            "game_response": "You use the key to unlock the door to the Hallway.",
                            "status_update": f"You are in the {self.current_room}.\n\n{self.rooms[self.current_room]['description']}",
                            "character_update": self.player.get_status()
                        }
                    else:
                        self.player.use_item(item)
                        return {
                            "game_response": f"You use the {item}.",
                            "character_update": self.player.get_status()
                        }
                else:
                    return {"game_response": f"You don't have the {item} in your inventory."}
            elif command == 'inventory':
                if self.player.inventory:
                    inventory_list = "\n".join(f"- {item}" for item in self.player.inventory)
                    return {"game_response": f"Your inventory contains:\n{inventory_list}"}
                else:
                    return {"game_response": "Your inventory is empty."}
            elif command.startswith('equip '):
                equip_item = command.removeprefix('equip ').lower()
                if self.player.is_in_inventory(equip_item):
                    is_equip_successful = self.player.equip(equip_item) 
                    if is_equip_successful:
                        return {
                            "game_response": f"You have equipped the {equip_item}.",
                            "character_update": self.player.get_status()
                        }
                    else:
                        return {"game_response": f"Failed to equip the {equip_item}."}
                else:
                    return {"game_response": f"You don't have the {equip_item} in your inventory."}
            
        elif self.state == self.COMBAT:
            # Handle combat commands
            pass

        if command in ["quit", "exit"]:
            return {"game_response": "Press Ctrl+Q to exit."}
        else:
            return {"game_response": "Command not recognized. Try again."}
