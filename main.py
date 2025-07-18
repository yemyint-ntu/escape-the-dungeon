import random

def dice_roll(sides_per_die, number_of_dice=1): # function definition
    sum = 0
    for _ in range(number_of_dice): # _ means the value is not used
        sum += random.randint(1, sides_per_die)
    return sum

def loot_roll(loot_list):
    number_of_loot_items = dice_roll(sides_per_die=3)  # roll a die to determine number of loot items
    looted_items = []
    # write a for loop number_of_loot_items times
        # in each iteration, select a random item from loot_list
        # and append it to looted_items
    # return the looted_items list


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
    strength, agility, mind = 8, 4, 2
elif class_choice == "2":
    player_class = "Rogue"
    strength, agility, mind = 4, 8, 2
elif class_choice == "3":
    player_class = "Mage"
    strength, agility, mind = 2, 4, 8
else:
    print("Invalid choice, defaulting to Warrior.")
    player_class = "Warrior"
    strength, agility, mind = 8, 4, 2

# declaring a dictionary
player = {
    "name": character_name,
    "class": player_class,
    "attributes": {
        "strength": strength,
        "agility": agility,
        "mind": mind,
    },
    "max_health": 5 * strength,  # health is 5 times the strength
    "current_health": 5 * strength,  # current health is also 5 times the strength
    "gold": 5,
    "inventory": [],
}

# Monster encounter

# monster_name, monster_health, monster_attack_power <- Tuple
skeleton_monster = ("skeleton", 30, 4)
zombie_monster = ("zombie", 35, 5)
goblin_monster = ("goblin", 20, 3)
dragon_monster = ("dragon", 100, 10)

monster_list = [ skeleton_monster, zombie_monster, goblin_monster, dragon_monster ]
monster = random.choice(monster_list)
monster_name, monster_health, monster_attack_power = monster # unpacking the tuple
# monster_name = monster_list[monster_index][0]
# monster_health = monster_list[monster_index][1]
# monster_attack_power = monster_list[monster_index][2]
print(f"\n⚠️ You have encountered a {monster_name}!")


loot_list = ["armor", "sword", "dagger", "staff", "mace", "axe"] # this is a list
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
        damage = strength + dice_roll(sides_per_die=6)  # strength + dice_roll(1, 6)
        monster_health -= damage
        print(f"You swing your weapon and deal {damage} damage!")

    elif action == 'dodge':
        dodge_chance = agility * 5  # percentage
        if dice_roll(sides_per_die=100) <= dodge_chance:
            has_dodged = True
            print("You dodged the attack!")
        else:
            has_dodged = False
            print("You tried to dodge but failed!")

    elif action == 'spell':
        if mind >= 6:
            print("You cast a powerful fireball!")
            monster_health = 0
        else:
            print("You fail to cast the spell.")
    else:
        print("Invalid action. Choose attack, dodge, or spell.")

    if monster_health <= 0:
        print(f"You defeated the {monster_name}!")
        print("Here are the possilbe loot items:")
        
        for loot in loot_list: # loop through the list
            print(loot)
        
        print("Rolling the dice ...")

        # Change to random.choice for selecting loot
        number_of_loot_items = dice_roll(sides_per_die=3) # roll a die to determine number of loot items
        loot = random.choice(loot_list) # select a random loot item

        loot_gold = dice_roll(number_of_dice=5, sides_per_die=4)

        print(f"The {monster_name} dropped one {loot} and {loot_gold} golds. Congrats!")
        player["inventory"].append(loot) # how to add an item to the list

        player["gold"] += loot_gold # gold = gold + loot_gold
        break
    else:
        if not has_dodged: # if has_dodged == False:
            # Monster attacks back
            hit = dice_roll(sides_per_die=6) + monster_attack_power
            player["current_health"] -= hit
            print(f"The {monster_name} hits you for {hit} damage. Your health is now {player["current_health"]}.")

# if player health is less than or equal to zero
# print game over
if player["current_health"] <= 0:
    print("Game Over!!")
else:
    print("Congratulations, brave adventurer! You have escaped the dungeon.")
    print(f"You now have {player["inventory"]} in your inventory and {player["gold"]} golds.")
# End of the game
