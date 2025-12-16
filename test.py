import unittest
from game import Armor, Consumable, PlayerCharacter, Attribute, Spell, Weapon

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
        fireball_spell = Spell("Fireball", "2d3", 120)
        player.learn_spell(fireball_spell)
        self.assertIsNotNone(player.spells[0])
        self.assertEqual(player.spells[0].name, "Fireball")
        player.cast_spell("Fireball", player)  # casting on self for test purposes

if __name__ == '__main__':
    unittest.main()