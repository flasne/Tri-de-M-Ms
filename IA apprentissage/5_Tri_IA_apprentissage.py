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
import pandas as pd


factory = PiGPIOFactory()

servoh = Servo(18, min_pulse_width=0.56/1000, max_pulse_width=1.85/1000, pin_factory=factory)
servob = Servo(17, min_pulse_width=0.52/1000, max_pulse_width=1.8/1000, pin_factory=factory)

# Charger le modèle et le label encoder
modele = joblib.load('LR.pkl')
label_encoder = joblib.load('label_encoder_LR.pkl')

# Définir les angles en microsecondes pour les positions
servoh_POSITIONS = {
    "chargement": 0.56/1000,  # Microsecondes pour la position de chargement
    "mesure": 0.645/1000,      # Microsecondes pour la position de mesure
    "ejection": 1.85/1000     # Microsecondes pour la position d'éjection
}


servob_POSITIONS = {
    
    "jaune": -0.95,   # Microsecondes pour jaune
    "marron": -0.3,  # poste 0 pour marron
    "rouge": 0.1,   # Microsecondes pour rouge
    "orange": -0.7,  # Microsecondes pour orange
    "vert":  0.6,    # poste 1 pour vert
    "bleu": .98     # Microsecondes pour bleu
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
    
 
    red =red - 19
    green = green -33
    blue = blue - 16
    
    #rang = rang +1
    return cData, red, green, blue
    
# Déterminer la couleur dominante
def detect_color():
    _, red, green, blue = read_colors()
    print(f"R: {red}, G: {green}, B: {blue}")
    
    # Utiliser le modèle pour prédire la catégorie en fonction des valeurs RGB
    nouvelle_couleur = pd.DataFrame([[red, green, blue]], columns=["Red", "Green", "Blue"])
    couleur_encoded = modele.predict(nouvelle_couleur)
    #couleur_encoded = modele.predict(nouvelle_couleur)
    couleur = label_encoder.inverse_transform([couleur_encoded[0]])[0]  # Décoder
    
    print(f"Couleur prédite : {couleur}")
    return couleur  # Retourne une chaîne de caractères (ex: "rouge", "bleu", etc.)

# Trier les M&M’s
def tri_m_and_ms():
    while True:
        print("Passage en position de chargement...")
        servoh.min()
        sleep(1)
        print("Passage en position de mesure...")
        servoh.mid()
        couleur= detect_color()
        print(couleur)
        
        if couleur in servob_POSITIONS:
            print(f"Tri pour {couleur}...")
            servob.value = servob_POSITIONS[couleur]
            # Éjection après tri
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