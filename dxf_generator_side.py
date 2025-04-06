import ezdxf

def generer_dxf_side_view_caisson(hauteur, profondeur, epaisseur_montant, epaisseur_fond, filename="caisson_side_view.dxf"):
    """
    Génère un fichier DXF représentant la vue de côté d'un caisson.

    Paramètres :
      hauteur           : hauteur totale du caisson (mm) – dimension verticale de la vue
      profondeur        : profondeur totale du caisson (mm) – dimension horizontale de la vue
      epaisseur_montant : épaisseur des montants (mm)
      epaisseur_fond    : épaisseur du fond (mm) – utilisée pour le panneau gauche
      filename          : nom du fichier DXF généré

    Disposition dans la vue de côté :
      - Panneau gauche (fond) : rectangle de x = 0 à x = epaisseur_fond, sur toute la hauteur (0 à hauteur).
      - Panneau inférieur (montant inférieur) : rectangle de x = epaisseur_fond à x = profondeur, de y = 0 à y = epaisseur_montant.
      - Panneau supérieur (montant supérieur) : rectangle de x = epaisseur_fond à x = profondeur, de y = hauteur - epaisseur_montant à y = hauteur.
      - Traverse verticale sur le bord droit : ligne reliant (profondeur, epaisseur_montant) à (profondeur, hauteur - epaisseur_montant).
    """
    # H : hauteur totale de la vue, D : profondeur totale, M : épaisseur des montants, F : épaisseur du fond
    H = hauteur
    D = profondeur
    M = epaisseur_montant
    F = epaisseur_fond

    doc = ezdxf.new(dxfversion='R2010')
    msp = doc.modelspace()

    # Optionnel : tracer le contour extérieur de la vue de côté
    msp.add_line((0, 0), (D, 0))
    msp.add_line((D, 0), (D, H))
    msp.add_line((D, H), (0, H))
    msp.add_line((0, H), (0, 0))

    # 1. Panneau gauche (fond) – de x = 0 à x = F, sur toute la hauteur (0 à H)
    msp.add_line((0, 0), (F, 0))
    msp.add_line((F, 0), (F, H))
    msp.add_line((F, H), (0, H))
    msp.add_line((0, H), (0, 0))

    # 2. Panneau inférieur (montant inférieur) – de x = F à x = D, de y = 0 à y = M
    msp.add_line((F, 0), (D, 0))
    msp.add_line((D, 0), (D, M))
    msp.add_line((D, M), (F, M))
    msp.add_line((F, M), (F, 0))

    # 3. Panneau supérieur (montant supérieur) – de x = F à x = D, de y = H - M à y = H
    msp.add_line((F, H - M), (D, H - M))
    msp.add_line((D, H - M), (D, H))
    msp.add_line((D, H), (F, H))
    msp.add_line((F, H), (F, H - M))

    # 4. Traverse verticale sur le bord droit – ligne reliant (D, M) à (D, H - M)
    msp.add_line((D, M), (D, H - M))

    doc.saveas(filename)
    return filename

if __name__ == "__main__":
    # Exemple : caisson avec hauteur = 2000 mm, profondeur = 500 mm, montants de 19 mm et fond de 8 mm.
    generer_dxf_side_view_caisson(hauteur=2000, profondeur=500, epaisseur_montant=19, epaisseur_fond=8, filename="caisson_side_view.dxf")
    print("Fichier DXF généré : caisson_side_view.dxf")
