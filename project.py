import json

from caisson import Caisson


class Projet:
    def __init__(self, nom, description, caissons=None):
        self.nom = nom
        self.description = description
        self.caissons = caissons or []

    def ajouter_caisson(self, caisson: Caisson):
        self.caissons.append(caisson)

    def afficher_caissons(self):
        for c in self.caissons:
            print(f"{c.nom}: {c.largeur}x{c.hauteur}x{c.profondeur} (Qté: {c.quantite})")

    def sauvegarder(self, file_path="projets_old.json"):
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
    def charger(file_path):
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
                projets = []
                for projet_data in data:
                    caissons = [
                        Caisson(
                            nom=caisson["nom"],
                            largeur=caisson.get["largeur"],
                            hauteur=caisson.get["hauteur"],
                            profondeur=caisson.get("profondeur"),  # Corrected this line
                            quantite=caisson["quantite"],
                            epaisseur_montant=caisson.get("epaisseur_montant", 19),  # Default to 19 if missing
                            epaisseur_traverse=caisson.get("epaisseur_traverse", 19),  # Default to 19 if missing
                            epaisseur_fond=caisson.get("epaisseur_fond", 8)  # Default to 8 if missing
                        ) for caisson in projet_data["caissons"]
                    ]
                    projets.append(
                        Projet(nom=projet_data["nom"], description=projet_data["description"], caissons=caissons)
                    )
                return projets
        except Exception as e:
            print(f"Error loading projects: {e}")
            return []
