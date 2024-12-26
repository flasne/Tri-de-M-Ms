import pandas as pd
from pandas.plotting import scatter_matrix
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib

# === 1. Chargement et exploration des données ===

# Chargement du dataset
file_path = 'couleurs.csv'  # Remplacez par le chemin correct
try:
    dataset = pd.read_csv(file_path)
    print("Dataset loaded successfully.")
except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
    exit()

# Dimensions du dataset
print("Dataset dimensions:", dataset.shape)

# Aperçu des premières lignes
print("First 5 rows:\n", dataset.head())

# Statistiques descriptives
print("Descriptive statistics:\n", dataset.describe())

# Matrice de dispersion des variables
scatter_matrix(dataset)
plt.title("Scatter Matrix of Dataset")
plt.show()

# === 2. Préparation des données ===

# Séparation des caractéristiques (RVB) et des labels (classe des couleurs)
X = dataset.iloc[:, :3].values  # Colonnes RVB
Y = dataset.iloc[:, 3].values  # Classe de couleur

# Encodage des labels (classes des couleurs)
label_encoder = LabelEncoder()
Y_encoded = label_encoder.fit_transform(Y)

# Séparation des données en ensembles d'entraînement et de validation
X_train, X_validation, Y_train, Y_validation = train_test_split(
    X, Y_encoded, test_size=0.30, random_state=1
)

# === 3. Définition et évaluation des modèles ===

# Liste des modèles à tester
models = [
    ('LR', LogisticRegression(solver='liblinear', multi_class='ovr')),
    ('LDA', LinearDiscriminantAnalysis()),
    ('KNN', KNeighborsClassifier()),
    ('CART', DecisionTreeClassifier()),
    ('NB', GaussianNB()),
    ('SVM', SVC(gamma='auto'))
]

# Comparaison des modèles
results = []
names = []
print("\nModel Evaluation Results:")
for name, model in models:
    kfold = StratifiedKFold(n_splits=7, random_state=1, shuffle=True)
    cv_results = cross_val_score(model, X_train, Y_train, cv=kfold, scoring='accuracy')
    results.append(cv_results)
    names.append(name)
    print(f"{name}: {cv_results.mean():.6f} ({cv_results.std():.6f})")

# Visualisation des performances
plt.boxplot(results, labels=names)
plt.title('Algorithm Comparison')
plt.ylabel('Accuracy')
plt.show()

# === 4. Entraînement, prédictions et sauvegarde des modèles ===

# Fonction utilitaire pour entraîner, prédire et sauvegarder un modèle
def train_and_save_model(model, model_name, X_train, Y_train, X_validation, Y_validation, label_encoder):
    model.fit(X_train, Y_train)
    predictions = model.predict(X_validation)

    # Sauvegarde du modèle et de l'encodeur
    joblib.dump(model, f'{model_name}.pkl')
    joblib.dump(label_encoder, f'label_encoder_{model_name}.pkl')

    # Évaluation des performances
    print(f"\n=== Results for {model_name} ===")
    print("Accuracy:", accuracy_score(Y_validation, predictions))
    print("Confusion Matrix:\n", confusion_matrix(Y_validation, predictions))
    print("Classification Report:\n", classification_report(Y_validation, predictions))

# Entraînement et sauvegarde pour chaque modèle
for name, model in models:
    train_and_save_model(model, name, X_train, Y_train, X_validation, Y_validation, label_encoder)

# === Fin du programme ===
print("All models trained and saved successfully.")

