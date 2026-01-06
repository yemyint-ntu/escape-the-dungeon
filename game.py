import random

armor_value = {
    "none": 0,
    "cloth armor": 1,
    "leather armor": 2,
    "chainmail": 3,
    "plate armor": 4,
    "dragon scale": 5,
}

class Item:
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name

class QuestItem(Item):
    def __init__(self, name):
        super().__init__(name)

class Consumable(Item):
    def __init__(self, name, effect, amount):
        super().__init__(name)
        self.effect = effect
        self.amount = amount

    def use(self, character):
        if self.effect == "heal":
            character.current_health += self.amount
            if character.current_health > character.max_health:
                character.current_health = character.max_health
            print(f"{character.name} healed for {self.amount} health points.")

class Weapon(Item):
    def __init__(self, name, damage_dice):
        super().__init__(name)
        self.damage_dice = damage_dice

    def get_damage(self):
        # based on damage dice string
        result = self.damage_dice.split('d')
        num_dice = int(result[0])
        sides = int(result[1])
        return dice_roll(sides_per_die=sides, number_of_dice=num_dice)

class Armor(Item):
    def __init__(self, name, type):
        super().__init__(name)
        self.type = type

    def get_defense(self):
        return armor_value[self.type]

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
        self.equipments = Equipment(None, None)
        self.is_in_combat = False

    def equip_armor(self, armor):
        self.equipments.armor = armor
        
    def equip_weapon(self, weapon):
        self.equipments.weapon = weapon

    def get_armor_value(self):
        if self.equipments != None and self.equipments.armor != None:
            return self.equipments.armor.get_defense()
        return 0

    def attack(self, enemy):
        damage = self.attributes.strength + self.equipments.weapon.get_damage()
        damage = damage - enemy.get_armor_value()
        enemy.current_health = enemy.current_health - damage
        return damage
    
    def dodge(self):
        dodge_chance = self.attributes.agility * 5
        if dice_roll(sides_per_die=100) <= dodge_chance:
            has_dodged = True
        else:
            has_dodged = False
        return has_dodged
    
    def show_stats(self):
        if self.is_in_combat == False:
            print("\n--- Character Stats ---")
            print(f"Name: {self.name}")
            print(f"Class: {self.character_class}")
            print(f"Health: {self.current_health}/{self.max_health}")
            print(f"Strength: {self.attributes.strength}")
            print(f"Agility: {self.attributes.agility}")
            print(f"Mind: {self.attributes.mind}")
            if self.equipments.weapon != None:
                print(f"Weapon: {self.equipments.weapon.name} ({self.equipments.weapon.damage_dice})")
            else:
                print("Weapon: None")
            if self.equipments.armor != None:
                print(f"Armor: {self.equipments.armor.name} ({self.equipments.armor.type})")
            else:
                print("Armor: None")
            print(f"Armor Value: {self.get_armor_value()}")
        else:
            print(f"{self.name} is in combat!")

    def start_combat(self):
        self.is_in_combat = True

    def end_combat(self):
        self.is_in_combat = False

class PlayerCharacter(Character): # inheritance - parent class is Character
    def __init__(self, name, character_class, attributes):
        super().__init__(name, character_class, attributes) # super() means parent class Character
        self.gold = 0
        self.inventory = []
        self.spells = (None, None, None) # tuple with 3 spell slots

    def is_in_inventory(self, item_name):
        for item in self.inventory:
            if item.name.lower() == item_name:
                return True
        return False
    
    def use_item(self, item_name):
        for index, item in enumerate(self.inventory):
            if item.name.lower() == item_name.lower():
                if isinstance(item, Consumable):
                    item.use(self)

                del self.inventory[index]
                break

    def unequip_armor(self):
        # if armor is equipped, unequip it and add to inventory
        if self.equipments.armor != None:
            armor = self.equipments.armor
            self.equipments.armor = None
            self.inventory.append(armor)
            print(f"You have unequipped the armor: {armor.name}")
        else:
            print("No armor is currently equipped.")

    def unequip_weapon(self):
        # if weapon is equipped, unequip it and add to inventory
        if self.equipments.weapon != None:
            weapon = self.equipments.weapon
            self.equipments.weapon = None
            self.inventory.append(weapon)
            print(f"You have unequipped the weapon: {weapon.name}")
        else:
            print("No weapon is currently equipped.")

    def equip(self, item_name):
        for index, item in enumerate(self.inventory):
            if item.name.lower() == item_name:
                if isinstance(item, Weapon):
                    self.unequip_weapon()
                    del self.inventory[index]
                    self.equip_weapon(item)
                    print(f"You have equipped the weapon: {item.name}")
                elif isinstance(item, Armor):
                    self.unequip_armor()
                    del self.inventory[index]
                    self.equip_armor(item)
                    print(f"You have equipped the armor: {item.name}")
                else:
                    print(f"You cannot equip the item: {item.name}")
                break

    def learn_spell(self, spell):
        for i in range(len(self.spells)):
            if self.spells[i] is None:
                spell_list = list(self.spells)
                spell_list[i] = spell
                self.spells = tuple(spell_list)
                print(f"You have learned the spell: {spell.name}")
                return
        print("You cannot learn more spells. Spell slots are full.")

    def cast_spell(self, spell_name, enemy):
        for spell in self.spells:
            if spell is not None and spell_name == spell.name:
                # implement spell casting logic
                spell.cast(enemy)
        

class NonplayerCharacter(Character):
    def __init__(self, name, character_class, attributes):
        super().__init__(name, character_class, attributes)

class Spell:
    def __init__(self, name, damage_dice, mana_cost):
        self.name = name
        self.damage_dice = damage_dice
        self.mana_cost = mana_cost

    def cast(self, enemy):
        sides_per_die = int(self.damage_dice.split('d')[1]) # 2d6 -> 6
        number_of_dice = int(self.damage_dice.split('d')[0]) # 2d6 -> 2
        damage = dice_roll(sides_per_die, number_of_dice)
        enemy.current_health -= damage
        print(f"You cast {self.name} and deal {damage} damage to {enemy.name}.")

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

def encounter(player, monster):
    print(f"\n⚠️ You have encountered a {monster.name}!")
    player.start_combat()

    loot_list = [
        Armor("White Leather Armor", "leather armor"), 
        Weapon("Sword", "1d6"), 
        Weapon("Dagger", "1d4"), 
        Weapon("Staff", "1d4"), 
        Weapon("Mace", "1d6"), 
        Weapon("Axe", "1d6"),
        Consumable("Health Potion", "heal", 10),
        Consumable("Health Potion", "heal", 10),
    ] # this is a list

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
            if player.spells[0] is not None or player.spells[1] is not None or player.spells[2] is not None:
                spell_name = input("Enter the spell name to cast: ").strip()
                player.cast_spell(spell_name, monster)
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

            looted_items = loot_roll(loot_list)  # loot_roll returns a list of looted items
            loot_gold = dice_roll(number_of_dice=5, sides_per_die=4)

            print(f"The {monster.name} dropped {looted_items} and {loot_gold} golds. Congrats!")
            player.inventory.extend(looted_items) # add a list to another list
            player.gold += loot_gold # gold = gold + loot_gold
            break
        else:
            if not has_dodged: # if has_dodged == False:
                # Monster attacks back
                hit = monster.attack(player)

                print(f"The {monster.name} hits you for {hit} damage. Your health is now {player.current_health}.")

    player.end_combat()

