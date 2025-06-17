import random

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
print("3. Mage (High Magic)")

# accept input from the player using the following prompt
# "Enter 1, 2, or 3: "
# Store the user's choice in a variable called class_choice
class_choice = input("Enter 1, 2, or 3: ")

if class_choice == "1":
    player_class = "Warrior"
    strength, agility, magic = 8, 4, 2
elif class_choice == "2":
    player_class = "Rogue"
    strength, agility, magic = 4, 8, 2
elif class_choice == "3":
    player_class = "Mage"
    strength, agility, magic = 2, 4, 8
else:
    print("Invalid choice, defaulting to Warrior.")
    player_class = "Warrior"
    strength, agility, magic = 8, 4, 2

health = 100
gold = 5
inventory = [] #empty list

# Monster encounter
monster_list = ["skeleton", "zombie", "goblin"]
monster_health_list = [ 30, 35, 20 ]
monster_index = random.randint(0, len(monster_list) - 1)
monster = monster_list[monster_index]
print(f"\n⚠️ You have encountered a {monster}!")
monster_health = monster_health_list[monster_index]

loot_list = ["armor", "sword", "dagger", "staff", "mace", "axe"] # this is a list
#index          0,        1,      2,        3       4      5

while True: #infinite loop
    # print(f"\nYour Health: {health} | Skeleton Health: {monster_health}")
    action = input("Choose action: attack / dodge / spell: ").lower()
    has_dodged = False
    if action == 'attack':
        damage = strength + random.randint(1, 6)
        monster_health -= damage
        print(f"You swing your weapon and deal {damage} damage!")

    elif action == 'dodge':
        dodge_chance = agility * 5  # percentage
        if random.randint(1, 100) <= dodge_chance:
            has_dodged = True
            print("You dodged the attack!")
        else:
            has_dodged = False
            print("You tried to dodge but failed!")

    elif action == 'spell':
        if magic >= 6:
            print("You cast a powerful fireball!")
            monster_health = 0
        else:
            print("You fail to cast the spell.")
    else:
        print("Invalid action. Choose attack, dodge, or spell.")

    if monster_health <= 0:
        print(f"You defeated the {monster}!")
        print("Here are the possilbe loot items:")
        
        for loot in loot_list: # loop through the list
            print(loot)
        
        print("Rolling the dice ...")
        loot_index = random.randint(0, len(loot_list) - 1) # random index from 0 to len(loot_list) - 1
        loot_gold = random.randint(5, 20)
        print(f"The {monster} dropped one {loot_list[loot_index]} and {loot_gold} golds. Congrats!")
        inventory.append(loot_list[loot_index]) # how to add an item to the list
        gold += loot_gold # gold = gold + loot_gold
        break
    else:
        if not has_dodged: # if has_dodged == False:
            # Monster attacks back
            hit = random.randint(1, 6) + 2
            health -= hit
            print(f"The {monster} hits you for {hit} damage. Your health is now {health}.")


print("Congratulations, brave adventurer! You have escaped the dungeon.")
print(f"You now have {inventory} in your inventory and {gold} golds.")
# End of the game
