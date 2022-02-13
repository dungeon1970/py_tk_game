from window import Gui
import json
from class_files.location import Location
from class_files.puzzle import Puzzle 


locations_dict = {}
puzzle_dict = {}

# load all locations into dictionary locations_dict
with open('new_game_data/locations.json') as l:
    locations = json.load(l)
    for item, info in locations.items():
        location = Location(item, **info)
        locations_dict.update({item: location})

# load all puzzles into dictionary called puzzle_dict
with open('new_game_data/puzzles.json') as p:
    puzzles = json.load(p)
    for item, info in puzzles.items():
        puzzle = Puzzle(item, **info)
        puzzle_dict.update({item: puzzle})

# open game window
game_window = Gui("Garden", locations_dict, puzzle_dict)

