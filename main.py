import random

class Equipment:
    def __init__(self, weapon, armor):
        self.weapon = weapon
        self.armor = armor

class Attribute:
    def __init__(self, strength, agility, mind):
        self.strength = strength
        self.agility = agility
        self.mind = mind

class Character:
    def __init__(self, name, character_class, attributes): #constructor method
        self.name = name
        self.character_class = character_class
        self.max_health = attributes.strength * 5
        self.current_health = self.max_health
        self.attributes = attributes
        # default values
        self.equipments = None

    def equip(self, equipment):
        self.equipments = equipment

    def get_armor_value(self):
        if self.equipments != None and self.equipments.armor != None:
            return armor_value[self.equipments.armor]
        return 0

    def attack(self, enemy):
        damage = self.attributes.strength + dice_roll(sides_per_die=6)
        damage = damage - enemy.get_armor_value()
        enemy.current_health = enemy.current_health - damage
        return damage

class PlayerCharacter(Character): # inheritance - parent class is Character
    def __init__(self, name, character_class, attributes):
        super().__init__(name, character_class, attributes) # super() means parent class Character
        self.gold = 0
        self.inventory = []

class NonplayerCharacter(Character):
    def __init__(self, name, character_class, attributes):
        super().__init__(name, character_class, attributes)

npc = NonplayerCharacter("Happy", "NPC", Attribute(5, 3, 2))  # create an object of NonplayerCharacter class

print(f"NPC Name: {npc.name}, Class: {npc.character_class}, Max Health: {npc.max_health}, Current Health: {npc.current_health}")

hero = PlayerCharacter("Hero", "Warrior", Attribute(6, 4, 3))
hero.equip(Equipment("sword", "leather armor"))
hero.attack(npc)

print(f"Player Name: {hero.name}, Class: {hero.character_class}, Max Health: {hero.max_health}, Current Health: {hero.current_health}")

def dice_roll(sides_per_die, number_of_dice=1): # function definition
    total = 0
    # for loop with number_of_dice times
    for _ in range(number_of_dice): # _ means the value is not used
        # in each iteration, add a random number between 1 and sides_per_die to total
        total += random.randint(1, sides_per_die)
    # return the total
    return total

def loot_roll(loot_list):
    number_of_loot_items = dice_roll(sides_per_die=3)  # roll a die to determine number of loot items
    looted_items = []
    # write a for loop number_of_loot_items times
    for _ in range(number_of_loot_items):
        # in each iteration, select a random item from loot_list
        loot = random.choice(loot_list)
        # and append it to looted_items
        looted_items.append(loot)
    # return the looted_items list
    return looted_items

def attack(attacker, enemy):
    damage = attacker["attributes"]["strength"] + dice_roll(sides_per_die=6)
    # reduce the damage based on enemy's armor value
    damage = damage - get_armor_value(enemy)
    enemy["current_health"] = enemy["current_health"] - damage
    return damage

def get_armor_value(character):
    return armor_value[character["equipments"]["armor"]]

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
    attr = Attribute(8, 4, 2)
elif class_choice == "2":
    player_class = "Rogue"
    attr = Attribute(4, 8, 2)
elif class_choice == "3":
    player_class = "Mage"
    attr = Attribute(2, 4, 8)
else:
    print("Invalid choice, defaulting to Warrior.")
    player_class = "Warrior"
    attr = Attribute(8, 4, 2)

# declaring a dictionary
player = {
    "name": character_name,
    "class": player_class,
    "attributes": {
        "strength": attr.strength,
        "agility": attr.agility,
        "mind": attr.mind,
    },
    "equipments": {
        "armor": "leather armor",
    },
    "max_health": 5 * attr.strength,  # health is 5 times the strength
    "current_health": 5 * attr.strength,  # current health is also 5 times the strength
    "gold": 5,
    "inventory": [],
}

_player = PlayerCharacter(character_name, player_class, attr)

# Monster encounter

