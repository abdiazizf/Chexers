# Converts a JSON into a dictionary of tuples(board co-ordinates) as keys with values to be printed
# e.g {[0,2]: 'R',[0,0]:'BLK'}

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
