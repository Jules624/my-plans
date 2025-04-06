import json
from caisson import Caisson

class Projet:
    def __init__(self, nom, description):
        self.nom = nom
        self.description = description
        self.caissons = []

    def ajouter_caisson(self, caisson: Caisson):
        self.caissons.append(caisson)

    def afficher_caissons(self):
        for c in self.caissons:
            print(f"{c.nom}: {c.largeur}x{c.hauteur}x{c.profondeur} (Qté: {c.quantite})")

    def sauvegarder(self, file_path="projets.json"):
        data = [{
            "nom": self.nom,
            "description": self.description,
            "caissons": [{
                "nom": c.nom,
                "largeur": c.largeur,
                "hauteur": c.hauteur,
                "profondeur": c.profondeur,
                "quantite": c.quantite
            } for c in self.caissons]
        }]
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
        return file_path

    @staticmethod
    def charger(file_path="projets.json"):
        projets = []
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
                for p in data:
                    projet = Projet(p["nom"], p["description"])
                    for c in p["caissons"]:
                        # Ici, on utilise des épaisseurs par défaut (à adapter selon tes besoins)
                        caisson = Caisson(c["nom"], c["largeur"], c["hauteur"], c["profondeur"], c["quantite"], 19, 8)
                        projet.ajouter_caisson(caisson)
                    projets.append(projet)
        except FileNotFoundError:
            pass
        return projets