# monster_name, monster_health, monster_attack_power <- Tuple
skeleton_monster = {
    "name": "skeleton",
    "attributes": {
        "strength": 4,
        "agility": 2,
        "mind": 0,
    },
    "equipments": {
        "armor": "cloth armor",
    },
    "max_health": 30,  # health is 5 times the strength
    "current_health": 30,  # current health is also 5 times the strength
}

_skeleton_monster = NonplayerCharacter("skeleton", "Undead", Attribute(4, 2, 0))

zombie_monster = {
    "name": "zombie",
    "attributes": {
        "strength": 5,
        "agility": 1,
        "mind": 0,
    },
    "equipments": {
        "armor": "cloth armor",
    },
    "max_health": 35,
    "current_health": 35,
}

goblin_monster = {
    "name": "goblin",
    "attributes": {
        "strength": 3,
        "agility": 4,
        "mind": 0,
    },
    "equipments": {
        "armor": "leather armor",
    },
    "max_health": 20,
    "current_health": 20,
}

dragon_monster = {
    "name": "dragon",
    "attributes": {
        "strength": 20,
        "agility": 10,
        "mind": 5,
    },
    "equipments": {
        "armor": "dragon scale",
    },
    "max_health": 100,
    "current_health": 100,
}

monster_list = [ skeleton_monster, zombie_monster, goblin_monster, dragon_monster ]
monster = random.choice(monster_list)

print(f"\n⚠️ You have encountered a {monster["name"]}!")

armor_value = {
    "none": 0,
    "cloth armor": 1,
    "leather armor": 2,
    "chainmail": 3,
    "plate armor": 4,
    "dragon scale": 5,
}
loot_list = ["leather armor", "sword", "dagger", "staff", "mace", "axe"] # this is a list
#index          0,        1,      2,        3       4      5

while True: #infinite loop
    # if player health is less than or equal to zero
    # exit from the loop
    if player["current_health"] <= 0:
        break

    # print(f"\nYour Health: {health} | Skeleton Health: {monster_health}")
    action = input("Choose action: attack / dodge / spell: ").lower()
    has_dodged = False
    if action == 'attack':
        damage = attack(player, monster)
        print(f"You swing your weapon and deal {damage} damage!")

    elif action == 'dodge':
        dodge_chance = attr.agility * 5  # percentage
        if dice_roll(sides_per_die=100) <= dodge_chance:
            has_dodged = True
            print("You dodged the attack!")
        else:
            has_dodged = False
            print("You tried to dodge but failed!")

    elif action == 'spell':
        if attr.mind >= 6:
            print("You cast a powerful fireball!")
            monster["current_health"] = 0
        else:
            print("You fail to cast the spell.")
    else:
        print("Invalid action. Choose attack, dodge, or spell.")

    if monster["current_health"] <= 0:
        print(f"You defeated the {monster["name"]}!")
        print("Here are the possilbe loot items:")
        
        for loot in loot_list: # loop through the list
            print(loot)
        
        print("Rolling the dice ...")

        looted_items = loot_roll(loot_list)  # loot_roll returns a list of looted items
        loot_gold = dice_roll(number_of_dice=5, sides_per_die=4)

        print(f"The {monster["name"]} dropped {looted_items} and {loot_gold} golds. Congrats!")
        player["inventory"].extend(looted_items) # add a list to another list
        player["gold"] += loot_gold # gold = gold + loot_gold
        break
    else:
        if not has_dodged: # if has_dodged == False:
            # Monster attacks back
            hit = attack(monster, player)

            print(f"The {monster["name"]} hits you for {hit} damage. Your health is now {player["current_health"]}.")

# if player health is less than or equal to zero
# print game over
if player["current_health"] <= 0:
    print("Game Over!!")
else:
    print("Congratulations, brave adventurer! You have escaped the dungeon.")
    print(f"You now have {player["inventory"]} in your inventory and {player["gold"]} golds.")
# End of the game
