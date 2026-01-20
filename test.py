import unittest
from game import Armor, Consumable, NonplayerCharacter, PlayerCharacter, Attribute, Skill, Spell, Weapon

class TestPlayerCharacter(unittest.TestCase):
    def test_create_new_player_character(self):
        attr = Attribute(3, 5, 7)
        player = PlayerCharacter("Aria", "Mage", attr)
        self.assertEqual(player.name, "Aria")
        self.assertEqual(player.character_class, "Mage")
        self.assertEqual(player.attributes.strength, 3)
        self.assertEqual(player.attributes.agility, 5)
        self.assertEqual(player.attributes.mind, 7)

    def test_player_use_health_potion(self):
        attr = Attribute(3, 5, 7)
        player = PlayerCharacter("Borin", "Warrior", attr)
        print(f"max health: {player.max_health}")

        # ensure player health increases when using a health potion
        player.current_health = 1 # Simulate damage
        potion = Consumable("Health Potion", "heal", 10)
        player.inventory.append(potion)
        player.use_item("Health Potion")
        self.assertEqual(player.current_health, 11)  # 1 + 10 from potion

        # ensure health does not exceed max health
        player.current_health = player.max_health - 5
        potion2 = Consumable("Health Potion", "heal", 10)
        player.inventory.append(potion2)
        player.use_item("Health Potion")
        self.assertEqual(player.current_health, player.max_health)  # should not exceed max health

    def test_player_equip_weapon(self):
        attr = Attribute(4, 4, 4)
        player = PlayerCharacter("Cora", "Rogue", attr)
        weapon = Weapon("Short Sword", "1d6")
        player.equip_weapon(weapon)
        print(f"Equipped weapon: {player.equipments.weapon}")
        self.assertEqual(player.equipments.weapon.name, "Short Sword")
    
    def test_player_equip_armor(self):
        attr = Attribute(4, 4, 4)
        player = PlayerCharacter("Dain", "Warrior", attr)
        armor = Armor("Silver Chainmail", "chainmail")
        player.equip_armor(armor)
        print(f"Equipped armor: {player.equipments.armor}")
        self.assertEqual(player.equipments.armor.name, "Silver Chainmail")

    def test_player_unequip_weapon(self):
        attr = Attribute(4, 4, 4)
        player = PlayerCharacter("Eira", "Rogue", attr)
        weapon = Weapon("Long Bow", "1d8")
        player.equip(weapon)
        print(f"Equipped weapon: {player.equipments.weapon}")
        player.unequip_weapon()
        self.assertIsNone(player.equipments.weapon)

    def test_player_unequip_weapon_error_case(self):
        attr = Attribute(4, 4, 4)
        player = PlayerCharacter("Finn", "Rogue", attr)
        # print(f"Player's inventory before unequip attempt: {player.inventory}")
        weapon = Weapon("Dagger", "1d4")
        # try to unequip a weapon that is not equipped
        player.unequip_weapon()
        # print(f"Player's inventory after unequip attempt: {player.inventory}")
        self.assertListEqual(player.inventory, [])  # inventory should remain empty

    def test_spell(self):
        attr = Attribute(2, 4, 8)
        player = PlayerCharacter("Gwen", "Mage", attr)
        fireball_spell = Spell("Fireball", "2d4", 120)
        player.learn_spell(fireball_spell)
        self.assertIsNotNone(player.spells[0])
        self.assertEqual(player.spells[0].name, "Fireball")
        player.cast_spell("Fireball", player)  # casting on self for test purposes

    def test_mage_encounter(self):
        # create a mage player
        attr = Attribute(2, 4, 8)
        player = PlayerCharacter("Hale", "Mage", attr)
        player.equip_armor(Armor("Cloth Armor", "cloth armor"))   
        player.equip_weapon(Weapon("Wooden Staff", "1d5"))
        fireball_spell = Spell("Fireball", "2d10", 120)
        
        player.learn_spell(fireball_spell)
        print(f"Player spells: {[spell.name for spell in player.spells if spell is not None]}")

        # create a monster
        goblin_monster = NonplayerCharacter("goblin", "Beast", Attribute(3, 4, 0))
        goblin_monster.equip_armor(Armor("leather armor", "leather armor"))
        goblin_monster.equip_weapon(Weapon("club", "1d6"))

        # simulate encounter
        while goblin_monster.current_health > 0 and player.current_health > 0:
            # player casts spell
            player.cast_spell("Fireball", goblin_monster)
            if goblin_monster.current_health <= 0:
                break
            # monster attacks
            hit = goblin_monster.attack(player)
            print(f"{goblin_monster.name} attacks player for {hit} damage.")

        if goblin_monster.current_health <= 0:
            print("Goblin defeated!")
        else:
            print("Player defeated!")

    def test_skill_use(self):
        attr = Attribute(4, 8, 2)
        player = PlayerCharacter("Iris", "Rogue", attr)
        
        backstab_skill = Skill("Backstab", "3d6", 200)
        player.learn_skill(backstab_skill)
        self.assertIsNotNone(player.skills[0])
        self.assertEqual(player.skills[0].name, "Backstab")
        
        goblin_monster = NonplayerCharacter("goblin", "Beast", Attribute(3, 4, 0))
        goblin_monster.equip_armor(Armor("leather armor", "leather armor"))
        goblin_monster.equip_weapon(Weapon("club", "1d6"))
        
        # simulate encounter
        while goblin_monster.current_health > 0 and player.current_health > 0:
            # player uses skill
            player.use_skill("Backstab", goblin_monster)
            if goblin_monster.current_health <= 0:
                break
            # monster attacks
            hit = goblin_monster.attack(player)
            print(f"{goblin_monster.name} attacks player for {hit} damage.")

        if goblin_monster.current_health <= 0:
            print("Goblin defeated!")
        else:
            print("Player defeated!")

if __name__ == '__main__':
    unittest.main()