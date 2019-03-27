"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors: Abdiaziz Farah, Jordan Puckridge


HEX BASED IMPLEMENTATION
"""

import sys
import json

def main():
    
    
    with open(sys.argv[1]) as file:
        data = json.load(file)

    board_dict = convert_json_to_board_dict(data)
    # TODO: Search for and output winning sequence of moves
    # ...
    game_board = board(board_dict)
    
    print_board(game_board.board_state)
    
    direction = (1,0)
    old_position = game_board.board_state[0,0]
    
    new_position = game_board.get_neighbour_in_direction(direction, old_position)
    
    game_board.swap_spaces_by_hex(new_position, old_position)
        
    print_board(game_board.board_state)
    
    
class board: 
    
    # With hex based the board_state dict will contain a dictionary of hexes
    # coordinates will still be key, hex is now value
    
    # Dictionary: tuples (board coordinates) as key, current piece status as value
    board_state = {}
    axial_directions = [(1,0),(1,-1),(0,-1),(-1,0),(-1,1),(0,1)]
    
    # Return a boolean if a board position is unoccupied
    def position_occupied(self,position):
        if(self.board_state[position].occupied == True):
            return True
        else: 
            return False     
    
    def hex_direction(self,direction):
        return self.axial_directions[direction]
        
    # Returns the neighbouring hex on the game board in specified direction
    def get_neighbour_in_direction(self,direction,game_hex):
        #neighbour_dir  = self.hex_direction(direction)
        
        new_position = tuple(sum(i) for i in zip(game_hex.coordinates, direction))
        
        return self.board_state[new_position]  
        
    def valid_position(self,game_hex):
    
        position = game_hex.coordinates
        if not (position[0] in range(-3,4)):
            return False
        elif not(position[1] in range(-3,4)):
            return False
        else: return self.position_occupied(position)
        
    def swap_spaces_by_hex(self,hex1,hex2):
        tmp = self.board_state[hex1.coordinates]
        self.board_state[hex1.coordinates] = self.board_state[hex2.coordinates] 
        self.board_state[hex2.coordinates] = tmp
    
    # Generate tuples and assign initial values from board_dict
    def generate_board(self, initial_board):

        tuples = [(x, y) for x in range(-3,4) for y in range(-3,4)]
        
        
        for entry in tuples:
            self.board_state[entry] = game_hex(entry)
            self.board_state[entry].current_piece = '-'
        for entry in initial_board:
            self.board_state[entry].occupied = True
            self.board_state[entry].current_piece = initial_board[entry]
        
    def __init__(self, initial_board):
        self.generate_board(initial_board)
    
class game_hex: 
    
    # Could possibly define a game board as a collection of hexes. 
    # Each hex has a co-ordinate 
    
    coordinates = None
    
    occupied = None
    
    current_piece = None
     
    
    def __init__(self,coordinate):
        self.coordinates = coordinate
    
    
class piece:
    
    colour = 'default'
    cur_position = ()
    

    def update_position(self, new_position):
        self.cur_positon = new_position
    
    def __init__(self,colour):
        self.colour = colour
        


def convert_json_to_board_dict(file):
    
    
    # Reads colour from the JSON, compares it to a dictionary of values and 
    # sets the correct symbol 
    colour_dict = {'red' : 'R','blue': 'B','green':'G'}
    player_colour = colour_dict[file['colour']]
    
    # Creates an empty dict and constructs an entry for each tuple in JSON, using
    # predetermined player colour for player pieces and a block otherwise
    board_dict = {}
    
    for coordinate in file['pieces']:
        board_dict[tuple(coordinate)] = player_colour
    for coordinate in file['blocks']:
        board_dict[tuple(coordinate)] = 'BLK'
    
    #return dict 
    return board_dict



def print_board(board_dict, message="", debug=False, **kwargs):
    """
    Helper function to print a drawing of a hexagonal board's contents.
    
    Arguments:

    * `board_dict` -- dictionary with tuples for keys and anything printable
    for values. The tuple keys are interpreted as hexagonal coordinates (using 
    the axial coordinate system outlined in the project specification) and the 
    values are formatted as strings and placed in the drawing at the corres- 
    ponding location (only the first 5 characters of each string are used, to 
    keep the drawings small). Coordinates with missing values are left blank.

    Keyword arguments:

    * `message` -- an optional message to include on the first line of the 
    drawing (above the board) -- default `""` (resulting in a blank message).
    * `debug` -- for a larger board drawing that includes the coordinates 
    inside each hex, set this to `True` -- default `False`.
    * Or, any other keyword arguments! They will be forwarded to `print()`.
    """

    # Set up the board template:
    if not debug:
        # Use the normal board template (smaller, not showing coordinates)
        template = """# {0}
