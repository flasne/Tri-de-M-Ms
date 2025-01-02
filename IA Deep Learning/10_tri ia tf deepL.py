from gpiozero import Servo
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory
import smbus
import time
import tensorflow as tf

# Configuration du Raspberry Pi
factory = PiGPIOFactory()

# Initialisation des servomoteurs
servo_horizontal = Servo(18, min_pulse_width=0.56/1000, max_pulse_width=1.85/1000, pin_factory=factory)
servo_vertical = Servo(17, min_pulse_width=0.52/1000, max_pulse_width=1.7/1000, pin_factory=factory)

# Charger le modèle TensorFlow
modele = tf.keras.models.load_model('modele_tensorflow DeepL.h5')

# Définir les positions des servomoteurs pour chaque index de couleur
SERVO_POSITIONS = {
    "horizontal": {
        "chargement": -0.98,
        "mesure": 0,
        "ejection": 0.98
    },
    "vertical": {
        25: -0.94,  # Jaune
        27: -0.7,   # Orange
        15: -0.3,   # Marron
        9: 0.1,    # Rouge
        28: 0.1,    # Rouge
        12: 0.55,   # Vert
        13: 0.55,   # Vert
        4: 0.95    # Bleu
    }
}

# Initialisation du bus I2C pour le capteur de couleur
bus = smbus.SMBus(1)




def afficher_indices_classes():
    print("Correspondance des indices et des positions des couleurs dans SERVO_POSITIONS :")
    for index, position in SERVO_POSITIONS["vertical"].items():
        print(f"Index : {index}, Position servo : {position}")







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

# Fonction : Détecter l'index de la couleur
def detect_color_index():
    red, green, blue = read_colors()
    # Préparer les données pour le modèle TensorFlow
    nouvelle_couleur = [[red, green, blue]]  # Forme attendue : liste de listes
    
    # Faire la prédiction
    prediction = modele.predict(nouvelle_couleur)
    print(f"Probabilités de la prédiction : {prediction[0]}")
    couleur_index = tf.argmax(prediction[0]).numpy()  # Index de la classe prédite
    print(f"Index de la couleur détectée : {couleur_index}")
    return couleur_index

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
        couleur_index = detect_color_index()

        if couleur_index in SERVO_POSITIONS["vertical"]:
            print(f"Tri pour la couleur d'index : {couleur_index}")
            position_servo(servo_vertical, SERVO_POSITIONS["vertical"][couleur_index])
            print("Éjection...")
            position_servo(servo_horizontal, SERVO_POSITIONS["horizontal"]["ejection"])
        else:
            print(f"Couleur inconnue (index {couleur_index}), éjection à une position par défaut.")
            position_servo(servo_vertical, 0)  # Position par défaut ou d'échec

        sleep(1)  # Pause avant la prochaine itération

# Programme principal
if __name__ == "__main__":
    try:
        print("Initialisation du capteur...")
        init_sensor()
        afficher_indices_classes()
        sleep(10)  # Pause avant la prochaine itération
        
        print("Début du tri...")
        tri_m_and_ms()
    except KeyboardInterrupt:
        print("Programme arrêté par l'utilisateur.")
    finally:
        # Désactiver les servomoteurs
        servo_horizontal.value = None
        servo_vertical.value = None
        print("Servos désactivés.")
