# Tri-de-M-Ms

# Introduction à l'IA avec un Trieur de Couleurs pour M&M's

<a href="https://github.com/flasne/Tri-de-M-Ms"</a>

## 1. Introduction Générale

- **Objectifs du cours :**
  - Comprendre les concepts de base de l'IA et leur application dans un projet concret.
- **Présentation du projet :**
  - Créer un trieur de couleurs pour des M&M's à l'aide d'un Raspberry Pi, avec une progression de techniques (classiques à IA avancée).
- **Rappel des prérequis :**
  - Notions de base en Python.
  - Compréhension des capteurs et actionneurs utilisés avec le Raspberry Pi.
  - Contexte des couleurs : spectres lumineux et perception RVB.

---

## 2. Approche Classique : Analyse des Écarts de Valeurs Mesurées

- **Principe de la méthode :**
  - Comparer les valeurs RVB mesurées par un capteur à des seuils prédéfinis pour classer les couleurs.

### Matériel nécessaire :
- Raspberry Pi.
- Capteur de couleur (TCS34725 ou équivalent).
- Servo-moteur pour trier les M&M's.

### Étapes :
1. **Mesurer les couleurs :** Exploiter le capteur pour obtenir des valeurs RVB des M&M's.
2. **Définir les seuils :** Établir une gamme de valeurs pour chaque couleur (rouge, vert, bleu, jaune).
3. **Programmer la logique conditionnelle :** Utiliser des instructions `if-else` pour diriger les M&M's vers des emplacements spécifiques.

### Limites de l'approche classique :
- Sensibilité aux variations de lumière.
- Difficulté à généraliser.

---

## 3. Introduction aux Modèles d'IA Classiques

- **Principe :**
  - Remplacer la logique conditionnelle par un modèle d'IA entraîné pour classer les couleurs.
  
### Modèles abordés :
- Régression logistique.
- Forêt aléatoire.
- k-Nearest Neighbors (k-NN).

### Étapes :
1. **Collecte de données :** Créer un dataset en mesurant des valeurs RVB et en annotant manuellement les couleurs.
2. **Entraînement des modèles :** Utiliser une bibliothèque comme `scikit-learn` pour entraîner un modèle sur les données collectées.
3. **Évaluation :** Comparer les performances des différents modèles sur des M&M's non vus pendant l'entraînement.
4. **Implémentation :** Intégrer le modèle choisi dans le programme pour trier les M&M's en temps réel.

### Discussion :
- **Avantages de l'IA sur les seuils fixes :** Meilleure adaptabilité et robustesse.

---

## 4. Exemple Avancé : Introduction au Deep Learning

- **Principe :**
  - Utiliser un réseau de neurones pour classer les couleurs avec davantage de flexibilité.

### Matériel et outils :
- Raspberry Pi (avec un accélérateur comme Google Coral pour le traitement en temps réel, si possible).
- Bibliothèque `TensorFlow` ou `PyTorch`.

### Étapes :
1. **Collecte et augmentation des données :** Capturer un dataset plus large, inclure des variations de luminosité, bruit, etc.
2. **Création d’un modèle simple :** Un réseau à plusieurs couches (MLP) pour traiter les données RVB.
3. **Entraînement :** Utiliser un ordinateur pour entraîner le modèle, puis déployer sur le Raspberry Pi.
4. **Optimisation :** Discuter des outils comme TensorFlow Lite pour optimiser le modèle pour l'embarqué.
5. **Évaluation finale :** Comparer les performances du deep learning avec les modèles classiques.

### Discussion :
- **Applications pratiques :** Tri automatisé dans l'industrie, reconnaissance d'images, domotique.
- **Limites :** Temps d'entraînement, besoin en données.

---

## 5. Conclusion et Ouverture

- **Résumé :**
  - Évolution des techniques : classique → modèles d'IA → deep learning.
  - Avantages et inconvénients de chaque approche.
- **Applications réelles :** Tri automatisé dans l'industrie, reconnaissance d'images, domotique.
- **Prolongements :** Intégrer des caméras pour détecter les formes ou textures en complément des couleurs.
- **Questions et perspectives :** Comment améliorer le modèle avec plus de données ou d'autres capteurs ?

---

## 6. Annexes et Ressources

- **Code Python :** Scripts pour chaque étape.
- **Datasets :** Exemples pour tester les modèles.
- **Références :**
  - Documentation scikit-learn.
  - Guides TensorFlow Lite.
  - Ressources pédagogiques complémentaires.
