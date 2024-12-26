'''
lancer

sudo pigpiod

avant
'''

from gpiozero import Servo
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory
import smbus
import csv

factory = PiGPIOFactory()

servoh = Servo(18, min_pulse_width=0.56/1000, max_pulse_width=1.85/1000, pin_factory=factory)
servob = Servo(17, min_pulse_width=0.52/1000, max_pulse_width=1.8/1000, pin_factory=factory)

# Configuration I2C
bus = smbus.SMBus(1)
SENSOR_ADDRESS = 0x39

# Définir le chemin du fichier CSV
nom_fichier = "couleurs_echantillons.csv"

# Liste des couleurs et structure pour stocker les données
COULEURS = ["bleu", "rouge", "vert", "marron", "jaune", "orange"]
echantillons = {couleur: [] for couleur in COULEURS}

# Initialisation du capteur
def init_sensor():
    bus.write_byte_data(SENSOR_ADDRESS, 0x00 | 0x80, 0x03)
    bus.write_byte_data(SENSOR_ADDRESS, 0x07 | 0x80, 0x00)

# Lecture des données RGB
def read_colors():
    bus.write_byte_data(SENSOR_ADDRESS, 0x00 | 0x80, 0x03)
    sleep(0.5)
    data = bus.read_i2c_block_data(SENSOR_ADDRESS, 0x10 | 0x80, 8)
    green = data[1] * 256 + data[0]
    red = data[3] * 256 + data[2]
    blue = data[5] * 256 + data[4]

    # Ajustement pour fond noir
    red -= 19.00
    green -= 35.00
    blue -= 16.00
    return red, green, blue

# Collecte des données pour une couleur spécifique
def collect_sample(couleur, num_samples=10):
    print(f"Insérez des pastilles de couleur '{couleur}'.")
    for i in range(num_samples):
        print(f"Mesure {i + 1}/{num_samples} pour {couleur}.")
        print("Position de mesure...")
        servoh.mid()
        sleep(1)
        red, green, blue = read_colors()
        echantillons[couleur].append((red, green, blue))
        print(f"R: {red}, G: {green}, B: {blue} enregistré pour {couleur}.")
        
        print("Position de dechargement...")
        servoh.max()
        sleep(1)
        
        print("Position de chargement...")
        servoh.min()
        sleep(3)

# Enregistrement des données dans un fichier CSV
def save_to_csv():
    with open(nom_fichier, 'w', newline='', encoding='utf-8') as fichier_csv:
        file = csv.writer(fichier_csv)
        file.writerow(["Couleur", "Red", "Green", "Blue"])  # En-têtes
        for couleur, samples in echantillons.items():
            for red, green, blue in samples:
                file.writerow([couleur, red, green, blue])
    print(f"Données enregistrées dans {nom_fichier}.")

# Programme principal
def main():
    try:
        init_sensor()
        servoh.mid()
        servob.mid()
        for couleur in COULEURS:
            collect_sample(couleur)
        save_to_csv()
    except KeyboardInterrupt:
        print("Programme interrompu.")
    finally:
        servoh.value = None
        servob.value = None
        print("Servos désactivés. Fin du programme.")

if __name__ == "__main__":
    main()


from gpiozero import Servo
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory
import smbus
import csv

factory = PiGPIOFactory()

servoh = Servo(18, min_pulse_width=0.56/1000, max_pulse_width=1.85/1000, pin_factory=factory)
servob = Servo(17, min_pulse_width=0.52/1000, max_pulse_width=1.8/1000, pin_factory=factory)

# Configuration I2C
bus = smbus.SMBus(1)
SENSOR_ADDRESS = 0x39

# Définir le chemin du fichier CSV
nom_fichier = "couleurs_echantillons.csv"

# Liste des couleurs et structure pour stocker les données
COULEURS = ["bleu", "rouge", "vert", "marron", "jaune", "orange"]
echantillons = {couleur: [] for couleur in COULEURS}

# Initialisation du capteur
def init_sensor():
    bus.write_byte_data(SENSOR_ADDRESS, 0x00 | 0x80, 0x03)
    bus.write_byte_data(SENSOR_ADDRESS, 0x07 | 0x80, 0x00)

# Lecture des données RGB
def read_colors():
    bus.write_byte_data(SENSOR_ADDRESS, 0x00 | 0x80, 0x03)
    sleep(0.5)
    data = bus.read_i2c_block_data(SENSOR_ADDRESS, 0x10 | 0x80, 8)
    green = data[1] * 256 + data[0]
    red = data[3] * 256 + data[2]
    blue = data[5] * 256 + data[4]
    
    return red, green, blue

# Collecte des données pour une couleur spécifique
def collect_sample(couleur, num_samples=10):
    print(f"Insérez des pastilles de couleur '{couleur}'.")
    for i in range(num_samples):
        print(f"Mesure {i + 1}/{num_samples} pour {couleur}.")
        print("Position de mesure...")
        servoh.mid()
        sleep(1)
        red, green, blue = read_colors()
        echantillons[couleur].append((red, green, blue))
        print(f"R: {red}, G: {green}, B: {blue} enregistré pour {couleur}.")
        
        print("Position de dechargement...")
        servoh.max()
        sleep(1)
        
        print("Position de chargement...")
        servoh.min()
        sleep(3)

# Enregistrement des données dans un fichier CSV
def save_to_csv():
    with open(nom_fichier, 'w', newline='', encoding='utf-8') as fichier_csv:
        file = csv.writer(fichier_csv)
        file.writerow(["Couleur", "Red", "Green", "Blue"])  # En-têtes
        for couleur, samples in echantillons.items():
            for red, green, blue in samples:
                file.writerow([couleur, red, green, blue])
    print(f"Données enregistrées dans {nom_fichier}.")

# Programme principal
def main():
    try:
        init_sensor()
        servoh.mid()
        servob.mid()
        for couleur in COULEURS:
            collect_sample(couleur)
        save_to_csv()
    except KeyboardInterrupt:
        print("Programme interrompu.")
    finally:
        servoh.value = None
        servob.value = None
        print("Servos désactivés. Fin du programme.")

if __name__ == "__main__":
    main()

