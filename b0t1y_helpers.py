
volume_map = {
    # Each volume level has a different HEX value depending on it's location in a transmission
    # EX H/High volume:  '3' is the first bit of each byte in the init block,
    #                    '0' is the first bit of each byte in the address block,
    #                    '1' is the first bit of each byte in the command block
    'H': '301',       # High
    'L': '745',       # Low
    'O': 'B89'        # Off
}

address_map = {
    # The pairing sequence uses the F, L, R, and B direction buttons to create an address.
    # Each direction button corresponds to a HEX value which is used as part of the address.
    # There are 256 possible permutations of button presses which will result in a unique address.
    # This dict makes it easy to convert between direction/HEX addresses
    'F': '2',       # Forward
    'L': '4',       # Left
    'R': '6',       # Right
    'B': '8'        # Backward
}


def convert_addr(address: str):
    """ Accepts a 4-character address string as directions like 'FLBR' or hex values like '2864'
    and returns the converted address"""
    address = address.upper()   # Make the address uppercase to reduce the number of comparisons
    allowed = 'FLRB2468'        # These are the only acceptable address characters
    converted = []

    # Notify the user if the address is not exactly four characters long
    if len(address) != 4:
        print(f'You provided {address} which is {len(address)} characters. The address must be 4 characters long.')
        return None

    # Notify the user if any unexpected characters are provided
    if not all(character in allowed for character in address):
        disallowed = [character for character in address if character not in allowed]
        print(f'You provided {address} which contains the following invalid characters:\n'
              f'{[character for character in disallowed]}\n'
              f'The address may only contain {[character for character in allowed]}')
        return None

    # If the address contains numbers we will return direction-based address
    if address.isnumeric():
        for _hex in address:
            [converted.append(key) for key, value in address_map.items() if value == _hex]

    # Otherwise, if the address contains letters we will return the hex-based address
    else:
        converted = [address_map[character] for character in address]

    return converted


def parse_direction(direction: str):
    """ Accepts a direction command and returns the corresponding binary value that is transmitted to Botley """
    direction = direction.lower()  # To minimize errors, make sure direction is always lower case

    # The "move" dictionary maps simplified commands to the binary values that will be sent to Botley
    move = {'f': ('1', 'forward'), 'b': ('2', 'backward'),
            'l90': ('3', 'left90'), 'r90': ('4', 'right90'),
            'l45': ('5', 'left45'), 'r45': ('6', 'right45')}

    # The "commands" dictionary maps similar direction inputs to their common simplified "move" commands.
    # This allows us to say botley.move('forward') or botley.move('f'); both will move Botley forward.
    commands = {'forward': move['f'], 'backward': move['b'], 'f': move['f'], 'b': move['b'],
                'left90': move['l90'], 'right90': move['r90'], 'l': move['l90'], 'r': move['r90'],
                'left45': move['l45'], 'right45': move['r45'], 'l4': move['l45'], 'r4': move['r45']}

    # Next, "commands[direction]" looks for a "key" in "commands" that matches the "direction" parameter given.
    # If the "key" is found, the corresponding "value" is returned. In this case, the return value is a "key"
    # in the "move" dictionary. Because "commands[direction]" is inside of "move[]", the return value of
    # "commands[direction]" is passed as input to "move[]". "move[]" returns a list containing the
    # corresponding binary move command and a string that we can use to label the move when we print the queue.
    command = move[commands[direction]]

    return command