'''
Pré-requis :
- Lancer la commande `sudo pigpiod` avant d'exécuter ce script.
- Assurez-vous que les bibliothèques nécessaires sont installées :
  - tensorflow
  - gpiozero
  - smbus
  - pandas
'''

from gpiozero import Servo
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory
import smbus
import time
import pandas as pd
import tensorflow as tf
import joblib

# Configuration du Raspberry Pi
factory = PiGPIOFactory()

# Initialisation des servomoteurs
servo_horizontal = Servo(18, min_pulse_width=0.56/1000, max_pulse_width=1.85/1000, pin_factory=factory)
servo_vertical = Servo(17, min_pulse_width=0.52/1000, max_pulse_width=1.7/1000, pin_factory=factory)

# Charger le modèle TensorFlow
modele = tf.keras.models.load_model('modele_tensorflow.h5')
# Charger l'encodeur de labels
label_encoder = joblib.load('label_encoder_tensorflow.pkl')

# Définir les positions des servomoteurs pour chaque couleur
SERVO_POSITIONS = {
    "horizontal": {
        "chargement": -0.98,
        "mesure": 0,
        "ejection": 0.98
    },
    "vertical": {
        "jaune": -0.94,
        "orange": -0.7,
        "marron": -0.3,
        "rouge": 0.1,
        "vert": 0.55,
        "bleu": 0.95
    }
}

# Initialisation du bus I2C pour le capteur de couleur
bus = smbus.SMBus(1)

# Fonction : Initialiser le capteur de couleur
def init_sensor():
    bus.write_byte_data(0x39, 0x00 | 0x80, 0x03)  # Activer le capteur
    print("Capteur initialisé.")

# Fonction : Lire les données de couleur depuis le capteur
def read_colors():
    bus.write_byte_data(0x39, 0x07 | 0x80, 0x00)  # Configuration du gain
    time.sleep(0.5)
    data = bus.read_i2c_block_data(0x39, 0x10 | 0x80, 8)  # Lecture des données
    red = data[3] * 256 + data[2]
    green = data[1] * 256 + data[0]
    blue = data[5] * 256 + data[4]

    # Calibrage des couleurs pour corriger les déviations
    red = max(0, red - 19)
    green = max(0, green - 33)
    blue = max(0, blue - 16)

    print(f"Valeurs RGB : R={red}, G={green}, B={blue}")
    return red, green, blue

# Fonction : Détecter la couleur dominante
def detect_color():
    red, green, blue = read_colors()
    # Préparer les données pour le modèle TensorFlow
    nouvelle_couleur = [[red, green, blue]]  # Forme attendue : liste de listes
    prediction = modele.predict(nouvelle_couleur)
    couleur_index = tf.argmax(prediction[0]).numpy()  # Index de la classe prédite
    couleur = label_encoder.inverse_transform([couleur_index])[0]  # Décoder l'index
    print(f"Couleur détectée : {couleur}")
    return couleur

# Fonction : Positionner les servomoteurs
def position_servo(servo, position):
    servo.value = position
    sleep(0.5)

# Fonction : Trier les M&M's
def tri_m_and_ms():
    while True:
        print("Déplacement en position de chargement...")
        position_servo(servo_horizontal, SERVO_POSITIONS["horizontal"]["chargement"])

        print("Déplacement en position de mesure...")
        position_servo(servo_horizontal, SERVO_POSITIONS["horizontal"]["mesure"])
        couleur = detect_color()

        if couleur in SERVO_POSITIONS["vertical"]:
            print(f"Tri pour la couleur : {couleur}")
            position_servo(servo_vertical, SERVO_POSITIONS["vertical"][couleur])
            print("Éjection...")
            position_servo(servo_horizontal, SERVO_POSITIONS["horizontal"]["ejection"])
        else:
            print("Couleur inconnue, objet ignoré.")

        sleep(1)  # Pause avant la prochaine itération

# Programme principal
if __name__ == "__main__":
    try:
        print("Initialisation du capteur...")
        init_sensor()
        print("Début du tri...")
        tri_m_and_ms()
    except KeyboardInterrupt:
        print("Programme arrêté par l'utilisateur.")
    finally:
        # Désactiver les servomoteurs
        servo_horizontal.value = None
        servo_vertical.value = None
        print("Servos désactivés.")

