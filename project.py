class Caisson:
    def __init__(self, nom, largeur, hauteur, profondeur, quantite):
        self.nom = nom
        self.largeur = largeur
        self.hauteur = hauteur
        self.profondeur = profondeur
        self.quantite = quantite

class Projet:
    def __init__(self, nom, description):
        self.nom = nom
        self.description = description
        self.caissons = []

    def ajouter_caisson(self, caisson):
        self.caissons.append(caisson)

    def afficher_caissons(self):
        for c in self.caissons:
            print(f"{c.nom}: {c.largeur}x{c.hauteur}x{c.profondeur} (Qté: {c.quantite})")


import json

def sauvegarder_projets(projets, file_path="projets.json"):
    data = []
    for projet in projets:
        caissons_data = []
        for c in projet.caissons:
            caissons_data.append({
                "nom": c.nom,
                "largeur": c.largeur,
                "hauteur": c.hauteur,
                "profondeur": c.profondeur,
                "quantite": c.quantite
            })
        data.append({
            "nom": projet.nom,
            "description": projet.description,
            "caissons": caissons_data
        })
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


def charger_projets(file_path="projets.json"):
    projets = []
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            for p in data:
                projet = Projet(p["nom"], p["description"])
                for c in p["caissons"]:
                    caisson = Caisson(
                        c["nom"],
                        c["largeur"],
                        c["hauteur"],
                        c["profondeur"],
                        c["quantite"]
                    )
                    projet.ajouter_caisson(caisson)
                projets.append(projet)
    except FileNotFoundError:
        # Si le fichier n'existe pas, renvoie une liste vide
        pass
    return projets


import ezdxf

def generer_dxf(caisson, filename="caisson.dxf"):
    """
    Génère un fichier DXF pour représenter une face (par exemple, la face avant) du caisson.
    """
    # Création d'un nouveau document DXF
    doc = ezdxf.new(dxfversion='R2010')
    msp = doc.modelspace()

    # Dessiner un rectangle représentant la face avant du caisson
    # On utilise la largeur et la hauteur du caisson pour définir le rectangle
    msp.add_line((0, 0), (caisson.largeur, 0))
    msp.add_line((caisson.largeur, 0), (caisson.largeur, caisson.hauteur))
    msp.add_line((caisson.largeur, caisson.hauteur), (0, caisson.hauteur))
    msp.add_line((0, caisson.hauteur), (0, 0))

    # Sauvegarder le document DXF avec le nom de fichier fourni
    doc.saveas(filename)
