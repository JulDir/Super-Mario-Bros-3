import numpy as np
from couleurs import *


class Niveau():

    def __init__(self):
        self.LARGEUR = 40
        self.HAUTEUR = 30
        self.TAILLE = (self.LARGEUR, self.HAUTEUR)

        self.blocs_sol = np.zeros(self.TAILLE).astype(bool)
        self.blocs_sol[:,:2] = True
        self.blocs_sol[20:23, :] = False

        self.blocs_brique_ = np.zeros_like(self.blocs_sol).astype(bool)
        self.blocs_brique_[8:12, 5] = True

        self.blocs_brique = np.copy(self.blocs_brique_)
        self.blocs_solides = self.blocs_brique | self.blocs_sol

        self.fond = BLEU_CLAIR
        self.sol  = VERT_CLAIR
