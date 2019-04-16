"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors: Abdiaziz Farah, Jordan Puckridge


HEX BASED IMPLEMENTATION
"""

import sys
import json
import copy
import queue as Q

# TODO: Implement a move function for board to check for a valid move and then swap pieces
# Also needs to print the specified output according to the project spec

# TODO: Implement a distance function to calculate how far it is from a hex to
# the nearest goal space, to use in a heuristic evaluation

# TODO: Implement search algorithm that finds optimal solution and records
# the sequence of moves

#possible moves
axial_directions = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
axial_jump = [(2, 0), (2, -2), (0, -2), (-2, 0), (-2, 2), (0, 2)]
#goal for each colour
goal = {'R': [(3, -3), (3,-2) , (3,-1) , (3, 0)] , 'B':[(0, -3), (-1,-2) , (-2,-1) , (-3, 0)] , 'G' :[(-3, 3), (-2, 3) , (-1, 3) , (0, 3)]}

def main():

    with open(sys.argv[1]) as file:
        data = json.load(file)

    board_dict = convert_json_to_board_dict(data)
    print_board(board_dict)
    # TODO: Search for and output winning sequence of moves
    # ...


class State :
    def __init__(self,state,pieces,move, parent):
       self.state = state
       self.pieces = move
       self.parent = parent
       self.heuristic = heuristic(parent.targets, self.pieces)

    #prints object as a board and not memory location of object
    def __str__(self):
        return str(print_board(self.state))

    def __eq__(self, other):
        return self.state == other.state

class Board:
    # With hex based the board_state dict will contain a dictionary of hexes
    # coordinates will still be key, hex is now value
    # Dictionary: tuples (board coordinates) as key, current piece status as value
    state = {}
    pieces = []
    goal_state = []
    targets = []
    heuristic_list = []

    def __init__(self, initial_board):
        self.number_moves = 0
        self.state = initial_board
        self.parent = None
        for entry in initial_board:
            if initial_board[entry] in goal:
                self.pieces.append(entry)
                self.targets = goal[initial_board[entry]]
            self.heuristic= heuristic(self.targets, self.pieces)

    def successor_board_states(self):
        legal_moves = {}
        successor_states = []
        for piece in self.pieces:
            legal_moves[piece] = []
            for i in axial_directions:
                potential_moves = (piece[0]+i[0], piece[1]+i[1])
                if potential_moves not in self.state or self.state[potential_moves] is not None:
                    continue
                legal_moves[piece].append(potential_moves)
            for i in axial_jump :
                potential_jump = (piece[0] + i[0], piece[1] + i[1])
                if potential_jump not in self.state or self.state[potential_jump] is not None:
                    continue
                elif self.state[(potential_jump[0] - (i[0]/2), potential_jump[1] - (i[1] / 2))] is not None:
                    legal_moves[piece].append(potential_jump)
                else:
                    continue

        for each, value in legal_moves.items():
            for move in value :
                new_state = State(copy.deepcopy(self.state), copy.deepcopy(self.pieces), move, self)
                temp = new_state.state[each]
                new_state.state[each] = new_state[value]
                new_state[value] = temp
                successor_states.append(new_state)

        return successor_states


def same_sign(q, r):
    return (q < 0 and r < 0) or (q >= 0 and r >= 0)


def heuristic(target, source):
    heuristics = 0

    for each in source :
        to_target = []
        for every in target :
            distance_x = every[0] - each[0]
            distance_y = every[1] - each[1]
            if same_sign(distance_x, distance_y):
                to_target.append(abs(distance_x + distance_y))
            else:
                to_target.append(max(abs(distance_x), abs(distance_y)))
        heuristics += min(to_target)

    return heuristics


def search(initial_state):

    queue = Q.PriorityQueue()
    queue.put(initial_state, 0)
    while not queue.empty():
        current_node = queue.get()
        current_state = current_node.state()
        if current_node.piece[0] in initial_state.target:
            break
        for successor in current_node.successor_board_states():

            if successor not in cost_so_far or new_cost < cost_so_far[successor]:
                cost_so_far[successor] = new_cost
                priority = new_cost + heuristic(initial_state.target[0], successor.piece)
                queue.put(successor, priority)
                came_from[successor] = current_state

    return came_from


def convert_json_to_board_dict(file):
    # Reads colour from the JSON, compares it to a dictionary of values and
    # sets the correct symbol
    colour_dict = {'red' : 'R', 'blue': 'B', 'green': 'G'}
    player_colour = colour_dict[file['colour']]
    coordinates = [(q, r) for q in range(-3, 4) for r in range(-3, 4) if -q - r in range(-3, 4)]
    # Creates an empty dict and constructs an entry for each tuple in JSON, using
    # predetermined player colour for player pieces and a block otherwise
    board_dict = {}

    for coordinate in file['pieces']:
        board_dict[tuple(coordinate)] = player_colour
    for coordinate in file['blocks']:
        board_dict[tuple(coordinate)] = 'BLK'
    for coordinate in coordinates :
        if coordinate not in board_dict:
            board_dict[coordinate]= None

    # return dict

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
    ran = range(-3, +3 + 1)
    cells = []
    for qr in [(q, r) for q in ran for r in ran if -q - r in ran]:
        if qr in board_dict:
            cell = str(board_dict[qr]).center(5)
        else:
            cell = "     "  # 5 spaces will fill a cell
        cells.append(cell)

    # fill in the template to create the board drawing, then print!
    board = template.format(message, *cells)
    print(board, **kwargs)


# when this module is executed, run the `main` function:


if __name__ == '__main__':
    main()