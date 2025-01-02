import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Dropout
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt
import joblib

# Charger les données à partir du fichier CSV
fichier_csv = "couleurs.csv"  # Remplacez par le chemin de votre fichier CSV
data = pd.read_csv(fichier_csv)

# Préparer les données
X = data[["Red", "Green", "Blue"]].values  # Les colonnes RGB
y = data["Couleur"].values  # La colonne des étiquettes

# Encoder les étiquettes en entiers
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Convertir les étiquettes en format one-hot (nécessaire pour TensorFlow)
y_one_hot = to_categorical(y_encoded)

# Diviser les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y_one_hot, test_size=0.2, random_state=42)

# Définir le modèle en utilisant l'API fonctionnelle
inputs = Input(shape=(3,), name="Input_Layer")  # Couche d'entrée
x = Dense(64, activation='relu', name="Dense_1")(inputs)  # Première couche dense
x = Dropout(0.2, name="Dropout_1")(x)  # Dropout pour régularisation
x = Dense(32, activation='relu', name="Dense_2")(x)  # Deuxième couche dense
outputs = Dense(y_one_hot.shape[1], activation='softmax', name="Output_Layer")(x)  # Couche de sortie

# Création du modèle
model = Model(inputs=inputs, outputs=outputs)

# Compiler le modèle
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Entraîner le modèle
print("Entraînement du modèle...")
history = model.fit(X_train, y_train, epochs=50, batch_size=8, validation_data=(X_test, y_test))

# Évaluer le modèle
print("\nÉvaluation sur l'ensemble de test :")
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Précision : {test_accuracy * 100:.2f}%")

# Visualisation des courbes d'apprentissage
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.title("Courbes d'apprentissage")
plt.show()

# Sauvegarder le modèle entraîné
model.save("modele_tensorflow API.h5")
print("Modèle sauvegardé sous 'modele_tensorflow API.h5'.")

# Sauvegarder l'encodeur des étiquettes
joblib.dump(label_encoder, "label_encoder_tensorflow.pkl")
print("Encodeur des étiquettes sauvegardé sous 'label_encoder_tensorflow.pkl'.")

