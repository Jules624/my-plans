from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class CaissonCompleteParams(BaseModel):
    nom: str = Field(..., description="Nom du caisson")
    largeur: float = Field(..., gt=0, description="Largeur totale du caisson (vue de dessus)")
    hauteur: float = Field(..., gt=0, description="Hauteur totale du caisson (vue de côté)")
    profondeur: float = Field(..., gt=0, description="Profondeur totale du caisson")
    epaisseur_montant: float = Field(..., gt=0, description="Épaisseur des montants (vue de côté)")
    epaisseur_traverse: float = Field(..., gt=0, description="Épaisseur des traverses (vue de côté)")
    epaisseur_fond: float = Field(..., gt=0, description="Épaisseur du fond (vue de côté)")
    quantite: int = Field(..., gt=0, description="Quantité")
    porte: Optional[Dict[str, Any]] = Field(
        None,
        description=(
            "Paramètres de la porte, si présente. "
            "Exemple pour une porte double : {\"type_porte\": \"double\", \"epaisseur\": 19, "
            "\"jeu_gauche\": 0, \"jeu_droit\": 0, \"jeu_haut\": 0, \"jeu_bas\": 0, \"jeu_avant\": 3}. "
            "Si ce champ n'est pas fourni, aucune porte ne sera intégrée."
        )
    )
    epaisseur_tablette: Optional[float] = Field(19, description="Épaisseur des tablettes amovibles (même pour toutes)")
    nombre_tablettes: Optional[int] = Field(0, description="Nombre de tablettes amovibles à intégrer")
