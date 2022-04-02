from b0t1y_helpers import parse_direction
import numpy as np
import time


rules = {
    # These values describe the infrared waveform characteristics
    'header':   4150,
    'mark':     642,
    'space0':   1284,
    'space1':   642,
    'bits':     16,
    'delta':    200,
    'quiet':    25000,
    'carrier':  38000
}


def build_address(addr):
    """ Builds the address bytes at the beginning of each message """
    rtrn_qty = 3
    bits = [addr, 'F', '0', '0']
    return [hex(int(''.join(bits), 16))] * rtrn_qty


def build_preamble(addr):
    """ Builds the preamble bytes at the beginning of each message """
    rtrn_qty = 5
    byts = [[str(int(addr, 16) - 3), '2', 'B', str(i)] for i in range(1, rtrn_qty + 1)]
    return [hex(int(''.join(byte), 16)) for byte in byts]


def build_message_header(channel):
    """ Builds the header for each message """
    address_bytes = build_address(channel)
    preamble_bytes = build_preamble(channel)
    return address_bytes + preamble_bytes


def build_commands(commands):
    """ Accepts a list of user commands and converts them into their HEX equivalents """
    hex_commands = []
    for i, command in enumerate(commands):
        cmd_bit = parse_direction(command)[0]
        byte = ['8', cmd_bit, f'{i+1:02d}']
        hex_commands.append(hex(int(''.join(byte), 16)))
    return hex_commands


def build_instant(command):
    """ Accepts an instant user command and converts them into its HEX equivalent """
    cmd_bit = parse_direction(command)[0]
    byte = ['9', cmd_bit, '01']
    # Instant commands are simply the same hex value repeated twice
    hex_command = [hex(int(''.join(byte), 16))] * 2
    return hex_command


def build_message(channel, commands, instant=False):
    """ Builds the complete message that will be encoded and sent """
    # Construct the header which is sent with each transmission
    message_header = build_message_header(channel)

    if instant:
        # If the command is instantly transmitted (light, sound, etc) it needs to be built differently
        user_commands = build_instant(commands)

    else:
        # Convert the user commands into hex
        user_commands = build_commands(commands.replace(' ', '').split(','))

    # Combine the header and all of the commands to create the entire message
    hex_message = message_header + user_commands

    return hex_message


def encode_botley(message):
    """ Encodes the contents of the message """
    encoded = []
    for data in message:
        binary = f'{int(data, 16):16b}'.replace(' ', '0')
        encode = [[rules['space1'], rules['mark']] if int(bit) else [rules['space0'], rules['mark']] for bit in binary]
        encode = np.array(encode).ravel().tolist()
        encode = [rules['header']] + encode + [rules['quiet']]
        encoded.extend(encode)
    return encoded


def build_and_encode(channel, commands, instant=False):
    message = build_message_header(channel)
    message.extend(build_message(channel, commands, instant=instant))
    encoded = encode_botley(message)
    return encoded

def carrier(gpio, frequency, micros):
   """ Generate carrier square wave. """
   waveform = []
   cycle = 1000.0 / frequency
   cycles = int(round(micros/cycle))
   on = int(round(cycle / 2.0))
   sofar = 0
   for c in range(cycles):
      target = int(round((c+1)*cycle))
      sofar += on
      off = target - sofar
      sofar += off
      # waveform.append(pigpio.pulse(1 << gpio, 0, on))
      # waveform.append(pigpio.pulse(0, 1 << gpio, off))
   return waveform

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