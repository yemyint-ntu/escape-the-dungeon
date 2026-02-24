import game
import random

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer

class TextAdventureApp(App):

    def __init__(self):
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()


def game_loop():
    # accept input from the player using the following prompt:
    # "What is your name, brave adventurer? " 
    # Store the user's name in a variable called character_name
    character_name = input("What is your name, brave adventurer? ")

    # output the following to the screen
    # Welcome to Escape the Dungeon, adventurer $character_name
    print("Welcome to Escape the Dungeon, adventurer", character_name)

    # output the following to the screen
    # Choose your class:
    # 1. Warrior (High Strength)
    # 2. Rogue (High Agility)
    # 3. Mage (High Magic)
    print("Choose your class:")
    print("1. Warrior (High Strength)")
    print("2. Rogue (High Agility)")
    print("3. Mage (Magic User)")

    # accept input from the player using the following prompt
    # "Enter 1, 2, or 3: "
    # Store the user's choice in a variable called class_choice
    class_choice = input("Enter 1, 2, or 3: ")

    if class_choice == "1":
        player_class = "Warrior"
        attr = game.Attribute(8, 4, 2)
    elif class_choice == "2":
        player_class = "Rogue"
        attr = game.Attribute(4, 8, 2)
    elif class_choice == "3":
        player_class = "Mage"
        attr = game.Attribute(2, 4, 8)
    else:
        print("Invalid choice, defaulting to Warrior.")
        player_class = "Warrior"
        attr = game.Attribute(8, 4, 2)

    player = game.PlayerCharacter(character_name, player_class, attr)
    if player_class == "Warrior":
        player.equip_armor(game.Armor("chainmail armor", "chainmail"))
        player.equip_weapon(game.Weapon("longsword", "1d8"))

        # learn a starting skill
        power_strike_skill = game.Skill("Power Strike", "2d6", 150)
        player.learn_skill(power_strike_skill)
    elif player_class == "Rogue":
        player.equip_armor(game.Armor("leather armor",  "leather armor"))
        player.equip_weapon(game.Weapon("dagger",  "1d4"))

        # learn a starting skill
        backstab_skill = game.Skill("Backstab", "3d6", 200)
        player.learn_skill(backstab_skill)
    elif player_class == "Mage":
        player.equip_armor(game.Armor("cloth armor", "cloth armor"))
        player.equip_weapon(game.Weapon("staff", "1d5"))

        # learn a starting spell
        fireball_spell = game.Spell("Fireball", "2d10", 120)
        player.learn_spell(fireball_spell)
    else:
        player.equip_armor(game.Armor("cloth armor", "cloth armor"))
        player.equip_weapon(game.Weapon("sword", "1d6"))

    player.inventory.append(game.HealthPotion("Small Health Potion", 10))
    player.inventory.append(game.ThrowingKnife("Throwing Knife", "2d4"))

    player.show_stats()

    # Monster encounter
    skeleton_monster = game.NonplayerCharacter("skeleton", "Undead", game.Attribute(4, 2, 0))
    skeleton_monster.equip_armor(game.Armor("leather armor", "leather armor"))
    skeleton_monster.equip_weapon(game.Weapon("iron sword", "1d6"))

    zombie_monster = game.NonplayerCharacter("zombie", "Undead", game.Attribute(5, 1, 0))
    zombie_monster.equip_armor(game.Armor("cloth armor", "cloth armor"))
    zombie_monster.equip_weapon(game.Weapon("claws", "1d4"))

    goblin_monster = game.NonplayerCharacter("goblin", "Beast", game.Attribute(3, 4, 0))
    goblin_monster.equip_armor(game.Armor("leather armor", "leather armor"))
    goblin_monster.equip_weapon(game.Weapon("club", "1d6"))

    dragon_monster = game.NonplayerCharacter("dragon", "Dragon", game.Attribute(20, 10, 5))
    dragon_monster.equip_armor(game.Armor("scaled armor", "dragon scale"))
    dragon_monster.equip_weapon(game.Weapon("fire breath", "3d6"))

    monster_list = [ skeleton_monster, zombie_monster, goblin_monster, skeleton_monster ]

    # --- Rooms Map ---
    rooms = {
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

    # --- Start Game ---
    current_room = 'Cell'

    print("You find yourself in a dungeon. Your goal is to escape!")
    print ("Type 'exit' to quit the game or 'stats' to view your character sheet.")

    while True:
        print(f"\nYou are in the {current_room}.")
        print(rooms[current_room]['description'])

        if 'encounter' in rooms[current_room] and rooms[current_room]['encounter'] == True:
            monster = random.choice(monster_list)
            game.encounter(player, monster)
            rooms[current_room]['encounter'] = False  # prevent re-encounter in the same room
            if player.current_health <= 0:
                print("Game Over!!")
                break

        if 'item' in rooms[current_room]:
            print(f"You see a {rooms[current_room]['item']} here.")

        print("")
        print("Available actions: go [direction], take [item], use [item], stats, inventory, equip [weapon/armor], exit.")
        action = input("What do you want to do?: ").strip().lower()

        if action == 'exit':
            print("Exiting the game. Goodbye!")
            break
        elif action == 'stats':
            player.show_stats()
            continue
        elif action.startswith('go '):
            direction = action.split()[1].lower()
            if direction in rooms[current_room]:
                if rooms[current_room][direction].lower().endswith('(locked)'):
                    print("The path is locked. You need a key to proceed.")
                else:
                    current_room = rooms[current_room][direction]
                    if current_room == 'Exit':
                        print("Congratulations, brave adventurer! You have escaped the dungeon.")
                        break
            else:
                print("Invalid direction, try again.")
        elif action.startswith('take '):
            item = action.removeprefix('take ').lower()
            if 'item' in rooms[current_room] and item == rooms[current_room]['item']:
                player.inventory.append(game.QuestItem(rooms[current_room].pop('item')))
                print(f"You have taken the {item}.")
            else:
                print("Invalid item, try again.")
        elif action.startswith('use '):
            item = action.removeprefix('use ')
            if player.is_in_inventory(item):
                if item.lower() == 'key' and current_room == 'Cell':
                    player.use_item('key')
                    print("You use the key to unlock the door to the Hallway.")
                    rooms['Cell']['east'] = 'Hallway'
                    rooms['Cell']['description'] = rooms['Cell']['description'].replace('locked', 'unlocked')
                else:
                    player.use_item(item)

            else:
                print(f"You don't have the {item} in your inventory.")
        elif action == 'inventory':
            if player.inventory:
                print("Your inventory contains:")
                for item in player.inventory:
                    print(f"- {item}")
            else:
                print("Your inventory is empty.")
        elif action.startswith('equip '):
            equip_item = action.removeprefix('equip ').lower()
            if player.is_in_inventory(equip_item):
                player.equip(equip_item)

if __name__ == "__main__":
    # game_loop()
    app = TextAdventureApp()
    app.run()
