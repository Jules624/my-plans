import ezdxf

class DXFGenerator:
    def __init__(self, largeur, hauteur, profondeur, epaisseur_montant, epaisseur_traverse, epaisseur_fond, porte=None):
        self.largeur = largeur               # Pour la vue de dessus (largeur du caisson)
        self.hauteur = hauteur               # Pour la vue de côté (hauteur du caisson)
        self.profondeur = profondeur         # Pour la vue de dessus : profondeur du caisson, et pour la vue de côté : dimension hors tout
        self.epaisseur_montant = epaisseur_montant
        self.epaisseur_traverse = epaisseur_traverse
        self.epaisseur_fond = epaisseur_fond
        self.porte = porte                   # Instance de Porte ou None

    def generate_top_view(self, filename):
        """
        Vue de dessus :
          - L'enveloppe extérieure du caisson est dessinée de 0 à L horizontalement et de 0 à P verticalement.
          - Le panneau arrière est tracé sur la zone P-F à P.
          - Si une porte est définie, la structure interne (montants et traverse) est décalée
            d'un offset = door.epaisseur + door.jeu_avant pour réserver la zone de la porte.
          - La porte est dessinée en overlay sur la façade, de y = door.jeu_avant jusqu'à y = door.jeu_avant + door.epaisseur.
        """
        L = self.largeur
        P = self.profondeur
        M = self.epaisseur_montant
        F = self.epaisseur_fond

        # Calcul de l'offset pour la structure interne (si une porte existe)
        if self.porte is not None:
            offset = self.porte.epaisseur + self.porte.jeu_avant
        else:
            offset = 0

        doc = ezdxf.new(dxfversion='R2010')
        msp = doc.modelspace()

        # 1. Enveloppe extérieure (cote hors tout)
        # msp.add_line((0, 0), (L, 0))
        # msp.add_line((L, 0), (L, P))
        # msp.add_line((L, P), (0, P))
        # msp.add_line((0, P), (0, 0))

        # 2. Panneau arrière (fond)
        msp.add_line((0, P - F), (L, P - F))
        msp.add_line((L, P - F), (L, P))
        msp.add_line((L, P), (0, P))
        msp.add_line((0, P), (0, P - F))

        # 3. Structure interne (montants et traverse)
        # On décalera la structure vers l'arrière de l'offset pour laisser la zone de la porte en façade.
        # Montant gauche
        msp.add_line((0, offset), (M, offset))
        msp.add_line((M, offset), (M, P - F))
        msp.add_line((M, P - F), (0, P - F))
        msp.add_line((0, P - F), (0, offset))
        # Montant droit
        msp.add_line((L - M, offset), (L, offset))
        msp.add_line((L, offset), (L, P - F))
        msp.add_line((L, P - F), (L - M, P - F))
        msp.add_line((L - M, P - F), (L - M, offset))
        # Traverse basse (entre montants)
        msp.add_line((M, offset), (L - M, offset))

        # 4. Dessin de la porte en vue de dessus (overlay sur la façade)
        if self.porte is not None:
            door = self.porte
            y_door = 0  # La porte commence à 0, de façon à être alignée sur le bord avant,
            # et le gap (door.jeu_avant) apparaîtra entre le bas de la porte et la structure.
            if door.type_porte == "simple":
                door_width = L - (door.jeu_gauche + door.jeu_droit)
                msp.add_line((door.jeu_gauche, y_door), (door.jeu_gauche + door_width, y_door))
                msp.add_line((door.jeu_gauche + door_width, y_door), (door.jeu_gauche + door_width, y_door + door.epaisseur))
                msp.add_line((door.jeu_gauche + door_width, y_door + door.epaisseur), (door.jeu_gauche, y_door + door.epaisseur))
                msp.add_line((door.jeu_gauche, y_door + door.epaisseur), (door.jeu_gauche, y_door))
            elif door.type_porte == "double":
                total_door_width = L - (door.jeu_gauche + door.jeu_droit)
                gap = 3  # écart fixe entre les deux panneaux
                single_width = (total_door_width - gap) / 2
                # Panneau gauche
                msp.add_line((door.jeu_gauche, y_door), (door.jeu_gauche + single_width, y_door))
                msp.add_line((door.jeu_gauche + single_width, y_door), (door.jeu_gauche + single_width, y_door + door.epaisseur))
                msp.add_line((door.jeu_gauche + single_width, y_door + door.epaisseur), (door.jeu_gauche, y_door + door.epaisseur))
                msp.add_line((door.jeu_gauche, y_door + door.epaisseur), (door.jeu_gauche, y_door))
                # Panneau droit
                x_start = L - door.jeu_droit - single_width
                msp.add_line((x_start, y_door), (x_start + single_width, y_door))
                msp.add_line((x_start + single_width, y_door), (x_start + single_width, y_door + door.epaisseur))
                msp.add_line((x_start + single_width, y_door + door.epaisseur), (x_start, y_door + door.epaisseur))
                msp.add_line((x_start, y_door + door.epaisseur), (x_start, y_door))
        doc.saveas(filename)
        return filename

    def generate_side_view(self, filename):
        """
        Vue de côté :
          - L'enveloppe extérieure (0 <= x <= D) est tracée.
          - La structure interne (panneaux, montants) est dessinée dans une zone réduite,
            de x = F jusqu'à x = structure_depth + door.jeu_avant,
            où structure_depth = D - (door.epaisseur + door.jeu_avant) si une porte est présente.
          - La porte est ensuite dessinée dans l'espace restant, de x = structure_depth + door.jeu_avant jusqu'à x = structure_depth + door.jeu_avant + door.epaisseur.
          - La hauteur visible de la porte est : door_height = H - (door.jeu_haut + door.jeu_bas).
        """
        H = self.hauteur
        D = self.profondeur
        M = self.epaisseur_traverse
        F = self.epaisseur_fond

        # Calcul de la profondeur utile de la structure
        if self.porte is not None:
            door = self.porte
            structure_depth = D - (door.epaisseur + door.jeu_avant)
        else:
            structure_depth = D

        doc = ezdxf.new(dxfversion='R2010')
        msp = doc.modelspace()

        # 1. Enveloppe extérieure (cote hors tout)
        # msp.add_line((0, 0), (D, 0))
        # msp.add_line((D, 0), (D, H))
        # msp.add_line((D, H), (0, H))
        # msp.add_line((0, H), (0, 0))

        # 2. Panneau gauche (fond)
        msp.add_line((0, 0), (F, 0))
        msp.add_line((F, 0), (F, H))
        msp.add_line((F, H), (0, H))
        msp.add_line((0, H), (0, 0))

        # 3. Structure interne (traverse inférieure et montants supérieurs)
        # Traverse inférieure
        msp.add_line((F, 0), (structure_depth, 0))
        msp.add_line((structure_depth, 0), (structure_depth, M))
        msp.add_line((structure_depth, M), (F, M))
        msp.add_line((F, M), (F, 0))
        # Montants supérieurs
        msp.add_line((F, H - M), (structure_depth, H - M))
        msp.add_line((structure_depth, H - M), (structure_depth, H))
        msp.add_line((structure_depth, H), (F, H))
        msp.add_line((F, H), (F, H - M))
        # Traverse verticale côté droit
        msp.add_line((structure_depth, M), (structure_depth, H - M))

        # 4. Dessin de la porte en vue de côté, si définie
        if self.porte is not None:
            door = self.porte
            door_height = H - (door.jeu_haut + door.jeu_bas)
            # Pour respecter la cote hors tout, on place la porte dans l'espace restant à l'avant.
            # On positionne x_origin = structure_depth + door.jeu_avant, de façon à laisser le jeu avant.
            x_origin = structure_depth + door.jeu_avant
            msp.add_line((x_origin, door.jeu_bas), (x_origin + door.epaisseur, door.jeu_bas))
            msp.add_line((x_origin + door.epaisseur, door.jeu_bas), (x_origin + door.epaisseur, door.jeu_bas + door_height))
            msp.add_line((x_origin + door.epaisseur, door.jeu_bas + door_height), (x_origin, door.jeu_bas + door_height))
            msp.add_line((x_origin, door.jeu_bas + door_height), (x_origin, door.jeu_bas))
        doc.saveas(filename)
        return filename
