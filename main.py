from fastapi import FastAPI
from project import Projet, Caisson, sauvegarder_projets, charger_projets, generer_dxf
from initial_data import projets_init
from models import CaissonCompleteParams, CaissonCompleteParams
from dxf_generator_top import generer_dxf_top_view_caisson
from dxf_generator_side import generer_dxf_side_view_caisson

app = FastAPI()

# Utilisation des données d'exemple
# (Assure-toi que projets_init est une liste de projets déjà définie dans initial_data.py)
projets = projets_init


@app.get("/")
def lire_projets():
    result = []
    for projet in projets:
        caissons = []
        for c in projet.caissons:
            caissons.append({
                "nom": c.nom,
                "dimensions": f"{c.largeur}x{c.hauteur}x{c.profondeur}",
                "quantite": c.quantite
            })
        result.append({
            "nom": projet.nom,
            "description": projet.description,
            "caissons": caissons
        })
    return {"projets": result}


@app.post("/sauvegarder")
def sauvegarder():
    sauvegarder_projets(projets)
    return {"message": "Les projets ont été sauvegardés avec succès."}


@app.get("/charger")
def charger():
    global projets
    projets = charger_projets()
    return {"message": "Projets chargés", "nombre": len(projets)}


@app.get("/dxf/{nom_caisson}")
def generer_dxf_endpoint(nom_caisson: str):
    """
    Cherche un caisson par son nom et génère un fichier DXF pour ce caisson.
    """
    for projet in projets:
        for c in projet.caissons:
            if c.nom.lower() == nom_caisson.lower():
                filename = f"{c.nom.replace(' ', '_')}.dxf"
                generer_dxf(c, filename)
                return {"message": f"DXF généré pour {c.nom}", "fichier": filename}
    return {"message": "Caisson non trouvé"}


@app.post("/generer_caisson_complet")
def generer_caisson_complet(params: CaissonCompleteParams):
    """
    Génère en une seule fois la vue de dessus et la vue de côté d'un caisson.

    Le modèle CaissonCompleteParams contient :
      - largeur: pour la vue de dessus,
      - hauteur: pour la vue de côté,
      - profondeur: dimension commune,
      - epaisseur_montant: épaisseur des montants pour la vue de côté,
      - epaisseur_fond: épaisseur du fond pour la vue de côté.
    """
    # Vue de dessus
    filename_top = f"caisson_top_{int(params.largeur)}x{int(params.profondeur)}.dxf"
    generer_dxf_top_view_caisson(
        largeur=params.largeur,
        epaisseur_montant=params.epaisseur_montant,
        epaisseur_fond=params.epaisseur_fond,
        profondeur=params.profondeur,
        filename=filename_top
    )

    # Vue de côté
    filename_side = f"caisson_side_{int(params.hauteur)}x{int(params.profondeur)}.dxf"
    generer_dxf_side_view_caisson(
        hauteur=params.hauteur,
        profondeur=params.profondeur,
        epaisseur_montant=params.epaisseur_montant,
        epaisseur_fond=params.epaisseur_fond,
        filename=filename_side
    )

    return {
        "message": "DXF complet généré avec succès",
        "fichier_top": filename_top,
        "fichier_side": filename_side
    }
