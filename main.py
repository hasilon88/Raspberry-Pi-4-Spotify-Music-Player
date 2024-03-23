from spotifyControls import *
from RPi import GPIO
import board
import digitalio
import adafruit_character_lcd.character_lcd as CharLCD
import multiprocessing
import pigpio
import os
from time import sleep
from smbus import SMBus

# -- CONSTANTS --
# LCD config variables
RS = digitalio.DigitalInOut(board.D17)
E = digitalio.DigitalInOut(board.D27)
DB7 = digitalio.DigitalInOut(board.D22)
DB6 = digitalio.DigitalInOut(board.D16)
DB5 = digitalio.DigitalInOut(board.D26)
DB4 = digitalio.DigitalInOut(board.D6)
COLS, ROWS = 8, 2
LCD = CharLCD.Character_LCD(RS,E,DB4,DB5,DB6,DB7,COLS,ROWS)

# Infinite rotator config variables
CLK, DT = 18, 25
GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(DT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Volume knob config variables
BUS = SMBus(1)

# Cette fonction permet de montrer les infomations de la chanson sur l'écran LCD
def showMusicInfoOnLcd(RS=RS, E=E, DB4=DB4, DB5=DB5, DB6=DB6, DB7=DB7, cols=COLS, rows=ROWS, lcd=LCD):

    # Ces variables nous permets de garder les informations en mémoire 
    tempSong, tempSinger = getCurrentPlayingSong().get("track_name"), getCurrentPlayingSong().get("artist_names")[0]

    while True:
        try:
            # On recupere la chanson et l'artist
            song = getCurrentPlayingSong().get("track_name")
            singer = getCurrentPlayingSong().get("artist_names")[0]
        except:
            song = "Unkown"
            singer = "Unkown"

        # Si l'artiste ou la chanson à plus de 8 caractère, il y a un "scrolling effect" sur le LCD
        if len(song) > 8 or len(singer) > 8:
            lcd.message = song
            lcd.cursor_position(0,1)
            lcd.message = singer
            sleep(0.001)
            lcd.move_left()
        else:
            lcd.message = song
            lcd.cursor_position(0,1)
            lcd.message = singer
        
        # Si la chanson change, on efface l'écran
        if tempSong != song or tempSinger != singer:
            lcd.clear()

        tempSong = getCurrentPlayingSong().get("track_name")
        tempSinger = getCurrentPlayingSong().get("artist_names")[0]



# Cette fonction nous permet de changer la chanson en fonction de quel sense on tourne le potentiomètre
def nextPrevWithRotator():
    clkLastState = GPIO.input(CLK)
    while True:
        clkState = GPIO.input(CLK)
        dtState = GPIO.input(DT)

        # Si le rotator change de place, on execute le code suivant
        if clkState != clkLastState:
            # S'il tourne a droite, on execute nextSong()
            if dtState != clkState:
                nextSong()
            # S'il tourne a gauche, on execute previous()
            else:
                previousSong()
            # On met un sleep pour ne pas recuperer plus q'un changement d'etat
            sleep(0.5)

        clkLastState = GPIO.input(CLK)

# Cette fonction nous permet de pause/play la chanson
def toggleButton():
    pi = pigpio.pi()
    pi.set_mode(5,pigpio.INPUT)
    pi.set_mode(14,pigpio.OUTPUT)

    dernier = 1
    while True:
        signal = pi.read(5)
        # Le GPIO 14 est connecte au LED
        pi.write(14,0)
        if signal != dernier and signal == 0:
            # Si on clique sur le bouton, ca change l'etat de la musique et ca allume la LED
            togglePlay()
            pi.write(14,1)
            # On met un sleep pour ne pas recuperer plus qu'un click
            sleep(0.5)
        dernier = signal  

# Cette fonction nous permet de changer le volume de la musique.
def adjustVolume():
    while True:
        # Dans la variable value, on recupere la valeur qui est entrain de se faire lire dans l'adresse memoire 0x4b, 
        # on a la divise par 2.55 pour avoir une valeur entre 0 et 100 et on l'arrondie pour ne pas avoir de nombre a virgule
        values = int(round((BUS.read_byte(0x4b))/2.55, 0))
        # On passe une commande au systeme qui change le volume
        os.system(f"amixer --quiet set Master {values}%")



# Chaque fonction est mis dans un processus différent et sont tous démarrés une après l'autre. 
lcdMusicProcess = multiprocessing.Process(target=showMusicInfoOnLcd)
lcdMusicProcess.start()

button = multiprocessing.Process(target=toggleButton)
button.start()

changeMusicRotator = multiprocessing.Process(target=nextPrevWithRotator)
changeMusicRotator.start()

changeVolume = multiprocessing.Process(target=adjustVolume)
changeVolume.start()
