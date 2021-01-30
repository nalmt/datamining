import csv
import sklearn
import numpy as np

# I - Lecture des données
from sklearn.datasets import make_classification

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


## II - Clusterisation

# Une méthode pour trouver les patterns qui ont le plus de succès, est de créer des clusters de jeux selon les ventes
# qu'ils ont atteintes, et de

# On charge les données
clusterisation_data = []
for elt in data:
    clusterisation_data.append([elt["Global_Sales"]])
clusterisation_data = np.asarray(clusterisation_data)

# On initialise les algorithmes de clusterisations et le nombre de clusters à tester

nb_clusters = [i for i in range(3, 20)]
for nb_clusters in range(3, 20):
    # kmeans(machin)
    # evaluation
    # AglomerativeClustering
    # evaluation
    pass


# COPIE DU TP ANS :

# On calcule la PCA
# SC = StandardScaler()
# SC.fit(X)
# X_norm = SC.transform(X)
#
# pca = PCA(n_components=12)
# pca.fit(X_norm)
# X_pca = pca.transform(X_norm)
#
# # On applique KMeans
# clusters = KMeans(n_clusters=3).fit_predict(X)
#
# colors = ['red','yellow','blue','pink']
# plt.scatter(X_pca[:, 0], X_pca[:, 1], c=clusters, cmap=matplotlib.colors.ListedColormap(colors))
# for label, x, y in zip(labels, X_pca[:, 0], X_pca[:, 1]):
# 	plt.annotate(label, xy=(x, y), xytext=(-0.2, 0.2), textcoords='offset points')
# plt.show()