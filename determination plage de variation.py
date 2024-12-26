import csv

# Fonction pour calculer les plages de variation des couleurs
def calculate_color_ranges(file_path):
    color_data = {}

    # Lecture du fichier CSV
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Ignorer les en-têtes
        for row in reader:
            r, g, b, color = float(row[0]), float(row[1]), float(row[2]), row[3]
            if color not in color_data:
                color_data[color] = {"R": [], "G": [], "B": []}
            color_data[color]["R"].append(r)
            color_data[color]["G"].append(g)
            color_data[color]["B"].append(b)

    # Calcul des plages pour chaque couleur
    color_ranges = {}
    for color, channels in color_data.items():
        color_ranges[color] = {
            "R": (min(channels["R"]), max(channels["R"])),
            "G": (min(channels["G"]), max(channels["G"])),
            "B": (min(channels["B"]), max(channels["B"]))
        }

    return color_ranges

# Fonction principale
def main():
    file_path = "couleurs_echantillons.csv"  # Remplacez par le chemin de votre fichier CSV
    color_ranges = calculate_color_ranges(file_path)
    
    print("Plages de variation des couleurs :")
    for color, ranges in color_ranges.items():
        print(f"{color.capitalize()} :")
        print(f"  R (Rouge) : {ranges['R']}")
        print(f"  G (Vert)  : {ranges['G']}")
        print(f"  B (Bleu)  : {ranges['B']}")

# Exécution du script
if __name__ == "__main__":
    main()

