import numpy as np
import objet
from collisions import *
from constantes import *
from couleurs import *


def creer_niveau(blocs, plateformes = None, entites = None, decors=PLAINE):
    blocs_ = np.array(blocs, dtype=int)
    if plateformes is not None:
        plateformes_ = np.array(plateformes, dtype=int)
    else:
        plateformes_ = np.zeros_like(blocs_)
    if entites is not None:
        entites_ = np.array(entites, dtype=int)
    else:
        entites_ = np.zeros_like(blocs_)

    niveau = [
        blocs_,
        plateformes_,
        entites_,
        decors,
        np.copy(blocs_)
    ]
    return niveau

def taille(niveau):
    return niveau[BLOCS].shape

def blocs(niveau):
    filtre = niveau[BLOCS] != BLOC_AIR
    return filtre

def blocs_sol(niveau):
    filtre = niveau[BLOCS] == BLOC_SOL
    return filtre

def blocs_non_sol(niveau):
    filtre1 = niveau[BLOCS] != BLOC_AIR
    filtre2 = niveau[BLOCS] != BLOC_SOL
    return filtre1 & filtre2

def briques(niveau):
    filtre = niveau[BLOCS] == BLOC_BRIQUE
    return filtre

def blocs_mysteres(niveau):
    filtre = niveau[BLOCS] == BLOC_MYSTERE
    return filtre

def blocs_frappables(niveau):
    return briques(niveau) | blocs_mysteres(niveau)

def trouver_bloc(niveau, position_mario, etat_mario):
    bloc_existe = blocs(niveau)
    x, y = position_mario

    x_b, y_b = round(x), round(y + TAILLE_MARIO[etat_mario][V])
    if not bloc_existe[x_b, y_b]:
        xg, xm, xd = generate_rays_references_x(position_mario, LARGEUR_MARIO)
        x_b = round(xg) if round(xd) == x_b else round(xd)
    return (x_b, y_b)

def frapper_bloc(niveau, position_mario, etat_mario, temps_maintenant):
    est_frappables = blocs_frappables(niveau)
    est_brique  = briques(niveau)

    x_b, y_b = trouver_bloc(niveau, position_mario, etat_mario)
    if not est_frappables[x_b, y_b]:
        return

    if niveau[ENTITES][x_b, y_b] != 0:
        # objet dans bloc
        objet.creer_depuis_bloc(niveau[ENTITES][x_b, y_b], (x_b, y_b), temps_maintenant)
        niveau[BLOCS][x_b, y_b] = BLOC_VIDE
    elif est_brique[x_b, y_b] and etat_mario != PETIT:
        # casser brique
        niveau[BLOCS][x_b, y_b] = BLOC_AIR