import game
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
player.equip_armor(game.Armor("cloth armor", "cloth armor"))
player.equip_weapon(game.Weapon("dagger", "1d4"))

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
