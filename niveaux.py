import numpy as np
from collisions import *
from constantes import *
from couleurs import *


def creer_niveau(sol, blocs, ennemis, decors=PLAINE):
    taille = sol.shape
    if taille != blocs.shape or taille != ennemis.shape:
        print("taille incompatible")
        return
    niveau = [
        blocs,
        ennemis,
        decors
    ]
    return niveau

class Niveau():
    # classe temporaire pour les tests

    def __init__(self):
        self.LARGEUR = 40
        self.HAUTEUR = 30
        self.TAILLE = (self.LARGEUR, self.HAUTEUR)

        self.blocs_sol = np.zeros(self.TAILLE).astype(bool)
        self.blocs_sol[:,:2] = True
        self.blocs_sol[20:23, :] = False

        self.blocs_briques_ = np.zeros_like(self.blocs_sol).astype(bool)
        self.blocs_briques_[8:12, 5] = True

        self.blocs_briques = np.copy(self.blocs_briques_)
        self.blocs_solides = self.blocs_briques | self.blocs_sol

        self.fond = BLEU_CLAIR
        self.sol  = VERT_CLAIR

    def frapper_bloc(self, position_mario, etat_mario):
        x, y = position_mario
        x_b, y_b = round(x), round(y + TAILLE_MARIO[etat_mario][V])
        if not self.blocs_briques[x_b, y_b]:
            xg, xm, xd = generate_rays_references_x(position_mario, LARGEUR_MARIO)
            x_b = round(xg) if round(xd) == x_b else round(xd)
        
        if etat_mario != PETIT:
            self.blocs_briques[x_b, y_b] = False
        self.blocs_solides = self.blocs_briques | self.blocs_sol
