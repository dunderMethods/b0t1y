from b0t1y_helpers import *
import numpy as np
import time

""" NOTE: Any function names beginning with an underscore '_' are functions you probably shouldn't be calling directly.
    Functions without the underscore are higher-level functions which could be useful to the user."""

rules = {
    # These values describe the infrared waveform characteristics that Botley expects. Don't change them!
    'header':   4150,
    'mark':     642,
    'space0':   1284,
    'space1':   642,
    'bits':     16,
    'delta':    200,
    'quiet':    25000,
    'carrier':  38000
}


def _build_init(volume):
    """ Builds the message initializer block at the beginning of each message """
    rtrn_qty = 3    # Init block is just the same packet repeated three times
    bits = [volume[0], 'F', '0', '0']
    return [hex(int(''.join(bits), 16))] * rtrn_qty


def _build_address(volume, address):
    """ Builds the address block, which comes after the init block of each message """
    address = '2' + ''.join(address)     # First part of the address block always includes a 2, append our address to it
    # Below, we iterate over "address" to create a 16-bit address packet for each part of the address
    # Address packet anatomy: [ volume_bit, address_bit, always 'B', address_packet_index ]
    packets = [[str(int(volume[1], 16)), address[i], 'B', str(i + 1)] for i in range(len(address))]
    return [hex(int(''.join(packet), 16)) for packet in packets]


def _build_message_header(volume, address):
    """ Builds the header (init, address) for each message """
    vol_bits = volume_map[volume]
    addr_bits = convert_addr(address) if address.isalpha() else address
    init_bytes = _build_init(vol_bits)
    address_bytes = _build_address(vol_bits, addr_bits)
    return init_bytes + address_bytes


def _build_commands(volume, commands):
    """ Accepts a list of user commands and converts them into their HEX equivalents """
    hex_commands = []
    vol_bits = volume_map[volume]
    for i, command in enumerate(commands):
        cmd_bit = parse_direction(command)[0]
        byte = [vol_bits[2], cmd_bit, f'{i+1:02d}']
        hex_commands.append(hex(int(''.join(byte), 16)))
    return hex_commands


def _build_instant(command):
    """ Accepts an instant user command and converts it into its HEX equivalent """
    # TODO add an instant command parser
    cmd_bit = parse_direction(command)[0]
    byte = ['9', cmd_bit, '0', '1']
    # Instant commands are simply the same hex value repeated twice
    hex_command = [hex(int(''.join(byte), 16))] * 2
    return hex_command


def build_message(volume, address, commands, instant=False):
    """ Builds the complete message that will be encoded and sent """
    # Construct the header which is sent with each transmission
    message_header = _build_message_header(volume, address)

    if instant:
        # If the command is instantly transmitted (light, sound, etc) it needs to be built differently
        user_commands = _build_instant(commands)

    else:
        # Convert the user commands into hex
        user_commands = _build_commands(volume, commands.replace(' ', '').split(','))

    # Combine the header and all of the commands to create the entire message
    hex_message = message_header + user_commands

    return hex_message


def encode_botley(message):
    """ Encodes the contents of our message into a list of pulse widths which represent zeros and ones"""
    encoded = []
    # TODO: The following 2 lines are a hack to add an end packet.
    #  Need to integrate the end packet into the build sequence
    mlen = len(message[7:])
    message += [f'0x0f{mlen:02d}']
    print(message)
    for data in message:
        # Convert the hex command to binary
        binary = f'{int(data, 16):16b}'.replace(' ', '0')

        # Use the binary values to construct a series of time periods which constitute the IR waveform
        # "For each bit in binary, if bit is 1, store a double-space and a mark, otherwise single-space and a mark."
        encode = [[rules['space1'], rules['mark']] if not int(bit) else [rules['space0'], rules['mark']] for bit in binary]

        # Use Numpy's ravel method to "flatten" our list-of-lists into a 1D list
        encode = np.array(encode).ravel().tolist()

        # Wrap the encoded command with a packet header and footer
        encode = [rules['header']] + encode + [rules['quiet']]

        # Add the latest packet to the encoded list
        encoded.extend(encode)
    print(encoded)
    return encoded


def build_and_encode(volume, address, commands, instant=False):
    """ Given a channel and list of commands, Performs end-to-end encoding and returns the encoded data"""
    message = build_message(volume, address, commands, instant=instant)
    encoded = encode_botley(message)
    return encoded




#
# def transmit(message):
#    emit_time = time.time()
#
#
#    for arg in args.id:
#       if arg in records:
#
#          code = records[arg]
#
#          # Create wave
#
#          marks_wid = {}
#          spaces_wid = {}
#
#          wave = [0]*len(code)
#
#          for i in range(0, len(code)):
#             ci = code[i]
#             if i & 1: # Space
#                if ci not in spaces_wid:
#                   pi.wave_add_generic([pigpio.pulse(0, 0, ci)])
#                   spaces_wid[ci] = pi.wave_create()
#                wave[i] = spaces_wid[ci]
#             else: # Mark
#                if ci not in marks_wid:
#                   wf = carrier(GPIO, FREQ, ci)
#                   pi.wave_add_generic(wf)
#                   marks_wid[ci] = pi.wave_create()
#                wave[i] = marks_wid[ci]
#
#          delay = emit_time - time.time()
#
#          if delay > 0.0:
#             time.sleep(delay)
#
#          pi.wave_chain(wave)
#
#
#          while pi.wave_tx_busy():
#             time.sleep(0.002)
#
#          emit_time = time.time() + GAP_S
#
#          for i in marks_wid:
#             pi.wave_delete(marks_wid[i])
#
#          marks_wid = {}
#
#          for i in spaces_wid:
#             pi.wave_delete(spaces_wid[i])
#
#          spaces_wid = {}