# ezdxf est une bibliothèque Python pour créer des fichiers DXF (AutoCAD)
import ezdxf


class DXFGenerator:
    """
    Classe responsable de la génération de fichiers DXF (dessins techniques)
    pour un caisson, en vue de dessus et en vue de côté.
    """
    def __init__(
            self,
            largeur,
            hauteur,
            profondeur,
            epaisseur_montant,
            epaisseur_traverse,
            epaisseur_fond,
            porte=None,
            nombre_tablettes=0,
            tablettes=None
    ):
        """
        Initialise un générateur DXF avec tous les paramètres nécessaires.

        :param largeur: largeur totale du caisson (vue de dessus)
        :param hauteur: hauteur totale du caisson (vue de côté)
        :param profondeur: profondeur totale (vue de côté)
        :param epaisseur_montant: épaisseur des panneaux latéraux verticaux
        :param epaisseur_traverse: épaisseur des traverses hautes et basses
        :param epaisseur_fond: épaisseur du panneau arrière (fond)
        :param porte: instance d'une Porte (ou None si le caisson est sans porte)
        :param nombre_tablettes: nombre de tablettes à dessiner
        :param tablettes: liste d'instances de TabletteAmovible à dessiner
        """
        self.largeur = largeur
        self.hauteur = hauteur
        self.profondeur = profondeur
        self.epaisseur_montant = epaisseur_montant
        self.epaisseur_traverse = epaisseur_traverse
        self.epaisseur_fond = epaisseur_fond
        self.porte = porte
        self.nombre_tablettes = nombre_tablettes
        self.tablettes = tablettes or []  # liste des objets TabletteAmovible

    def generate_top_view(self, filename):
        """
        Génère la VUE DE DESSUS du caisson (en projection).

        :param filename: nom du fichier DXF à créer
        """
        # Alias pour simplifier la lecture
        L, P, M, F = self.largeur, self.profondeur, self.epaisseur_montant, self.epaisseur_fond
        offset = (self.porte.epaisseur + self.porte.jeu_avant) if self.porte else 0  # décalage si porte présente

        # Création d'un nouveau fichier DXF et d'un espace de dessin
        doc = ezdxf.new(dxfversion="R2010")
        msp = doc.modelspace()

        # Contour extérieur du caisson
        msp.add_lwpolyline([(0, 0), (L, 0), (L, P), (0, P)], close=True)

        # Fond du caisson
        msp.add_lwpolyline([(0, P - F), (L, P - F), (L, P), (0, P)], close=True)

        # Montants gauche et droit (panneaux verticaux)
        msp.add_lwpolyline([(0, offset), (M, offset), (M, P - F), (0, P - F)], close=True)
        msp.add_lwpolyline([(L - M, offset), (L, offset), (L, P - F), (L - M, P - F)], close=True)

        # Traverse basse (ligne horizontale)
        msp.add_line((M, offset), (L - M, offset))

        # Dessin de la porte (simple ou double)
        if self.porte:
            door = self.porte
            total_width = L - door.jeu_gauche - door.jeu_droit

            if door.type_porte == "simple":
                msp.add_lwpolyline([
                    (door.jeu_gauche, 0),
                    (door.jeu_gauche + total_width, 0),
                    (door.jeu_gauche + total_width, door.epaisseur),
                    (door.jeu_gauche, door.epaisseur)], close=True)

            elif door.type_porte == "double":
                gap = 3  # écart au centre
                single_width = (total_width - gap) / 2

                # Porte gauche
                msp.add_lwpolyline([
                    (door.jeu_gauche, 0),
                    (door.jeu_gauche + single_width, 0),
                    (door.jeu_gauche + single_width, door.epaisseur),
                    (door.jeu_gauche, door.epaisseur)], close=True)

                # Porte droite
                x_right = L - door.jeu_droit - single_width
                msp.add_lwpolyline([
                    (x_right, 0),
                    (x_right + single_width, 0),
                    (x_right + single_width, door.epaisseur),
                    (x_right, door.epaisseur)], close=True)

        # Représentation symbolique des tablettes (lignes horizontales)
        for tablette in self.tablettes:
            y = offset + 5  # position fixe, pourrait être améliorée avec tablette.position
            x1 = M + 0.5
            x2 = L - M - 0.5
            msp.add_line((x1, y), (x2, y))

        # Sauvegarde du fichier
        doc.saveas(filename)
        return filename

    def generate_side_view(self, filename):
        """
        Génère la VUE DE CÔTÉ du caisson, avec toutes les pièces internes visibles.

        :param filename: nom du fichier DXF à créer
        """
        # Aliases
        H, D, M, F = self.hauteur, self.profondeur, self.epaisseur_traverse, self.epaisseur_fond

        # Profondeur totale de la structure sans dépasser la porte
        structure_depth = D - (self.porte.epaisseur + self.porte.jeu_avant) if self.porte else D

        doc = ezdxf.new(dxfversion="R2010")
        msp = doc.modelspace()

        # Contour du caisson
        msp.add_lwpolyline([(0, 0), (D, 0), (D, H), (0, H)], close=True)

        # Panneau arrière
        msp.add_lwpolyline([(0, 0), (F, 0), (F, H), (0, H)], close=True)

        # Traverse basse
        msp.add_lwpolyline([(F, 0), (structure_depth, 0), (structure_depth, M), (F, M)], close=True)

        # Traverse haute
        msp.add_lwpolyline([(F, H - M), (structure_depth, H - M), (structure_depth, H), (F, H)], close=True)

        # Montant vertical avant (ligne de structure)
        msp.add_line((structure_depth, M), (structure_depth, H - M))

        # Porte (si présente)
        if self.porte:
            door = self.porte
            hauteur_porte = H - door.jeu_haut - door.jeu_bas
            x_door = structure_depth + door.jeu_avant
            msp.add_lwpolyline([
                (x_door, door.jeu_bas),
                (x_door + door.epaisseur, door.jeu_bas),
                (x_door + door.epaisseur, door.jeu_bas + hauteur_porte),
                (x_door, door.jeu_bas + hauteur_porte)], close=True)

        # Tablettes amovibles
        for tablette in self.tablettes:
            # Calcul des dimensions de la tablette à partir des dimensions internes du caisson
            largeur, profondeur, _, _, _ = tablette.get_dimensions(
                internal_width=self.largeur - 2 * self.epaisseur_montant,
                internal_depth=self.profondeur - self.epaisseur_fond - (
                    self.porte.epaisseur + self.porte.jeu_avant if self.porte else 0)
            )

            y = tablette.position  # position verticale
            x = self.epaisseur_fond  # contre le fond

            # Dessin de la tablette (rectangle plein)
            msp.add_lwpolyline([
                (x, y),
                (x + profondeur, y),
                (x + profondeur, y + tablette.epaisseur),
                (x, y + tablette.epaisseur)
            ], close=True)

        doc.saveas(filename)
        return filename
