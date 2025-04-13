import os
from dxf_generator import DXFGenerator
from porte import Porte

class Caisson:
    def __init__(self, nom, largeur, hauteur, profondeur, quantite,
                 epaisseur_montant, epaisseur_traverse, epaisseur_fond,
                 porte=None, save_path="./dxf_files"):
        self.nom = nom
        self.largeur = largeur
        self.hauteur = hauteur
        self.profondeur = profondeur
        self.quantite = quantite
        self.epaisseur_montant = epaisseur_montant
        self.epaisseur_traverse = epaisseur_traverse
        self.epaisseur_fond = epaisseur_fond
        self.porte = porte  # Instance de Porte ou None
        self.save_path = save_path

        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

        # On passe l'objet porte au générateur DXF
        self.dxf_generator = DXFGenerator(largeur, hauteur, profondeur,
                                           epaisseur_montant, epaisseur_traverse,
                                           epaisseur_fond, porte=self.porte)

    def to_dict(self):
        # Vous pouvez compléter ce dictionnaire pour inclure des infos sur la porte si besoin
        return {
            "nom": self.nom,
            "largeur": self.largeur,
            "hauteur": self.hauteur,
            "profondeur": self.profondeur,
            "quantite": self.quantite,
            "epaisseur_montant": self.epaisseur_montant,
            "epaisseur_traverse": self.epaisseur_traverse,
            "epaisseur_fond": self.epaisseur_fond,
            # Optionnel : ajouter "porte" si elle est définie
            "porte": str(self.porte) if self.porte is not None else None
        }

    def generate_dxf(self):
        """Génère et renvoie les noms des fichiers DXF pour la vue de dessus et la vue de côté."""
        try:
            generated_files = []

            for i in range(self.quantite):
                filename_top = f"{self.nom.replace(' ', '_')}_top_{int(self.largeur)}x{int(self.profondeur)}_{i + 1}.dxf"
                filename_side = f"{self.nom.replace(' ', '_')}_side_{int(self.hauteur)}x{int(self.profondeur)}_{i + 1}.dxf"

                file_path_top = os.path.join(self.save_path, filename_top)
                file_path_side = os.path.join(self.save_path, filename_side)

                print(f"Generating DXF file for {self.nom}")
                print(f"Top view will be saved as {file_path_top}")
                print(f"Side view will be saved as {file_path_side}")

                self.dxf_generator.generate_top_view(file_path_top)
                self.dxf_generator.generate_side_view(file_path_side)

                if os.path.exists(file_path_top) and os.path.exists(file_path_side):
                    print(f"Successfully generated DXF files: {file_path_top}, {file_path_side}")
                else:
                    print(f"Failed to generate DXF files for {self.nom}")

                generated_files.append({"fichier_top": file_path_top, "fichier_side": file_path_side})

            return {"generated_files": generated_files}

        except Exception as e:
            print(f"An error occurred while generating DXF files: {str(e)}")
            return {"error": f"An error occurred while generating DXF files: {str(e)}"}
