import os
from dxf_generator import DXFGenerator
from porte import Porte
from tablette_amovible import TabletteAmovible


class Caisson:
    def __init__(self, nom, largeur, hauteur, profondeur, quantite,
                 epaisseur_montant, epaisseur_traverse, epaisseur_fond,
                 porte=None, nombre_tablettes=0, epaisseur_tablette=19, save_path="./dxf_files"):
        self.nom = nom
        self.largeur = largeur
        self.hauteur = hauteur
        self.profondeur = profondeur
        self.quantite = quantite
        self.epaisseur_montant = epaisseur_montant
        self.epaisseur_traverse = epaisseur_traverse
        self.epaisseur_fond = epaisseur_fond
        self.porte = porte  # Instance de Porte ou None
        self.epaisseur_tablette = epaisseur_tablette
        self.nombre_tablettes = nombre_tablettes  # Nombre de tablettes à dessiner
        self.save_path = save_path

        # Debug : affichage des paramètres de base
        print(f"[DEBUG] Initialisation du caisson: {self.nom}")
        print(f"[DEBUG] Dimensions: {self.largeur} x {self.hauteur} x {self.profondeur}")
        print(
            f"[DEBUG] Epaisseurs - Montants: {self.epaisseur_montant}, Traverse: {self.epaisseur_traverse}, Fond: {self.epaisseur_fond}")
        if self.porte:
            print(f"[DEBUG] Objet Porte: {self.porte}")
        else:
            print("[DEBUG] Aucune porte définie")
        print(f"[DEBUG] Nombre de tablettes: {self.nombre_tablettes}")

        # Répartition équitable des tablettes avec objets TabletteAmovible
        self.tablettes = []
        if self.nombre_tablettes > 0:
            hauteur_dispo = self.hauteur - 2 * self.epaisseur_traverse
            espace_total = hauteur_dispo - (self.nombre_tablettes * self.epaisseur_tablette)
            espacement = espace_total / (self.nombre_tablettes + 1)
            position = self.epaisseur_traverse + espacement
            for _ in range(self.nombre_tablettes):
                tablette = TabletteAmovible(position=position, epaisseur=self.epaisseur_tablette)
                self.tablettes.append(tablette)
                position += self.epaisseur_tablette + espacement
        # Création du dossier de sortie s'il n'existe pas
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
            print(f"[DEBUG] Création du dossier {self.save_path}")

        # Initialisation du générateur DXF avec les paramètres, y compris la porte et le nombre de tablettes.
        self.dxf_generator = DXFGenerator(
            largeur,
            hauteur,
            profondeur,
            epaisseur_montant,
            epaisseur_traverse,
            epaisseur_fond,
            porte=self.porte,
            tablettes=self.tablettes
        )
        print("[DEBUG] Générateur DXF initialisé.")

    def to_dict(self):
        return {
            "nom": self.nom,
            "largeur": self.largeur,
            "hauteur": self.hauteur,
            "profondeur": self.profondeur,
            "quantite": self.quantite,
            "epaisseur_montant": self.epaisseur_montant,
            "epaisseur_traverse": self.epaisseur_traverse,
            "epaisseur_fond": self.epaisseur_fond,
            "porte": str(self.porte) if self.porte is not None else None,
            "nombre_tablettes": self.nombre_tablettes
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

                print(f"[DEBUG] Génération du DXF pour '{self.nom}' (exemple {i + 1})")
                print(f"[DEBUG] Vue de dessus: {file_path_top}")
                print(f"[DEBUG] Vue de côté: {file_path_side}")

                self.dxf_generator.generate_top_view(file_path_top)
                self.dxf_generator.generate_side_view(file_path_side)

                if os.path.exists(file_path_top) and os.path.exists(file_path_side):
                    print(f"[DEBUG] Fichiers générés avec succès : {file_path_top} et {file_path_side}")
                else:
                    print(f"[ERROR] Échec de la génération pour {self.nom}")

                generated_files.append({"fichier_top": file_path_top, "fichier_side": file_path_side})

            return {"generated_files": generated_files}
        except Exception as e:
            print(f"[ERROR] Erreur lors de la génération des fichiers DXF : {str(e)}")
            return {"error": f"Erreur lors de la génération des fichiers DXF : {str(e)}"}
