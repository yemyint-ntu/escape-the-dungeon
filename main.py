import game
import random

# npc = NonplayerCharacter("Happy", "NPC", Attribute(5, 3, 2))  # create an object of NonplayerCharacter class

# print(f"NPC Name: {npc.name}, Class: {npc.character_class}, Max Health: {npc.max_health}, Current Health: {npc.current_health}")

# hero = PlayerCharacter("Hero", "Warrior", Attribute(6, 4, 3))
# iron_sword = Weapon("iron sword", "1d6")
# dagger = Weapon("dagger", "1d4")
# magic_sword = Weapon("magic sword", "2d4")

# beginner_armor = Armor("beginner armor", "cloth armor")
# hero.equip(Equipment(iron_sword, beginner_armor))
# hero.attack(npc)

# print(f"Player Name: {hero.name}, Class: {hero.character_class}, Max Health: {hero.max_health}, Current Health: {hero.current_health}")

# def attack(attacker, enemy):
#     damage = attacker["attributes"]["strength"] + dice_roll(sides_per_die=6)
#     # reduce the damage based on enemy's armor value
#     damage = damage - get_armor_value(enemy)
#     enemy["current_health"] = enemy["current_health"] - damage
#     return damage

# def get_armor_value(character):
#     return armor_value[character["equipments"]["armor"]]

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

# Monster encounter
skeleton_monster = game.NonplayerCharacter("skeleton", "Undead", game.Attribute(4, 2, 0))
zombie_monster = game.NonplayerCharacter("zombie", "Undead", game.Attribute(5, 1, 0))
goblin_monster = game.NonplayerCharacter("goblin", "Beast", game.Attribute(3, 4, 0))
dragon_monster = game.NonplayerCharacter("dragon", "Dragon", game.Attribute(20, 10, 5))

monster_list = [ skeleton_monster, zombie_monster, goblin_monster, dragon_monster ]
monster = random.choice(monster_list)

print(f"\n⚠️ You have encountered a {monster.name}!")

loot_list = ["leather armor", "sword", "dagger", "staff", "mace", "axe"] # this is a list
#index          0,        1,      2,        3       4      5

while True: #infinite loop
    # if player health is less than or equal to zero
    # exit from the loop
    if player.current_health <= 0:
        break

    # print(f"\nYour Health: {health} | Skeleton Health: {monster_health}")
    action = input("Choose action: attack / dodge / spell: ").lower()
    has_dodged = False
    if action == 'attack':
        damage = player.attack(monster)
        print(f"You swing your weapon and deal {damage} damage!")

    elif action == 'dodge':
        has_dodged = player.dodge()
        if has_dodged:
            print("You dodged the attack!")
        else:
            print("You tried to dodge but failed!")

    elif action == 'spell':
        if attr.mind >= 6:
            print("You cast a powerful fireball!")
            monster.current_health = 0
        else:
            print("You fail to cast the spell.")
    else:
        print("Invalid action. Choose attack, dodge, or spell.")

    if monster.current_health <= 0:
        print(f"You defeated the {monster.name}!")
        print("Here are the possilbe loot items:")
        
        for loot in loot_list: # loop through the list
            print(loot)
        
        print("Rolling the dice ...")

        looted_items = game.loot_roll(loot_list)  # loot_roll returns a list of looted items
        loot_gold = game.dice_roll(number_of_dice=5, sides_per_die=4)

        print(f"The {monster.name} dropped {looted_items} and {loot_gold} golds. Congrats!")
        player.inventory.extend(looted_items) # add a list to another list
        player.gold += loot_gold # gold = gold + loot_gold
        break
    else:
        if not has_dodged: # if has_dodged == False:
            # Monster attacks back
            hit = monster.attack(player)

            print(f"The {monster.name} hits you for {hit} damage. Your health is now {player.current_health}.")

# if player health is less than or equal to zero
# print game over
if player.current_health <= 0:
    print("Game Over!!")
else:
    print("Congratulations, brave adventurer! You have escaped the dungeon.")
    print(f"You now have {player.inventory} in your inventory and {player.gold} golds.")
# End of the game
