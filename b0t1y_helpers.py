
def parse_direction(direction: str):
    # Accepts a direction command and returns the corresponding binary value that is transmitted to Botley.
    direction = direction.lower()  # To minimize errors, make sure direction is always lower case

    # The "move" dictionary maps simplified commands to the binary values that will be sent to Botley
    move = {'f': ('1', 'forward'), 'b': ('2', 'backward'),
            'l90': ('3', 'left90'), 'r90': ('4', 'right90'),
            'l45': ('5', 'left45'), 'r45': ('6', 'right45')}

    # The "commands" dictionary maps similar direction inputs to their common simplified "move" commands.
    # This allows us to say botley.move('forward') or botley.move('f'); both will move Botley forward.
    commands = {'forward': move['f'], 'backward': move['b'], 'f': move['f'], 'b': move['b'],
                'left90': move['l90'], 'right90': move['r90'], 'l90': move['l90'], 'r90': move['r90'],
                'left45': move['l45'], 'right45': move['r45'], 'l45': move['l45'], 'r45': move['r45']}

    # Next, "commands[direction]" looks for a "key" in "commands" that matches the "direction" parameter given.
    # If the "key" is found, the corresponding "value" is returned. In this case, the return value is a "key"
    # in the "move" dictionary. Because "commands[direction]" is inside of "move[]", the return value of
    # "commands[direction]" is passed as input to "move[]". "move[]" returns a list containing the
    # corresponding binary move command and a string that we can use to label the move when we print the queue.
    command = move[commands[direction]]

    return command