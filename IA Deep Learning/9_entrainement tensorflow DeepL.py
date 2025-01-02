import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt
import joblib
import numpy as np

# Charger les données depuis le fichier CSV
fichier_csv = "couleurs_deep.csv"  # Remplacez par le chemin de votre fichier CSV
data = pd.read_csv(fichier_csv)

# Les données ne contiennent pas de colonne de labels explicites
# On suppose que chaque combinaison RGB correspond à une classe unique
# Charger les données sans la colonne des labels explicites
X = data.values  # Les colonnes RGB

# S'assurer que les données sont de type float
X = X.astype(float)

# Vérifier et gérer les valeurs manquantes
if pd.isnull(X).any():
    X = pd.DataFrame(X).fillna(0).values

# Générer des étiquettes basées sur des combinaisons uniques de RGB
y = pd.factorize([tuple(rgb) for rgb in X])[0]

# Convertir les étiquettes en format one-hot
y_one_hot = to_categorical(y)

# Diviser les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y_one_hot, test_size=0.2, random_state=42)

# Définir le modèle TensorFlow
model = Sequential([
    Dense(64, input_dim=3, activation='relu'),  # Couche d'entrée avec 3 neurones pour RGB
    Dropout(0.2),  # Dropout pour éviter le surapprentissage
    Dense(32, activation='relu'),  # Couche cachée
    Dense(y_one_hot.shape[1], activation='softmax')  # Couche de sortie
])

# Compiler le modèle
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Entraîner le modèle
print("Entraînement du modèle...")
history = model.fit(X_train, y_train, epochs=50, batch_size=8, validation_data=(X_test, y_test))
# Convertir les étiquettes one-hot en indices
y_test_indices = np.argmax(y_test, axis=1)# Convertir les étiquettes one-hot en indices

# Afficher les indices des classes
print(f"Indices des classes dans les données d'entraînement : {sorted(set(y_test_indices))}")


# Évaluer le modèle
print("\nÉvaluation sur l'ensemble de test :")
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Précision : {test_accuracy * 100:.2f}%")

# Visualisation de l'historique d'entraînement
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

# Sauvegarder le modèle entraîné
model.save("modele_tensorflow DeepL.h5")
print("Modèle sauvegardé sous 'modele_tensorflow DeepL.h5'.")

# Sauvegarder l'encodeur des étiquettes
joblib.dump(pd.factorize([tuple(rgb) for rgb in X])[1], "label_encoder_tensorflow DeepL.pkl")
print("Encodeur des étiquettes sauvegardé sous 'label_encoder_tensorflow DeepL.pkl'.")
