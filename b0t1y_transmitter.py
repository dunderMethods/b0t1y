import pigpio
import time
import json

GPIO = 18
FREQ = 38
pi = pigpio.pi()  # Connect to Pi.


def send_ir(encoded):
    pi.set_mode(GPIO, pigpio.OUTPUT)  # IR TX connected to this GPIO.
    pi.wave_add_new()
    emit_time = time.time()
    marks_wid = {}
    spaces_wid = {}
    wave = [0] * len(encoded)

    for i in range(0, len(encoded)):
        ci = int(encoded[i] / 2.1)  # Hack to fix the issue where my signals were getting stretched
        if i & 1:  # Space
            if ci not in spaces_wid:
                pi.wave_add_generic([pigpio.pulse(0, 0, ci)])
                spaces_wid[ci] = pi.wave_create()
            wave[i] = spaces_wid[ci]
        else:  # Mark
            if ci not in marks_wid:
                wf = carrier(GPIO, FREQ, ci)
                pi.wave_add_generic(wf)
                marks_wid[ci] = pi.wave_create()
            wave[i] = marks_wid[ci]

    delay = emit_time - time.time()

    time.sleep(delay) if delay > 0.0 else None

    pi.wave_chain(wave)

    while pi.wave_tx_busy():
        time.sleep(0.002)

    # Cleanup
    [pi.wave_delete(marks_wid[i]) for i in marks_wid]
    [pi.wave_delete(spaces_wid[i]) for i in spaces_wid]
    marks_wid, spaces_wid = {}, {}


def carrier(gpio, frequency, micros):
    """ Generate carrier square wave. """
    waveform = []
    cycle = 1000.0 / frequency
    cycles = int(round(micros / cycle))
    on = int(round(cycle / 2.0))
    sofar = 0
    for c in range(cycles):
        target = int(round((c + 1) * cycle))
        sofar += on
        off = target - sofar
        sofar += off
        waveform.append(pigpio.pulse(1 << gpio, 0, on))
        waveform.append(pigpio.pulse(0, 1 << gpio, off))
    return waveform
