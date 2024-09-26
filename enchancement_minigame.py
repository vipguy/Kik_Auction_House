import random

class EnchantingGame:
    def __init__(self):
        self.player_enchantments = {}  # Dictionary to store each player's enchanted equipment

    def start_enchanting(self, player_id, equipment):
        # Initialize the enchanting process for the player's selected equipment
        self.player_enchantments[player_id] = {"equipment": equipment, "ingredients": []}
        return f"You begin enchanting your {equipment}. Gather the ingredients needed for the enchantment."

    def gather_ingredient(self, player_id, location):
        # Simulate gathering ingredients from a chosen location
        ingredients = {
            "forest": "magical herb",
            "cave": "crystal",
            "ruins": "ancient artifact"
        }
        ingredient = ingredients.get(location)
        if ingredient:
            self.player_enchantments[player_id]["ingredients"].append(ingredient)
            return f"You gather a {ingredient} from the {location}."
        else:
            return "You search but find nothing of use in that location."

# Example usage
game = EnchantingGame()
player_id = 1
equipment = "sword"
print(game.start_enchanting(player_id, equipment))  # Player starts enchanting their sword
location = "forest"
print(game.gather_ingredient(player_id, location))  # Player gathers a magical herb from the forest
