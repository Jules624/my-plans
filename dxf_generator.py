import ezdxf

class DXFGenerator:
    def __init__(self, largeur, hauteur, profondeur, epaisseur_montant, epaisseur_fond, epaisseur_traverse):
        self.largeur = largeur       # Pour la vue de dessus
        self.hauteur = hauteur       # Pour la vue de côté
        self.profondeur = profondeur
        self.epaisseur_montant = epaisseur_montant
        self.epaisseur_fond = epaisseur_fond
        self.epaisseur_traverse = epaisseur_traverse

    def generate_top_view(self, filename):
        """Génère la vue de dessus (top) du caisson."""
        L = self.largeur
        P = self.profondeur
        M = self.epaisseur_montant
        F = self.epaisseur_fond

        doc = ezdxf.new(dxfversion='R2010')
        msp = doc.modelspace()

        # Contour extérieur
        msp.add_line((0, 0), (L, 0))
        msp.add_line((L, 0), (L, P))
        msp.add_line((L, P), (0, P))
        msp.add_line((0, P), (0, 0))

        # Fond (panneau arrière)
        msp.add_line((0, P - F), (L, P - F))
        msp.add_line((L, P - F), (L, P))
        msp.add_line((L, P), (0, P))
        msp.add_line((0, P), (0, P - F))

        # Montant gauche
        msp.add_line((0, 0), (M, 0))
        msp.add_line((M, 0), (M, P - F))
        msp.add_line((M, P - F), (0, P - F))
        msp.add_line((0, P - F), (0, 0))

        # Montant droit
        msp.add_line((L - M, 0), (L, 0))
        msp.add_line((L, 0), (L, P - F))
        msp.add_line((L, P - F), (L - M, P - F))
        msp.add_line((L - M, P - F), (L - M, 0))

        # Traverse basse
        msp.add_line((M, 0), (L - M, 0))

        doc.saveas(filename)
        return filename

    def generate_side_view(self, filename):
        """Génère la vue de côté (side) du caisson."""
        H = self.hauteur
        D = self.profondeur
        M = self.epaisseur_traverse
        F = self.epaisseur_fond

        doc = ezdxf.new(dxfversion='R2010')
        msp = doc.modelspace()

        # Contour extérieur
        msp.add_line((0, 0), (D, 0))
        msp.add_line((D, 0), (D, H))
        msp.add_line((D, H), (0, H))
        msp.add_line((0, H), (0, 0))

        # Panneau gauche (fond)
        msp.add_line((0, 0), (F, 0))
        msp.add_line((F, 0), (F, H))
        msp.add_line((F, H), (0, H))
        msp.add_line((0, H), (0, 0))

        # Traverse inférieur (panneau inférieur)
        msp.add_line((F, 0), (D, 0))
        msp.add_line((D, 0), (D, M))
        msp.add_line((D, M), (F, M))
        msp.add_line((F, M), (F, 0))

        # Montant supérieur (panneau supérieur)
        msp.add_line((F, H - M), (D, H - M))
        msp.add_line((D, H - M), (D, H))
        msp.add_line((D, H), (F, H))
        msp.add_line((F, H), (F, H - M))

        # Traverse verticale sur le bord droit
        msp.add_line((D, M), (D, H - M))

        doc.saveas(filename)
        return filename
