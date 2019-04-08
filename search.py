
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
    pieces, target = create_piece_and_target_list(board_dict)

    a = search(board_dict,pieces,target)
    print_board(a.state)

#Class for every node state
class State :
    def __init__(self,state,pieces,parent,cost,action,target):
       self.state = state
       self.pieces = pieces
       self.parent = parent
       self.cost = cost
       self.action = action
       self.target = target

    #prints object as a board and not memory location of object
    def __str__(self):
        return str(print_board(self.state))


    def __hash__(self):
        my_tuple = self.state
        return hash(my_tuple)

    def __eq__(self, other):
        return (self.state, self.pieces, self.parent) == (other.state, other.pieces, other.parent)
    def __lt__(self,other):
        return self.cost< other.cost

    def successor_board_states(self):
        legal_moves = []
        successor_states = []
        for i in axial_directions:
            potential_moves = (self.pieces[0][0]+i[0], self.pieces[0][1]+i[1])
            if potential_moves not in self.state or self.state[potential_moves] is not None:
                continue
            legal_moves.append(potential_moves)

        for i in axial_jump :
            potential_jump = (self.pieces[0][0] + i[0], self.pieces[0][1] + i[1])
            if potential_jump not in self.state or self.state[potential_jump] is not None:
                continue
            elif self.state[(potential_jump[0] - (i[0]/2), potential_jump[1] - (i[1] / 2))] is not None:
                legal_moves.append(potential_jump)
            else:
                continue

        for each in legal_moves:
            action = (each[0] - self.pieces[0][0], each[1] - self.pieces[0][1])
            new_state = copy.deepcopy(self.state)
            new_piece = copy.deepcopy(self.pieces)
            temp = new_state[each]
            new_state[each]= new_state[new_piece[0]]
            new_state[new_piece[0]] = temp
            new_piece[0] = each

            state = State(new_state,new_piece,self,self.cost + 1 ,action,self.target)
            successor_states.append(state)

        return successor_states

def same_sign(q , r) :
    if q < 0 and r < 0 :
        return (q < 0 and r < 0)or (q>=0 and r>= 0)


def heuristic(target, source):
    heuristic_list= []
    for goal in target:
        distance_x = goal[0] - source[0]
        distance_y = goal[1] - source[1]
        if same_sign(distance_x, distance_y):
            heuristic_list.append(abs(distance_x + distance_y))
        else:
            heuristic_list.append(max(abs(distance_x), abs(distance_y)))

    return min(heuristic_list)




def search(initial_state, pieces , target) :
    initial_state = State(initial_state,pieces,None,0,None,target)
    queue = Q.PriorityQueue()
    queue.put(initial_state, initial_state.cost)
    cost_so_far = {}
    cost_so_far[tuple(initial_state.state.items())] = initial_state.cost
    while not queue.empty():
        current_node = queue.get()
        if current_node.pieces[0] in current_node.target:
            break
        for successor in current_node.successor_board_states():
            new_cost = successor.cost
            if tuple(successor.state.items()) not in cost_so_far or new_cost < cost_so_far[tuple(successor.state.items())]:
                cost_so_far[tuple(successor.state.items())] = new_cost
                priority = new_cost + heuristic(initial_state.target , successor.pieces[0])
                queue.put(successor, priority)
    return current_node


def convert_json_to_board_dict(file):
    # Reads colour from the JSON, compares it to a dictionary of values and
    # sets the correct symbol
    colour_dict = {'red' : 'R','blue': 'B','green':'G'}
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

def create_piece_and_target_list(board_dict):
    pieces = []
    for entry in board_dict:
        if board_dict[entry] in goal:
            pieces.append(entry)
            target = goal[board_dict[entry]]
        return pieces, target


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
