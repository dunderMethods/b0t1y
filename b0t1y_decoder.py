import numpy as np
import json
import pandas as pd

rules = {'header': 4150, 'mark': 642, 'space0': 1284, 'space1': 642, 'bits': 16, 'delta': 200, 'quiet': 25000, 'carrier': 38000}


def chk_tol(val, target, tol):
    #   Returns True if val is within target +/- tol, otherwise false.
    return 1 if target - tol <= val <= target + tol else 0


def decode_rpi(signals):
    cleaned = {}
    for key_name, data in signals.items():
        value = True
        bits = []
        for i, pulse in enumerate(data):
            bits.append(np.array([i, pulse, int(value)]))
            value = not value

        cleaned[key_name] = [bits]
    decode_signal(cleaned)


def decode_signal(commands):
    # Decode the contents of each transmission sample
    decd = {}
    for command, history in commands.items():
        samples = []
        for series in history:
            bursts = []
            burst = []
            header = False
            bits = []

            for sequence in series:
                if not sequence[2]:  # If a space
                    if header:  # If we already found the header
                        # If the length of the space is extra long
                        if chk_tol(sequence[1], rules['quiet'], 10000):
                            bursts.extend(burst)  # Assume we've finished processing a burst
                            burst = []  # Init to prepare for the next burst
                            header = False  # A new burst means a new header, so set to false
                            continue  # We got a burst! lets look for the next one

                        # Otherwise, keep appending bits
                        bits.append(str(chk_tol(sequence[1], rules['space0'], rules['delta'])))

                        # Each burst will contain a max of 16 bits, so if we're at 16
                        if len(bits) == rules['bits']:
                            #                             print('Found a packet!')
                            # Then it's time to store this burst and prepare for the next one
                            burst.append(hex(int(''.join(bits), 2)).split('x')[1].upper())  # Output to HEX
                            # burst.append(int(''.join(bits), 2))                           # Output to DEC
                            # burst.append(''.join(bits))                                   # Output to BIN
                            bits = []  # New burst means new bits - init
                            continue

                elif sequence[2]:  # If a mark... We don't really care about marks...
                    if not header:  # Unless we haven't found the header

                        # We totally care about that mark
                        if chk_tol(sequence[1], rules['header'], rules['delta']):
                            #                             print('Found the header!')
                            header = True  # Time to collect some bits...
                            continue

            samples.append(bursts)
        decd.update({command: samples})
    dfs = {key: pd.DataFrame(decd[key]) for key in decd.keys()}
    {print(f'{key}:\n {dfs[key]}\n\n') for key in decd.keys()}
    return decd
