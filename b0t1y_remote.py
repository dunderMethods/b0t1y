

class B0t1yRemote:

    def __init__(self, channel=1, mode='queue'):
        self.channel = channel              # Up to 4 Botleys can be used at once so there are 4 channels
        self.mode = mode                    # If mode='interactive' then commands are transmitted instantly.
        self.queue_limit = 150              # Botley can store up to 150 commands
        self.queue = []                     # The command queue stores the list of user's commands
        self.interactive_queue = []         # The interactive queue stores the list of user's commands

    def pair(self):
        # Method to pair with a botley device
        pass

    def switch_mode(self):
        # Call this method to toggle between 'queue' and 'interactive' modes.
        self.mode = 'queue' if self.mode == 'interactive' else 'queue'
        # Print a message to let the user know what mode we are in
        print(f'Switched to {self.mode.capitalize()} mode')

    def add_to_queue(self, command: list, times: int):
        for i in range(times):
            if len(self.queue) >= self.queue_limit:
                print(f'Error: Queue limit of {self.queue_limit} commands has been reached!\n'
                      f'{command[1].capitalize()} could not be added to the queue.')
                break
            else:
                self.queue.append(command)
                print(f'{command[1].capitalize()} added at index {len(self.queue)}/{self.queue_limit} of the queue')

    def print_queue(self):
        # This method prints the current list of direction commands in the queue.
        q_len = len(self.queue)
        if q_len == 0:
            print(f'The command queue is currently empty!')
        else:
            print(f'The Botley command queue currently contains {q_len}/{self.queue_limit} commands:')
            print('Index  |  Command')
            [print(f'{i}: {command[1].capitalize()}') for command in self.queue]

    def clear_queue(self):
        # A simple method to erase the entire command queue
        self.queue = []
        print('The queue has been cleared')

    def delete(self, index: (int, list, tuple) = -1):
        # Deletes items from the queue by index or a range of indices. If no index is provided, the last item is deleted
        if isinstance(index, int):
            command = self.queue.pop(index)
            print(f'{command} removed from the queue at index {index}')

        elif isinstance(index, (list, tuple)):
            if len(index) > 2:
                print(f'If you want to delete a range of commands from the queue you must provide a start and end index'
                      f'Ex: delete_item((10, 15)) will delete all commands from index 10 to 15')
            else:
                start, end = index
                self.queue = self.queue[:start] + self.queue[end+1:]
                print(f'Commands from index {start} to {end} have been removed from the queue')

    @staticmethod
    def parse_direction(direction: str):
        # Accepts a direction command and returns the corresponding binary value that is transmitted to Botley.
        direction = direction.lower()  # To minimize errors, make sure direction is always lower case

        # The "move" dictionary maps simplified commands to the binary values that will be sent to Botley
        move = {'f': (1, 'forward'), 'b': (2, 'backward'),
                'l90': (3, 'left90'), 'r90': (4, 'right90'),
                'l45': (5, 'left45'), 'r45': (6, 'right45')}

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

    def move(self, direction: str, times=1):
        # Method that accepts "direction" and "times" parameters.
        command = self.parse_direction(direction)

        # If we are in interactive mode then the command should be transmitted immediately
        if self.mode == 'interactive':
            [self.transmit(command) for _ in range(times)]

        # Otherwise we just call the add_to_queue method to add our direction commands to the queue!
        else:
            self.add_to_queue(self, command, times)

    def moves(self, directions: str, times=1):
        # The moves() method is similar to move() except that "moves()" accepts a series of direction commands
        # as a sting and parses them to a list of individual directions which are sent to "move()". This way
        # you can program Botley using a simple string of commands like this: 'f, f, l90, f, f, l45, b, b'.
        # If a "times" parameter is passed, the entire string of commands is added to the queue "times" times.

        directions = directions.split(', ')   # Here is how we split the string into a list of individual commands

        # This for loop will repeat itself "times" times; so if times = 5, the string of commands will be sent 5 times.
        for _ in range(times):
            # Now we use a list comprehension to send each individual direction from the list of "directions" to move()
            [self.move(direction) for direction in directions]

    def light(self, times=1, queue=True):
        # This method allows you to control Botley's lights!
        # If "queue" = True, a light command will be added to the queue, otherwise it is transmitted immediately.
        # If "times" > 1 then the light command is transmitted or added to the queue "times" times.
        pass

    def transmit(self, command: str):
        # This method handles all transmission of commands to Botley.
        pass


    def connection_test(self):
        # Call this method and a command will be sent to Botley.
        # Botley will cycle through all of it's light colors to indicate that the test was successful.
        pass

