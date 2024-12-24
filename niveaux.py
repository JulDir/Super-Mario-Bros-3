import numpy as np
from couleurs import *


class Niveau():

    def __init__(self):
        self.LARGEUR = 40
        self.HAUTEUR = 30
        self.TAILLE = (self.LARGEUR, self.HAUTEUR)

        self.blocs_solides_ = np.zeros(self.TAILLE).astype(bool)
        self.blocs_solides_[:,:2] = True
        self.blocs_solides_[10,5] = True
        self.blocs_solides_[11,6] = True
        self.blocs_solides_[14,3:9] = True

        self.blocs_solides = np.copy(self.blocs_solides_)

        self.fond = BLEU_CLAIR
        self.sol = VERT_CLAIR
