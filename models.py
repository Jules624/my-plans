from pydantic import BaseModel

class CaissonCompleteParams(BaseModel):
    largeur: float         # Pour la vue de dessus (largeur totale)
    hauteur: float         # Pour la vue de côté (hauteur totale)
    profondeur: float      # Profondeur totale du caisson
    epaisseur_montant: float  # Épaisseur des montants pour la vue de côté
    epaisseur_fond: float     # Épaisseur du fond (ou traverses) pour la vue de côté
