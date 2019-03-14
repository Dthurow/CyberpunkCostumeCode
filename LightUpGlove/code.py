import time
import board
import neopixel
from digitalio import DigitalInOut, Direction, Pull
import microphoneNeopixel


# On CircuitPlayground Express, and boards with built in status NeoPixel -> board.NEOPIXEL
# Otherwise choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D1
pixel_pin = board.NEOPIXEL

# The number of NeoPixels
num_pixels = 10

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=.5, auto_write=False,
                           pixel_order=ORDER)


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


def customRainbow(j):
    step = 255//num_pixels
    for i in range(num_pixels):
        index = (i+j) % num_pixels
        pixels[index] = wheel(i * step)
    pixels.show()
    return (j+ 1) % num_pixels

def flash(colorAndIndexTuple):
    color = colorAndIndexTuple[0]
    index = colorAndIndexTuple[1]

    pixels[index] = wheel(color)

    for i in range(1, 5):
        nullingIndex = (index + i) % num_pixels
        pixels[nullingIndex] = (0,0,0)

    pixels.show()
    time.sleep(.1)
    
    if index == 0:
        color = (color + 50) % 255

    return (color, (index +1) % num_pixels)



buttonA = DigitalInOut(board.BUTTON_A) #button a 
buttonA.direction = Direction.INPUT
buttonA.pull = Pull.DOWN
buttonB = DigitalInOut(board.BUTTON_B) # button b
buttonB.direction = Direction.INPUT
buttonB.pull = Pull.DOWN

startRainbowPassIn = 0
startFlashColor = (0,0)
startMicrophonePeak = 0

curState = 0
numStates = 4
rainbowPassIn = startRainbowPassIn
flashColor = startFlashColor
microphonePeak = startMicrophonePeak

def reset():
    pixels.fill((0,0,0))
    pixels.show()
    rainbowPassIn = startRainbowPassIn
    flashColor = startFlashColor
    microphonePeak = startMicrophonePeak


while True:
    if buttonA.value:
        curState = (curState + 1) % numStates
        reset()
    elif buttonB.value:
        reset()
        if curState > 0:
            curState -= 1
        else:
            curState = numStates -1

    if curState == 0:
        print("rainbow")
        rainbowPassIn = customRainbow(rainbowPassIn)
        time.sleep(.1)
    elif curState == 1:
        print("flash")
        flashColor = flash(flashColor)
    elif curState == 2:
        print("off")
        pixels.fill((0,0,0))
        pixels.show()
        time.sleep(.1)
    elif curState == 3:
        print("microphone")
        microphonePeak = microphoneNeopixel.microphoneFunc(pixels, microphonePeak)
