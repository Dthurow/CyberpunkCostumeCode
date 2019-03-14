# CircuitPlaygroundExpress_CapTouch

import time

import board
import touchio
import neopixel
import array
import math
import audioio
import digitalio

#global stuff
RED = 0x100000  
YELLOW = (0x10, 0x10, 0)
GREEN = (0, 0x10, 0)
AQUA = (0, 0x10, 0x10)
BLUE = (0, 0, 0x10)
PURPLE = (0x10, 0, 0x10)
BLACK = (0, 0, 0)


FREQUENCY = 440  # 440 Hz middle 'A'
SAMPLERATE = 8000  # 8000 samples/second, recommended!
 

# enable the speaker
speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker_enable.direction = digitalio.Direction.OUTPUT
speaker_enable.value = True
 
audio = audioio.AudioOut(board.A0)

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
        audio.play(wave, loop=loop)
    except:
        return


def makeSoundWave(frequency):
    length = SAMPLERATE // frequency
    sine_wave = array.array("H", [0] * length)
    for i in range(length):
        sine_wave[i] = int(math.sin(math.pi * 2 * i / 18) * (2 ** 15) + 2 ** 15)
    return audioio.RawSample(sine_wave)

# Generate one period of sine wav.
sine_wave_sample = makeSoundWave(FREQUENCY)

class touchSensor:
    isOn = False
    color = (255,0,0)
    pixelIndex = 0


    def __init__(self, color, pixelIndex, touchsens, soundWave):
        self.color = color
        self.pixelIndex = pixelIndex
        self.touch = touchsens
        self.soundWave = soundWave
    
    def playClick(self):
        audio.play(self.soundWave, loop=True)  # keep playing the sample over and over
        time.sleep(.05)  # until...
        audio.stop()  # we tell the board to stop

    def checkTouch(self):
        colorToSet = (0,0,0)
        if self.touch.value and self.isOn:
            self.isOn = False
            self.playClick()
        elif self.touch.value and not self.isOn:
            self.isOn = True
            self.playClick()

        if (self.isOn):
            colorToSet = self.color

        pixels[self.pixelIndex] = colorToSet
        return self.isOn

#set up
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=.2)

touch1 = touchio.TouchIn(board.A1)
touch2 = touchio.TouchIn(board.A2)
touch3 = touchio.TouchIn(board.A3)
touch4 = touchio.TouchIn(board.A4)
touch5 = touchio.TouchIn(board.A5)
touch6 = touchio.TouchIn(board.A6)
touch7 = touchio.TouchIn(board.A7)


touchPads = {"touch1" : touchSensor(RED, 6, touch1, makeSoundWave(440)),
"touch2" : touchSensor(AQUA, 8, touch2, makeSoundWave(494)),
"touch3" : touchSensor(PURPLE, 9, touch3, makeSoundWave(523)),
"touch4" : touchSensor(BLUE, 1, touch4, makeSoundWave(587)),
"touch5" : touchSensor(YELLOW, 2, touch5, makeSoundWave(660)),
"touch6" : touchSensor(BLUE, 3, touch6, makeSoundWave(690)),
"touch7" : touchSensor(GREEN, 4, touch7, makeSoundWave(780)),

  }

goodSets = [["touch1", "touch2", "touch3"], ["touch7", "touch4", "touch5"]]
badSets = [["touch1", "touch3", "touch5"]]

def flash(color, fileToPlay):
    play_wav(fileToPlay)
    for i in range(0,3):
        pixels.fill(color)
        pixels.show()
        time.sleep(.2)
        pixels.fill((0,0,0))
        pixels.show()
        time.sleep(.2)

def checkSets(onSet, setsToCheck, colorToUse, fileToPlay):
    if len(onSet) > 0:
        for curset in setsToCheck:
            if len(curset) == len(onSet):
                isMatch = True
                for i in range(0, len(onSet)):
                    if onSet[i] != curset[i]:
                        isMatch = False
                        break
                if isMatch:
                    flash(colorToUse, fileToPlay)
                    break

prevOnTouch = []
onTouchPads = []
#main loop
while True:
    for t in touchPads.keys():
        print("check " + t)
        if touchPads[t].checkTouch():
            onTouchPads.append(t)
    print(onTouchPads)
    if prevOnTouch != onTouchPads:
        checkSets(onTouchPads, goodSets, GREEN, "SystemAccessed")
        checkSets(onTouchPads, badSets, RED, "AccessDenied")
    time.sleep(0.2)
    prevOnTouch = onTouchPads
    onTouchPads = []



