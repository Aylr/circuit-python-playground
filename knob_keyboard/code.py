"""
https://github.com/andyclymer/minikbd/tree/master/Software/TwoEncoder-VolumeControl
Handy bits for track control:
- cc.send(ConsumerControlCode.SCAN_NEXT_TRACK)
- cc.send(ConsumerControlCode.SCAN_PREVIOUS_TRACK)
"""
import board
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from digitalio import DigitalInOut, Direction, Pull
from encoder import Encoder
import time
import random
import neopixel


kbd = Keyboard()
cc = ConsumerControl()

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
colors = [RED, YELLOW, GREEN, BLUE, CYAN, PURPLE]
color_i = 0
color_increment = 13
color_max = 255

letters = [
    'a',
    'b',
    'c',
    'd',
    'e',
    'f',
    'g',
    'h',
    'i',
    'j',
    'k',
    'l',
    'm',
    'n',
    'o',
    'p',
    'q',
    'r',
    's',
    't',
    'u',
    'v',
    'w',
    'x',
    'y',
    'z',
    '.',
    '?',
    '!',
    'space',
]
keycodes_by_letter = {
    'a': Keycode.A,
    'b': Keycode.B,
    'c': Keycode.C,
    'd': Keycode.D,
    'e': Keycode.E,
    'f': Keycode.F,
    'g': Keycode.G,
    'h': Keycode.H,
    'i': Keycode.I,
    'j': Keycode.J,
    'k': Keycode.K,
    'l': Keycode.L,
    'm': Keycode.M,
    'n': Keycode.N,
    'o': Keycode.O,
    'p': Keycode.P,
    'q': Keycode.Q,
    'r': Keycode.R,
    's': Keycode.S,
    't': Keycode.T,
    'u': Keycode.U,
    'v': Keycode.V,
    'w': Keycode.W,
    'x': Keycode.X,
    'y': Keycode.Y,
    'z': Keycode.Z,
    '.': Keycode.PERIOD,
    'space': Keycode.SPACE,
}

padded_letters = letters + ['']
letter_i = 0

def display_gui():
    global letters
    global padded_letters

    line_1 = [' '] * len(padded_letters)

    # TODO TRY CATCH
    line_1[letter_i] = '['
    try:
        line_1[letter_i + 1] = ']'
    except IndexError:
        line_1[0] = ']'

    readout = []
    for sep, letter in zip(line_1, padded_letters):
        readout.append(sep)
        readout.append(letter)
    print(''.join(readout))

def check_wrap():
    global letters
    global letter_i
    if letter_i >= len(letters):
        letter_i = 0
    elif letter_i < 0:
        letter_i = len(letters) - 1

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)

prevTurn = time.monotonic()
def fastTurn():
	global prevTurn
	now = time.monotonic()
	diff = now - prevTurn
	prevTurn = now
    # 0.1 for no neopixel code
    # bigger for neopixel delays
	if diff < 0.2:
		return True
	return False

def enc2Up():
    global color_i
    global letter_i
    # print(">", letters[letter_i])
    pixels.fill(wheel(color_i))
    color_i += color_increment
    letter_i += 1
    pixels.show()
    check_wrap()
    display_gui()
    # if not fastTurn():
    #     kbd.press(Keycode.ALT)
    #     kbd.press(Keycode.SHIFT)
    # cc.send(ConsumerControlCode.VOLUME_INCREMENT)
    # kbd.release_all()
    

def enc2Down():
    global color_i
    global letter_i
    # print("<", letters[letter_i])
    pixels.fill(wheel(color_i))
    color_i -= color_increment
    letter_i -= 1
    pixels.show()
    check_wrap()
    display_gui()
    # if not fastTurn():
    #     kbd.press(Keycode.ALT)
    #     kbd.press(Keycode.SHIFT)
    # cc.send(ConsumerControlCode.VOLUME_DECREMENT)
    # kbd.release_all()

def button1():
    if not fastTurn():
        # print(letters[letter_i])
        kbd.send(keycodes_by_letter[letters[letter_i]])
        # cc.send(ConsumerControlCode.PLAY_PAUSE)

e2 = Encoder(board.D3, board.D4, upCallback=enc2Up, downCallback=enc2Down)

button = DigitalInOut(board.D2)
button.direction = Direction.INPUT
button.pull = Pull.UP

# NeoPixel strip (of 16 LEDs) connected on D4
NUMPIXELS = 16
pixels = neopixel.NeoPixel(board.D1, NUMPIXELS, brightness=.1, auto_write=False, bpp=4)

display_gui()

while True:
    if color_i > color_max:
        color_i = 0
    elif color_i < 0:
        color_i = color_max

    e2.update()
    if not button.value:
        button1()

