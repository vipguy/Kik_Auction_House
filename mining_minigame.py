import random

class MiningGame:
    def __init__(self):
        self.player_positions = {}  # Dictionary to store each player's current position in the mine
        self.player_energy = {}  # Dictionary to store each player's energy level
        self.player_loot = {}  # Dictionary to store each player's loot


    def start_mining(self, player_id):
        # Initialize the player's position in the mine (e.g., start at the entrance)
        self.player_positions[player_id] = 0
        self.player_energy[player_id] = 50
        self.player_loot[player_id] = {
            "iron ore": 0,
            "gold": 0,
            "gemstone": 0
        }

        return "You enter the mine. Which direction will you choose? (left/right/center)"

    def mine(self, player_id, direction):
        if self.player_energy[player_id] <= 2:
            return self.player_loot[player_id], "end"
        self.player_positions[player_id] += 1  # Increment the player's position in the mine
        self.player_energy[player_id] -= 3  # Deduct energy for mining
        # Simulate mining based on the player's chosen direction
        if self.player_positions[player_id] < 10:
            # Modify the weights to change the odds
            weights = {
                'left':{
                    "iron ore": 40.00,  # 80% chance
                    "gold": 10.00,      # 50% chance
                    "nothing": 50.00    # 20% chance
                },
                'right':{
                    "gemstone": 30.00,  # 30% chance
                    "nothing": 70.00    # 20% chance
                },
                'center':{

                    "gemstone": 20.00,   # 10% chance
                    "gold": 20.00,      # 50% chance
                    "nothing": 40.00,    # 20% chance
                    "iron ore": 20.00  # 80% chance
                }

            }

        elif self.player_positions[player_id] < 20:
            # Modify the weights to change the odds
            weights = {
                'left':{
                    "iron ore": 40.00,  # 80% chance
                    "gold": 10.00,      # 50% chance
                    "nothing": 50.00    # 20% chance
                },
                'right':{
                    "gemstone": 30.00,  # 30% chance
                    "nothing": 70.00    # 20% chance
                },
                'center':{

                    "gemstone": 20.00,   # 10% chance
                    "gold": 20.00,      # 50% chance
                    "nothing": 40.00,    # 20% chance
                    "iron ore": 20.00  # 80% chance
                }

            }

        elif self.player_positions[player_id] < 30:
            # Modify the weights to change the odds
            weights = {
                'left':{
                    "iron ore": 40.00,  # 80% chance
                    "gold": 10.00,      # 50% chance
                    "nothing": 50.00    # 20% chance
                },
                'right':{
                    "gemstone": 30.00,  # 30% chance
                    "nothing": 70.00    # 20% chance
                },
                'center':{

                    "gemstone": 20.00,   # 10% chance
                    "gold": 20.00,      # 50% chance
                    "nothing": 40.00,    # 20% chance
                    "iron ore": 20.00  # 80% chance
                }

            }

        elif self.player_positions[player_id] < 40:
            # Modify the weights to change the odds
            weights = {
                'left':{
                    "iron ore": 40.00,  # 80% chance
                    "gold": 10.00,      # 50% chance
                    "nothing": 50.00    # 20% chance
                },
                'right':{
                    "gemstone": 30.00,  # 30% chance
                    "nothing": 70.00    # 20% chance
                },
                'center':{

                    "gemstone": 20.00,   # 10% chance
                    "gold": 20.00,      # 50% chance
                    "nothing": 40.00,    # 20% chance
                    "iron ore": 20.00  # 80% chance
                }

            }

        elif self.player_positions[player_id] < 50:
            # Modify the weights to change the odds
            weights = {
                'left':{
                    "iron ore": 40.00,  # 80% chance
                    "gold": 10.00,      # 50% chance
                    "nothing": 50.00    # 20% chance
                },
                'right':{
                    "gemstone": 30.00,  # 30% chance
                    "nothing": 70.00    # 20% chance
                },
                'center':{

                    "gemstone": 20.00,   # 10% chance
                    "gold": 20.00,      # 50% chance
                    "nothing": 40.00,    # 20% chance
                    "iron ore": 20.00  # 80% chance
                }

            }

        elif self.player_positions[player_id] < 60:
            # Modify the weights to change the odds
            weights = {
                'left':{
                    "iron ore": 40.00,  # 80% chance
                    "gold": 10.00,      # 50% chance
                    "nothing": 50.00    # 20% chance
                },
                'right':{
                    "gemstone": 30.00,  # 30% chance
                    "nothing": 70.00    # 20% chance
                },
                'center':{

                    "gemstone": 20.00,   # 10% chance
                    "gold": 20.00,      # 50% chance
                    "nothing": 40.00,    # 20% chance
                    "iron ore": 20.00  # 80% chance
                }

            }
        
        # Simulate the outcome of mining based on the chosen direction
        outcome = random.choices(list(weights[direction].keys()), weights=list(weights[direction].values()))[0]
        if outcome == "nothing":
            return f"You mine {direction}, find {outcome}, you have {self.player_energy[player_id]} energy left. mine depth is {self.player_positions[player_id]}"
        elif outcome == "end":
            return self.player_loot[player_id], "end"
        else:
            self.player_loot[player_id][outcome] += 1
            return f"You mine {direction}, find {outcome}, you have {self.player_energy[player_id]} energy left. mine depth is {self.player_positions[player_id]}"

# Function to play the game in the terminal
def play_game():
    game = MiningGame()
    player_id = 'me'
    print(game.start_mining(player_id))  # Player enters the mine
    choices = ['left', 'right', 'center']
    while True:
        decision = random.choice(choices)
        print(f"Player mines in the {decision} tunnel")
        if not decision == 'exit':
            material_found = game.mine(player_id, decision)  # Player mines in the chosen tunnel
            if material_found[1] == "end":
                print(material_found[0])
                break
            print(material_found)
        elif decision == 'nothing':
            print("You found nothing")
            continue
        else:
            break

# Play the game
play_game()

