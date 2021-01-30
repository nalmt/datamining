# Analyse des tendances pour conseiller des développeurs de jeux vidéos

# Nous nous sommes demandés, si, grâce aux méthodes vu en cours, il était possible de connaître les tendances des jeux
# vidéos, et de conseiller aux développeurs des bonnes pratiques pour réaliser de bon chiffres de ventes.
#
# Malheureusement, les données que nous possédons ne montrent que peu d'informations sur les jeux en questions.
# Cependant, nous pouvons tout de même les utiliser pour connaître les genres et les plateformes (console) qui ont le plus
# de succès.
#
# ## I - Re-traitement des données
#
# La première étape consiste à générer un nouveau dataset à partir de deux autres.
# Le premier dataset, "DATA/vgsales" contient la plupart des informations dont nous avons besoins.
# Le second ("DATA/steam.csv") contient plus de jeux et plus de variables sur eux, mais ne concerne que les jeux vendus
# sur steam, et ne concerne donc qu'une seule plateforme. Cependant, il contient tout de même les dates de sortie de
# certains jeux qui sont inconnues dans le dataset initial (pour lesquels la valeur de la date vaut "N/A").
# Nous avons donc cherché à croiser ces données pour obtenir un troisième dataset.
#
# Nous profitons de la création de ce troisième dataset pour supprimer les collones que nous considérons comme inutiles,
# ou pour supprimer les lignes qui contiennent des données inconnues.
#
# Le code correspondant à cette étape se trouve dans le fichier "generate_data.py". Il consiste à générer un code .csv,
# qui est déjà généré. Il n'est donc pas nécessaire d'exécuter la cellule ci-dessous.

import os
import csv

# os.system('python3 generate_data.py')

# Maintenant que notre dataset a été généré, nous pouvons le charger.
# Pour cette partie du projet, nous ne prendrons que les jeux qui ont une date postérieure à 2012.
# En effet, l'objectif de cette partie est de conseiller des développeurs pour le développement d'un nouveau jeux.
#
# Les tendances antérieures à 2012 n'ont que peut d'intérêt pour nous.

data = []
with open('DATA/data_output.csv', mode='r') as infile:
    columns_keys = None
    reader = csv.reader(infile, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)

    for row in reader:
        if columns_keys is None:
            columns_keys = row
        else:
            elt = {}
            for index, _ in enumerate(columns_keys):
                elt[columns_keys[index]] = row[index]

            # Ici, on filtre les données
            if int(elt["Year"]) >= 2012:
                data.append(elt)

print("\n=================================================================\n")
print("    Affichage du dataset : ")
print("\n=================================================================\n")
print(data)


## II - Analyse en utilisant les fréquents et fermés.

# Une méthode pour trouver les patterns qui ont le plus de succès, est de connaitre pour chaque motif de catégories,
# les ventes moyennes de ces derniers, et de récupérer les motifs qui ont le meilleur score.
#
# Cependant, certaines variables ne nous intéressent pas. En effet, il n'est pas pertinent de savoir qu'un jeux en
# particulier (si le motif contient un titre) a eu beaucoup de succès.
#
# Ensuite, il est intéressant de conserver des fréquents qui ont un support minimum, pour éviter que les moyennes que nous
# réalisons soient basés sur peu d'apparitions, et soit donc moins fiables.
#
# Enfin, nous allons chercher à ne conserver que les fermés. Cela nous permet d'afficher pour chaque motif l'ensemble
# des caractéristiques qui ont influencées ce résultat.

# import csv

# Nous commençont par définir une fonction, qui pour chaque liste de paramètre, nous permettra de récupérer la liste des
# motifs possibles pour cette liste.

def getMotifs(line):
    """ Retourne tous les motifs d'une liste de valeurs donnée """
    # list to store all the sublists
    sublist = []
    for i in range(len(line) + 1):
        for j in range(i + 1, len(line) + 1):
            sli = line[i:j]  # make a slice of the subarray
            sublist.append(sli)  # add it to the list of sublists
    return sublist


# Nous pouvons désormais parcourir notre dataset pour compter les suport des motifs présent dans notre dataset.
# Nous effectuons un tris sur les colones, car certaines informations ne sont pas pertinentes pour l'objectif que nous
# recherchons

variables_to_use = ["Platform", "Genre", "Year"]
frequents = {}
for row_index, row in enumerate(data):
    complete_pattern = []
    for variable_key in variables_to_use:
        complete_pattern.append(row[variable_key])
    motifs = getMotifs(complete_pattern)  # remode globals sales that will be our value
    global_sales = row["Global_Sales"]

    for motif in motifs:
        key = tuple(motif)
        if key not in frequents:
            frequents[key] = {
                "total_sales": float(global_sales),
                "index_apparitions": [row_index],
                "support": 1
            }
        else:
            frequents[key]["total_sales"] += float(global_sales)
            frequents[key]["support"] += 1
            frequents[key]["index_apparitions"].append(row_index)

# Filtrage des fréquents
minsup = 20
filtered_frequents = []  # Nous créons une liste afin de pouvoir la filtrer
for motif, content in frequents.items():
    if content["support"] >= minsup:
        frequent = {
            "motif": motif,
            "average_sales": frequents[motif]["total_sales"] / frequents[motif]["support"],
            "total_sales": frequents[motif]["total_sales"],
            "index_apparitions": frequents[motif]["index_apparitions"],
            "support": frequents[motif]["support"]
        }
        filtered_frequents.append(frequent)
print("\n=================================================================\n")
print("    Affichage de " + str(len(filtered_frequents)) + " fréquents")
print("\n=================================================================\n")
for frequent in filtered_frequents:
    print(
        "Motif: " + str(frequent["motif"])
        + ", average_sales: " + str(frequent["average_sales"])
        + ", support: " + str(frequent["support"]))

# Maintenant que nous avons trouvé les fréquents, nous pouvons chercher les fermés, afin d'avoir un maximum
# d'informations sur les motifs que nous sélectionnons.

print("recherche de fermés ... \n")
closed_patterns = filtered_frequents.copy()
for motif in filtered_frequents:
    for potential_closure in filtered_frequents:
        if motif["index_apparitions"] == potential_closure["index_apparitions"] \
                and len(motif["motif"]) < len(potential_closure["motif"]):
            closed_patterns.remove(motif)

print("\n=================================================================\n")
print("    Affichage de " + str(len(closed_patterns)) + " fermés")
print("\n=================================================================\n")
for closed_pattern in closed_patterns:
    print(
        "Motif: " + str(closed_pattern["motif"])
        + ", average_sales: " + str(closed_pattern["average_sales"])
        + ", support: " + str(closed_pattern["support"]))
# Maintenant que nous avons des fréquents, nous pouvons les triers pour trouver ceux qui peuvent intéresser les
# développeurs de jeux vidéos, c'est à dire, les motifs de jeux qui se vendent le mieux

print("\n=================================================================\n")
print("    Affichage des fermés triés")
print("\n=================================================================\n")

closed_patterns.sort(key=lambda frequent: frequent["average_sales"], reverse=True)

for frequent in closed_patterns:
    print(
        "Motif: " + str(frequent["motif"]) + ", average_sales: " + str(frequent["average_sales"]) + ", support: " + str(
            frequent["support"]))
