from fastapi import FastAPI
from models import CaissonCompleteParams
from caisson import Caisson
from project import Projet

app = FastAPI()

# Exemple : création d'un projet et ajout d'un caisson
projet = Projet("Projet Test", "Exemple de projet avec un caisson")
caisson = Caisson("Caisson Test", 600, 2000, 500, 1, epaisseur_montant=19, epaisseur_fond=8)
projet.ajouter_caisson(caisson)

@app.get("/")
def lire_projets():
    return {"projets": [{
        "nom": projet.nom,
        "description": projet.description,
        "caissons": [{
            "nom": c.nom,
            "dimensions": f"{c.largeur}x{c.hauteur}x{c.profondeur}",
            "quantite": c.quantite
        } for c in projet.caissons]
    }]}

@app.post("/generer_caisson_complet")
def generer_caisson(params: CaissonCompleteParams):
    caisson = Caisson(
        nom="Caisson Généré",
        largeur=params.largeur,
        hauteur=params.hauteur,
        profondeur=params.profondeur,
        quantite=1,
        epaisseur_montant=params.epaisseur_montant,
        epaisseur_fond=params.epaisseur_fond
    )
    fichiers = caisson.generate_dxf()
    return {"message": "DXF généré", "fichiers": fichiers}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
