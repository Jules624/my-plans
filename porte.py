class Porte:
    def __init__(self, type_porte: str, epaisseur: float,
                 jeu_gauche: float, jeu_droit: float,
                 jeu_haut: float, jeu_bas: float,
                 jeu_avant: float):
        """
        Initialise une porte avec ses paramètres.

        :param type_porte: 'simple' ou 'double'
        :param epaisseur: L'épaisseur du panneau de la porte.
        :param jeu_gauche: Écart sur le côté gauche (pour la vue de dessus).
        :param jeu_droit: Écart sur le côté droit (pour la vue de dessus).
        :param jeu_haut: Écart en haut (pour la vue de côté).
        :param jeu_bas: Écart en bas (pour la vue de côté).
        :param jeu_avant: Écart entre la porte et le chant avant du caisson (pour la vue de côté et/ou de dessus).
        """
        if type_porte not in ("simple", "double"):
            raise ValueError("type_porte doit être 'simple' ou 'double'")
        self.type_porte = type_porte
        self.epaisseur = epaisseur
        self.jeu_gauche = jeu_gauche
        self.jeu_droit = jeu_droit
        self.jeu_haut = jeu_haut
        self.jeu_bas = jeu_bas
        self.jeu_avant = jeu_avant

    def __str__(self):
        return (f"Porte({self.type_porte}, epaisseur={self.epaisseur}, "
                f"jeux: gauche={self.jeu_gauche}, droit={self.jeu_droit}, "
                f"haut={self.jeu_haut}, bas={self.jeu_bas}, avant={self.jeu_avant})")
