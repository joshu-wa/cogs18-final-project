#!/usr/bin/python

from .grid import GridBoard
from .bots import WanderBot


def test_food_pref():
    
    bots_list = [WanderBot(ord('1'))]
    test_grid = [['.', 'x'],
                 ['o', 'x']]
    
    grid = GridBoard(custom_grid_list=test_grid)
    grid.play_board(bots=bots_list, n_iter=1)
    
    assert bots_list[0].position == [1, 0]

    
def test_wall():
    
    bots_list = [WanderBot(ord('1'))]
    test_grid = [['.', 'x'],
                 ['x', 'x']]
    
    grid = GridBoard(custom_grid_list=test_grid)
    grid.play_board(bots=bots_list, n_iter=1)
    
    assert bots_list[0].position == [0, 0]
    
    
def test_add_food():
    
    test_grid = [['.', 'x'],
                 ['x', 'o']]
    exp_grid = [['o', 'x'],
                ['x', 'o']]
    
    grid = GridBoard(custom_grid_list=test_grid)
    grid.add_food(num_food=1)
    
    assert grid.grid_list == exp_grid
    
    
def test_clear_grid():
    
    test_grid = [['1', 'o'],
                 ['x', '2']]
    exp_grid = [['.', 'o'],
                ['x', '.']]
    
    grid = GridBoard(custom_grid_list=test_grid)
    grid.clear_grid()
    
    assert grid.grid_list == exp_grid
    
    
def test_eat_bot():
    
    bots_list = [WanderBot(ord('1')),
                 WanderBot(ord('2'))]
    bots_list[0].level = 5
    test_grid = [['.', '.'],
                 ['x', 'x']]
    
    grid = GridBoard(custom_grid_list=test_grid)
    grid.play_board(bots=bots_list, n_iter=1)
    
    assert bots_list[0].level == 6
    
    
def test_no_eat_bot():
    
    bots_list = [WanderBot(ord('1')),
                 WanderBot(ord('2'))]
    test_grid = [['.', '.'],
                 ['x', 'x']]
    
    grid = GridBoard(custom_grid_list=test_grid)
    grid.play_board(bots=bots_list, n_iter=1)
    
    assert bots_list[0].level == 1 and bots_list[1].level == 1
    