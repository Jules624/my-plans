from pydantic import BaseModel, Field

class CaissonCompleteParams(BaseModel):
    nom: str = Field(..., description="Nom de la caisson")
    largeur: float = Field(..., gt=0, description="Largeur totale du caisson (vue de dessus)")
    hauteur: float = Field(..., gt=0, description="Hauteur totale du caisson (vue de côté)")
    profondeur: float = Field(..., gt=0, description="Profondeur totale du caisson")
    epaisseur_montant: float = Field(..., gt=0, description="Épaisseur des montants (vue de côté)")
    epaisseur_fond: float = Field(..., gt=0, description="Épaisseur du fond (vue de côté)")
    epaisseur_traverse: float = Field(..., gt=0, description="Épaisseur des traverses (vue de côté)")
    quantite: int = Field(..., gt=0, description="quantite")
