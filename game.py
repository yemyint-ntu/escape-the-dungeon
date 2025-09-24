import random

armor_value = {
    "none": 0,
    "cloth armor": 1,
    "leather armor": 2,
    "chainmail": 3,
    "plate armor": 4,
    "dragon scale": 5,
}
class Weapon:
    def __init__(self, name, damage_dice):
        self.name = name
        self.damage_dice = damage_dice

    def get_damage(self):
        # based on damage dice string
        result = self.damage_dice.split('d')
        num_dice = int(result[0])
        sides = int(result[1])
        return dice_roll(sides_per_die=sides, number_of_dice=num_dice)

class Armor:
    def __init__(self, name, type):
        self.name = name
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

class NonplayerCharacter(Character):
    def __init__(self, name, character_class, attributes):
        super().__init__(name, character_class, attributes)

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
