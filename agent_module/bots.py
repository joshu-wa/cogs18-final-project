import random

from .wander_utils import add_lists, check_bounds



class WanderBot:
    
    def __init__(self, character=8982):
        """Create a bot that will wander the board.

        Parameters
        ----------
        character : int, optional
            The unicode number for the character to represent the bot. default = 8982.
        """
        
        self.character = chr(character)
        self.position = [0,0]
        self.moves = [[-1, 0], [1, 0], [0, 1], [0, -1]]
        self.grid_size = None
        self.level = 1
        
        
    def wander(self, walls, food):
        """Move to a new location with a vision of all immediately accessible spaces.

        Parameters
        ----------
        walls : List of List of int
            The positions of wall spaces directly accessible to the bot.
        food : List of List of int
            The positions of food spaces directly accessible to the bot.
            
        Returns
        -------
        List
            The new location the bot has moved to.
        """
        
        # Set preferred moves (prioritize food, avoid walls)
        preferred_moves = []
        possible_moves = []
        for move in self.moves:
            possible_pos = add_lists(self.position, move)
            if possible_pos in food:
                preferred_moves.append(move)
            elif possible_pos not in walls and check_bounds(possible_pos, self.grid_size):
                possible_moves.append(move)
       
        if len(preferred_moves) == 0:
            if len(possible_moves) == 0:
                # If surrounded by walls (no preferred moves), stay in place
                preferred_moves.append([0, 0])
            else:
                # If no food is around, pick a random adjacent empty space
                preferred_moves = possible_moves
                
        has_new_pos = False
        while not has_new_pos:
            move = random.choice(preferred_moves)
            new_pos = add_lists(self.position, move)
            has_new_pos = check_bounds(new_pos, self.grid_size)
        return new_pos
    
    
    def move(self, walls, food):
        """Update the bot's position with its wandering movement.

        Parameters
        ----------
        walls : List of List of int
            The positions of wall spaces directly accessible to the bot.
        food : List of List of int
            The positions of food spaces directly accessible to the bot.
            
        Returns
        -------
        List
            The new location the bot has moved to.
        """
        
        self.position = self.wander(walls, food)
        return self.position
        