import unittest
from game import Consumable, Character, PlayerCharacter, Attribute

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


if __name__ == '__main__':
    unittest.main()