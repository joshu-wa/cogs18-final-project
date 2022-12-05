import random

from .wander_utils import add_lists, check_bounds
from .bots import WanderBot
from time import sleep
from IPython.display import clear_output



class GridBoard:
    
    # Symbols for grid spaces (should not be used for bot characters)
    EMPTY = '.'
    WALL = 'x'
    FOOD = 'o'
    
    
    def __init__(self, grid_size = 5, num_walls = 0, num_food = 1, custom_grid_list = None):
        """Create a grid to run bots on.

        Parameters
        ----------
        grid_size : int, optional
            Length of each side of the grid. default = 5.
        num_walls : int, optional
            Number of walls to generate on the grid. default = 0.
        num_food : int, optional
            Number of food spaces to generate on the grid. default = 1.
        custom_grid_list : List, optional
            A preset, specified grid to run on rather than a randomly generated one. default = None.
        """
        
        
        if custom_grid_list is not None:
            # Set the grid list to the given preset if provided
            self.grid_size = len(custom_grid_list)
            self.grid_list = custom_grid_list
        else:
            # Otherwise, randomly generate a grid
            self.grid_size = grid_size
            
            # Create the grid
            self.grid_list = [[GridBoard.EMPTY] * self.grid_size for ncols in range(self.grid_size)]

            # Add the walls
            for i in range(num_walls):
                position_set = False
                while not position_set:
                    position = [random.randrange(self.grid_size),
                                    random.randrange(self.grid_size)]
                    # Only add to empty spaces
                    if self.grid_list[position[0]][position[1]] == GridBoard.EMPTY:
                        self.grid_list[position[0]][position[1]] = GridBoard.WALL
                        position_set = True
            
            # Add the food
            for i in range(num_food):
                position_set = False
                while not position_set:
                    position = [random.randrange(self.grid_size),
                                    random.randrange(self.grid_size)]
                    # Only add to empty spaces
                    if self.grid_list[position[0]][position[1]] == GridBoard.EMPTY:
                        self.grid_list[position[0]][position[1]] = GridBoard.FOOD
                        position_set = True
       
    
    def clear_grid(self):
        """Clear the grid of all bot characters.
        """
        
        # Empty grid (without bots) to use when clearing the grid each iteration
        for row in range(len(self.grid_list)):
            for column in range(len(self.grid_list[row])):
                if self.grid_list[row][column] not in [GridBoard.EMPTY,
                                                       GridBoard.WALL,
                                                       GridBoard.FOOD]:
                    self.grid_list[row][column] = GridBoard.EMPTY
       
    
    def add_food(self, num_food = 1):
        """Add food spaces to the grid.

        Parameters
        ----------
        num_food : int, optional
            Number of food spaces to add. default = 1.
        """
        
        # Same as the version in __init__()
        for i in range(num_food):
            position_set = False
            while not position_set:
                position = [random.randrange(self.grid_size),
                                random.randrange(self.grid_size)]
                # Only add to empty spaces
                if self.grid_list[position[0]][position[1]] == GridBoard.EMPTY:
                    self.grid_list[position[0]][position[1]] = GridBoard.FOOD
                    position_set = True
        
    
    def play_board(self, bots, n_iter = 25, sleep_time = 0.3, restock_rate = 5, restock_amount = 1):
        """Run a bot or list of bots across a board.

        Parameters
        ----------
        bots : Bot() type or list of Bot() type
            One or more bots to be be played on the board
        n_iter : int, optional
            Number of turns to play on the board. default = 25.
        sleep_time : float, optional
            Amount of time to pause between turns. default = 0.3.
        restock_rate : int, optional
            Number of turns before more food is added, 0 to never restock. default = 0.
        restock_amount : int, optional
            Number of food spaces to add per restock. default = 1.
        """
        
        # Keep track of bot objects and their characters using a dict (no duplicates allowed)
        bots_dict = {}

        # If input is a single bot, put it in a list so that procedures work
        if not type(bots) == list:
            bots_dict[bots.character] = bots
        else:
            for bot in bots:
                bots_dict[bot.character] = bot

        # Update each bot to know about the grid_size they are on
        # Additionally, randomize their spawn locations to a valid (empty) space
        for bot in bots_dict.values():
            bot.grid_size = self.grid_size
            
            position_set = False
            while not position_set:
                bot.position = [random.randrange(self.grid_size),
                                random.randrange(self.grid_size)]
                # Only add to empty spaces
                if self.grid_list[bot.position[0]][bot.position[1]] == GridBoard.EMPTY:
                    self.grid_list[bot.position[0]][bot.position[1]] = bot.character
                    position_set = True

        # Begin iterating and moving bots
        for it in range(n_iter):

            # Clear the grid
            self.clear_grid()

            # Add bot(s) to the grid
            for bot in bots_dict.values():
                self.grid_list[bot.position[0]][bot.position[1]] = bot.character    
                
            # Restock food if necessary
            if restock_rate != 0 and (it + 1) % restock_rate == 0:
                self.add_food(restock_amount)

            # Clear the previous iteration, print the new grid (as a string), and wait
            clear_output(True)
            print('\n'.join([' '.join(lst) for lst in self.grid_list]))
            sleep(sleep_time)

            # Update bot states for next turn
            eaten_bots = []
            for bot in bots_dict.values():
                if bot.character not in eaten_bots: # skip the bot if it has been eaten
                    
                    # Inform the bot of the what kind of spaces it may try to move to (vision)
                    walls = []
                    food = []
                    for move in bot.moves:
                        next_pos = add_lists(bot.position, move)
                        if check_bounds(next_pos, self.grid_size):
                            next_space = self.grid_list[next_pos[0]][next_pos[1]]
                            if next_space == GridBoard.WALL: # cannot move into wall space
                                walls.append(next_pos)
                            elif next_space == GridBoard.FOOD: # prioritize moving to food space
                                food.append(next_pos)
                            elif next_space in bots_dict.keys(): # another bot is in the space
                                # Treat bots of equal level as walls
                                if bot.level == bots_dict[next_space].level:
                                    walls.append(next_pos)

                    # Remove bot from previous position (preparing for move)
                    self.grid_list[bot.position[0]][bot.position[1]] = GridBoard.EMPTY
                    new_pos = bot.move(walls, food)
                    new_space = self.grid_list[new_pos[0]][new_pos[1]]
                    # 'Take over' the space so other bots see an updated result during the iteration
                    self.grid_list[new_pos[0]][new_pos[1]] = bot.character

                    # Landing on a food space increments the level of the bot
                    if new_space == GridBoard.FOOD:
                        bot.level += 1
                        self.grid_list[new_pos[0]][new_pos[1]] = bot.character

                    # Bots on the same space will try to 'eat' each other
                    # Higher level bot 'eats' the other bot (takes their levels and removes them)
                    # If levels are equal, bots will not move into each other (like walls)
                    elif new_space in bots_dict.keys():
                        if bot.level > bots_dict[new_space].level:
                            bot.level += bots_dict[new_space].level
                            eaten_bots.append(new_space)
                        elif bot.level < bots_dict[new_space].level:
                            bots_dict[new_space].level += bot.level
                            eaten_bots.append(bot.character)
                            # Restore previous bot back to position (since it ate the current bot)
                            self.grid_list[new_pos[0]][new_pos[1]] = new_space
            
            # Remove all eaten bots in the iteration from the game
            for bot_char in eaten_bots:
                bots_dict.pop(bot_char, None)
           
        # Print all remaining bots and their levels
        print('Final Survivors:\n' +
              '\n'.join([bot_char + ': level ' + str(bot.level)
                         for bot_char, bot in bots_dict.items()]))
                    