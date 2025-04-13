class TabletteAmovible:
    def __init__(self, position: float, epaisseur: float):
        """
        Initialise une tablette amovible avec son épaisseur.

        :param position: Position verticale, en mm, depuis le bas de l'intérieur du caisson.
        :param epaisseur: Épaisseur de la tablette en mm.
        """
        self.position = position
        self.epaisseur = epaisseur

    def get_dimensions(self, internal_width: float, internal_depth: float):
        """
        Calcule les dimensions de la tablette amovible selon les contraintes :
        - Largeur tablette = internal_width - 1 mm,
        - Profondeur tablette = internal_depth - 5 mm,
        - Tablette centrée horizontalement, placée contre le fond.

        :param internal_width: Largeur intérieure du caisson en mm.
        :param internal_depth: Profondeur intérieure du caisson en mm.
        :return: Tuple (largeur_tablette, profondeur_tablette, marge_gauche, marge_droite, marge_fond).
        """
        largeur_tablette = internal_width - 1
        profondeur_tablette = internal_depth - 5
        marge_gauche = marge_droite = (internal_width - largeur_tablette) / 2
        marge_fond = 0

        return largeur_tablette, profondeur_tablette, marge_gauche, marge_droite, marge_fond

    def __str__(self):
        return f"TabletteAmovible(position={self.position}, epaisseur={self.epaisseur})"
