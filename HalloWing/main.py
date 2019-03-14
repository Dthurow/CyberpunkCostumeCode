import time
import board
import neopixel
import audioio
import touchio


# On CircuitPlayground Express, and boards with built in status NeoPixel -> board.NEOPIXEL
# Otherwise choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D1
pixel_pin = board.EXTERNAL_NEOPIXEL

#color standards
RED = 0x100000  
YELLOW = (0x10, 0x10, 0)
GREEN = (0, 0x10, 0)
AQUA = (0, 0x10, 0x10)
BLUE = (0, 0, 0x10)
PURPLE = (0x10, 0, 0x10)
BLACK = (0, 0, 0)


# The number of NeoPixels
num_pixels = 30

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

#set the left and right touch sensors
touch1 = touchio.TouchIn(board.A2)
touch2 = touchio.TouchIn(board.A5)

#set the speaker
AUDIO = audioio.AudioOut(board.A0)     # Speaker

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False,
                           pixel_order=ORDER)

def play_wav(name, loop=False):
    """
    Play a WAV file in the 'sounds' directory.
    @param name: partial file name string, complete name will be built around
                 this, e.g. passing 'foo' will play file 'sounds/foo.wav'.
    @param loop: if True, sound will repeat indefinitely (until interrupted
                 by another sound).
    """
    try:
        wave_file = open('Sounds/' + name + '.wav', 'rb')
        wave = audioio.WaveFile(wave_file)
        AUDIO.play(wave, loop=loop)
    except:
        return

def color_chase(color, wait):
    for i in range(num_pixels):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(255 - pos*3)
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)

def off(audioOff = True):
    pixels.fill((0,0,0))
    pixels.show()
    if audioOff and AUDIO.playing:
        AUDIO.stop()

def partyRainbow():
    playMusic()
    for i in range(0, num_pixels, 2):
        pixel_index = (i * 256 // num_pixels)
        pixels[i] = wheel(pixel_index & 255)
    pixels.show()
    time.sleep(.1)
    off(False)
    time.sleep(.1)
    for i in range(1, num_pixels, 2):
        pixel_index = (i * 256 // num_pixels)
        pixels[i] = wheel(pixel_index & 255)
    pixels.show()
    time.sleep(.1)
    off(False)
    time.sleep(.1)

def flash():
    pixels.fill((0, 0x10, 0))
    pixels.show()
    time.sleep(.2)
    off(False)
    time.sleep(.2)

def playMusic():
    if not AUDIO.playing:
        play_wav("Monplaisir_-_04_-_Level_1")

def colorChase():
    color_chase(AQUA, .2)
    off()


StateList = [colorChase, flash, partyRainbow]
CurState = 0
RunStates = False

while True:
    if (touch1.value):
        CurState = (CurState + 1)% len(StateList)
        off()

    if (touch2.value):
        RunStates = not RunStates

    if RunStates:
        StateList[CurState]()
    else:
        off()
    time.sleep(.2)
    
