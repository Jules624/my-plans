# initial_data.py
from project import Projet, Caisson

projets_init = []  # Renomme la variable pour clarifier son rôle

# Création d'un projet de test et ajout des caissons
projet_test = Projet("Cuisine", "Projet cuisine pour client XYZ")
caisson1 = Caisson("Caisson évier", 800, 700, 500, 2)
caisson2 = Caisson("Caisson four", 600, 700, 500, 1)
projet_test.ajouter_caisson(caisson1)
projet_test.ajouter_caisson(caisson2)
projets_init.append(projet_test)