#           .-'-._.-'-._.-'-._.-'-.
#          |{16:}|{23:}|{29:}|{34:}| 
#        .-'-._.-'-._.-'-._.-'-._.-'-.
#       |{10:}|{17:}|{24:}|{30:}|{35:}| 
#     .-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
#    |{05:}|{11:}|{18:}|{25:}|{31:}|{36:}| 
#  .-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
# |{01:}|{06:}|{12:}|{19:}|{26:}|{32:}|{37:}| 
# '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#    |{02:}|{07:}|{13:}|{20:}|{27:}|{33:}| 
#    '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#       |{03:}|{08:}|{14:}|{21:}|{28:}| 
#       '-._.-'-._.-'-._.-'-._.-'-._.-'
#          |{04:}|{09:}|{15:}|{22:}|
#          '-._.-'-._.-'-._.-'-._.-'"""
    else:
        # Use the debug board template (larger, showing coordinates)
        template = """# {0}
#              ,-' `-._,-' `-._,-' `-._,-' `-.
#             | {16:} | {23:} | {29:} | {34:} | 
#             |  0,-3 |  1,-3 |  2,-3 |  3,-3 |
#          ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
#         | {10:} | {17:} | {24:} | {30:} | {35:} |
#         | -1,-2 |  0,-2 |  1,-2 |  2,-2 |  3,-2 |
#      ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-. 
#     | {05:} | {11:} | {18:} | {25:} | {31:} | {36:} |
#     | -2,-1 | -1,-1 |  0,-1 |  1,-1 |  2,-1 |  3,-1 |
#  ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
# | {01:} | {06:} | {12:} | {19:} | {26:} | {32:} | {37:} |
# | -3, 0 | -2, 0 | -1, 0 |  0, 0 |  1, 0 |  2, 0 |  3, 0 |
#  `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' 
#     | {02:} | {07:} | {13:} | {20:} | {27:} | {33:} |
#     | -3, 1 | -2, 1 | -1, 1 |  0, 1 |  1, 1 |  2, 1 |
#      `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' 
#         | {03:} | {08:} | {14:} | {21:} | {28:} |
#         | -3, 2 | -2, 2 | -1, 2 |  0, 2 |  1, 2 | key:
#          `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' ,-' `-.
#             | {04:} | {09:} | {15:} | {22:} |   | input |
#             | -3, 3 | -2, 3 | -1, 3 |  0, 3 |   |  q, r |
#              `-._,-' `-._,-' `-._,-' `-._,-'     `-._,-'"""

    # prepare the provided board contents as strings, formatted to size.
    ran = range(-3, +3+1)
    cells = []
    for qr in [(q,r) for q in ran for r in ran if -q-r in ran]:
        if qr in board_dict:
            cell = str(board_dict[qr].current_piece).center(5)
        else:
            cell = "     " # 5 spaces will fill a cell
        cells.append(cell)

    # fill in the template to create the board drawing, then print!
    board = template.format(message, *cells)
    print(board, **kwargs)


# when this module is executed, run the `main` function:


if __name__ == '__main__':
    main()
