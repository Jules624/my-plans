from fastapi import FastAPI
from project import Projet, Caisson, sauvegarder_projets, charger_projets, generer_dxf
from initial_data import projets_init

app = FastAPI()

# Initialisation de la liste des projets avec les données d'exemple
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
                # Créer un nom de fichier basé sur le nom du caisson
                filename = f"{c.nom.replace(' ', '_')}.dxf"
                generer_dxf(c, filename)
                return {"message": f"DXF généré pour {c.nom}", "fichier": filename}
    return {"message": "Caisson non trouvé"}
