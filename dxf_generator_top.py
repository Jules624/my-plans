import ezdxf


def generer_dxf_top_view_caisson(largeur, profondeur, epaisseur_montant, epaisseur_fond,
                                 filename="caisson_top_view.dxf"):
    """
    Génère un fichier DXF représentant la vue de dessus d'un caisson avec :
      - Deux montants latéraux d'épaisseur 'epaisseur_montant'
      - Un fond à l'arrière d'épaisseur 'epaisseur_fond'
      - Une traverse basse (ligne reliant l'avant des montants)

    Paramètres :
      largeur          : largeur totale du caisson (mm)
      profondeur       : profondeur totale du caisson (mm)
      epaisseur_montant: épaisseur des montants (mm)
      epaisseur_fond   : épaisseur du fond (mm)
      filename         : nom du fichier DXF généré
    """
    L = largeur
    P = profondeur
    M = epaisseur_montant
    F = epaisseur_fond

    doc = ezdxf.new(dxfversion='R2010')
    msp = doc.modelspace()

    # Optionnel : tracer le contour extérieur du caisson pour repérer les dimensions
    msp.add_line((0, 0), (L, 0))
    msp.add_line((L, 0), (L, P))
    msp.add_line((L, P), (0, P))
    msp.add_line((0, P), (0, 0))

    # 1. Fond (panneau arrière) : Occupe toute la largeur, de y = P - F à y = P
    msp.add_line((0, P - F), (L, P - F))
    msp.add_line((L, P - F), (L, P))
    msp.add_line((L, P), (0, P))
    msp.add_line((0, P), (0, P - F))

    # 2. Montant gauche : de x = 0 à x = M, de y = 0 jusqu'à y = P - F
    msp.add_line((0, 0), (M, 0))
    msp.add_line((M, 0), (M, P - F))
    msp.add_line((M, P - F), (0, P - F))
    msp.add_line((0, P - F), (0, 0))

    # 3. Montant droit : de x = L - M à x = L, de y = 0 jusqu'à y = P - F
    msp.add_line((L - M, 0), (L, 0))
    msp.add_line((L, 0), (L, P - F))
    msp.add_line((L, P - F), (L - M, P - F))
    msp.add_line((L - M, P - F), (L - M, 0))

    # 4. Traverse basse : une ligne reliant le bord avant du montant gauche (x=M) au bord avant du montant droit (x=L-M) à y=0
    msp.add_line((M, 0), (L - M, 0))

    doc.saveas(filename)
    return filename


# Test rapide (à exécuter directement si besoin)
if __name__ == "__main__":
    # Exemple : caisson de 600mm x 500mm, montants de 19mm, fond de 8mm
    generer_dxf_top_view_caisson(600, 500, 19, 8, "caisson_top_view.dxf")
    print("Fichier DXF généré : caisson_top_view.dxf")
