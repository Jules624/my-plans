from dxf_generator import DXFGenerator

class Caisson:
    def __init__(self, nom, largeur, hauteur, profondeur, quantite, epaisseur_montant, epaisseur_fond):
        self.nom = nom
        self.largeur = largeur
        self.hauteur = hauteur
        self.profondeur = profondeur
        self.quantite = quantite
        self.epaisseur_montant = epaisseur_montant
        self.epaisseur_fond = epaisseur_fond

        # Associe le générateur DXF aux dimensions du caisson
        self.dxf_generator = DXFGenerator(largeur, hauteur, profondeur, epaisseur_montant, epaisseur_fond)

    def generate_dxf(self):
        """Génère et renvoie les noms des fichiers DXF pour la vue de dessus et la vue de côté."""
        filename_top = f"{self.nom.replace(' ', '_')}_top_{int(self.largeur)}x{int(self.profondeur)}.dxf"
        filename_side = f"{self.nom.replace(' ', '_')}_side_{int(self.hauteur)}x{int(self.profondeur)}.dxf"

        self.dxf_generator.generate_top_view(filename_top)
        self.dxf_generator.generate_side_view(filename_side)
        return {"fichier_top": filename_top, "fichier_side": filename_side}
