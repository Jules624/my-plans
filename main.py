import json
import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from caisson import Caisson
from models import CaissonCompleteParams
from porte import Porte  # Assure-toi que ce fichier est bien à jour
from project import Projet

projects_file = "projets.json"
app = FastAPI()

@app.post("/generer_caisson")
async def generer_caisson(params: CaissonCompleteParams):
    print(params)
    door = None
    if params.porte is not None:
        door = Porte(
            type_porte=params.porte.get("type_porte"),
            epaisseur=params.porte.get("epaisseur"),
            jeu_gauche=params.porte.get("jeu_gauche"),
            jeu_droit=params.porte.get("jeu_droit"),
            jeu_haut=params.porte.get("jeu_haut"),
            jeu_bas=params.porte.get("jeu_bas"),
            jeu_avant=params.porte.get("jeu_avant")
        )

    caisson = Caisson(
        nom=params.nom,
        largeur=params.largeur,
        hauteur=params.hauteur,
        profondeur=params.profondeur,
        quantite=params.quantite,
        epaisseur_montant=params.epaisseur_montant,
        epaisseur_fond=params.epaisseur_fond,
        epaisseur_traverse=params.epaisseur_traverse,
        porte=door
    )

    dxf_files = caisson.generate_dxf()

    if "error" in dxf_files:
        raise HTTPException(status_code=400, detail=dxf_files["error"])

    if os.path.exists(projects_file):
        with open(projects_file, "r") as f:
            projets = json.load(f)
    else:
        projets = []

    new_projet = caisson.to_dict()
    projets.append(new_projet)

    try:
        with open(projects_file, "w") as f:
            json.dump(projets, f, indent=4)
        print(f"Caisson added successfully to {projects_file}")

        # Optionnel : vérification du fichier JSON
        if os.path.exists(projects_file):
            with open(projects_file, "r") as f:
                data = json.load(f)
                if data and isinstance(data, list):
                    print("File exists and contains valid JSON data.")
                else:
                    print("Warning: File is empty or contains invalid data.")
        else:
            print(f"Error: File {projects_file} could not be created.")

    except Exception as e:
        print(f"Error while writing to {projects_file}: {e}")
        raise HTTPException(status_code=500, detail=f"Error while writing to {projects_file}: {e}")

    return {"message": "Caisson added successfully", "new_projet": new_projet}


@app.get("/projets")
def liste_projets():
    projets = Projet.charger("projets.json")
    return {
        "projets": [{
            "nom": p.nom,
            "description": p.description,
            "caissons": [{
                "nom": c.nom,
                "largeur": c.largeur,
                "hauteur": c.hauteur,
                "profondeur": c.profondeur,
                "quantite": c.quantite
            } for c in p.caissons]
        } for p in projets]
    }

@app.get("/projets/{nom}")
def liste_projet(nom: str):
    projets = Projet.charger("projets.json")
    print(projets)
    for p in projets:
        print("Projet trouvé:", p.nom)
        if p.nom.lower() == nom.lower():
            return {
                "nom": p.nom,
                "description": p.description,
                "caissons": [{
                    "nom": c.nom,
                    "largeur": c.largeur,
                    "hauteur": c.hauteur,
                    "profondeur": c.profondeur,
                    "quantite": c.quantite
                } for c in p.caissons]
            }
    raise HTTPException(status_code=404, detail=f"Projet {nom} n'existe pas")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
