'''
lancer

sudo pigpiod

avant
'''

from gpiozero import Servo
from time import sleep

from gpiozero.pins.pigpio import PiGPIOFactory

import smbus
import time
import csv
import joblib


factory = PiGPIOFactory()

servoh = Servo(18, min_pulse_width=0.56/1000, max_pulse_width=1.85/1000, pin_factory=factory)
servob = Servo(17, min_pulse_width=0.52/1000, max_pulse_width=1.8/1000, pin_factory=factory)


servob_POSITIONS = {
    "marron": -0.3,   # Position pour marron
    "vert": 0.6,      # Position pour vert
    "orange": -0.95,  # Position pour orange
    "jaune": -0.7,    # Position pour jaune
    "rouge": 0.1,     # Position pour rouge
    "bleu": 0.9       # Position pour bleu
}

COLOR_RANGES = {
    "bleu": [(0.0, 0.0), (1.0, 2.0), (4.0, 5.0)],
    "rouge": [(6.0, 7.0), (0.0, 1.0), (1.0, 1.0)],
    "vert": [(2.0, 2.0), (5.0, 6.0), (2.0, 2.0)],
    "marron": [(0.0, 1.0), (-1.0, -1.0), (0.0, 1.0)],
    "jaune": [(10.0, 12.0), (10.0, 13.0), (2.0, 3.0)],
    "orange": [(9.0, 11.0), (4.0, 5.0), (1.0, 2.0)],
}


# Get I2C bus
bus = smbus.SMBus(1)

# Initialisation du capteur
def init_sensor():
    # Initialisation du capteur
    # TCS3414 address, 0x39(57)
    # Select control register, 0x00(00), with Command register, 0x80(128)
    #		0x03(03)	Power ON, ADC enable
    bus.write_byte_data(0x39, 0x00 | 0x80, 0x03)


# Lecture des données de couleur
def read_colors():
    global rang
    bus.write_byte_data(0x39, 0x00 | 0x80, 0x03)
    # TCS3414 address, 0x39(57)
    # Select gain register, 0x07(07), with Command register, 0x80(128)
    #		0x00(00)	Gain : 1x, Prescaler Mode = Divide by 1
    bus.write_byte_data(0x39, 0x07 | 0x80, 0x00)
    time.sleep(0.5)
    # TCS3414 address, 0x39(57)
    # Read data back from 0x10(16), 8 bytes, with Command register, 0x80(128)
    # Green LSB, Green MSB, Red LSB, Red MSB
    # Blue LSB, Blue MSB, cData LSB, cData MSB
    data = bus.read_i2c_block_data(0x39, 0x10 | 0x80, 8)
    # Convert the data
    green = data[1] * 256 + data[0]
    red = data[3] * 256 + data[2]
    blue = data[5] * 256 + data[4]
    cData = data[7] * 256 + data[6]
    # Calculate luminance
    luminance = (-0.32466 * red) + (1.57837 * green) + (-0.73191 * blue)
    
 
    red -= 19.00
    green -= 35.00
    blue -= 16.00

    return cData, red, green, blue
    
# Déterminer la couleur dominante
def detect_color():
  _, r, g, b = read_colors()
  print(f"R: {r}, G: {g}, B: {b}")
  tolerance = 1
  for color, (r_range, g_range, b_range) in COLOR_RANGES.items():
        if (
            (r_range[0] - tolerance) <= r <= (r_range[1] + tolerance) and
            (g_range[0] - tolerance) <= g <= (g_range[1] + tolerance) and
            (b_range[0] - tolerance) <= b <= (b_range[1] + tolerance)
        ):
            return color
  return "inconnu"


# Trier les M&M’s
def tri_m_and_ms():
    while True:
        print("Passage en position de chargement...")
        servoh.min()
        sleep(1)
        print("Passage en position de mesure...")
        servoh.mid()
        couleur = detect_color()
        print(f"Couleur détectée : {couleur}")
        # Pause pour éviter des lectures rapides
        sleep(1)
        if couleur in servob_POSITIONS:
            print(f"Tri pour {couleur}...")
            servob.value = servob_POSITIONS[couleur]
            #control_servo(SERVO1_GPIO, SERVO1_POSITIONS["ejection"])  # Éjection après tri
            sleep(0.5)
            servoh.max()
        else:
            print("Couleur inconnue, ignorer l'objet")
     # Pause pour éviter des lectures rapides
        sleep(1)
        servob.value = 0

# Programme principal
print("Start in the middle")
servoh.mid()
servob.mid()
rang=1
try:
    init_sensor()
    tri_m_and_ms()
except KeyboardInterrupt:
    print("Arrêt du programme.")
