import numpy as np
from constantes import *


def sens_vitesse(vitesse, direction):
    return np.sign(vitesse[direction])

def position_relative(objet, taille_objet, reference, taille_reference):
    return position_relative_H(objet[H], taille_objet[H], reference[H], taille_reference[H]) \
        + position_relative_V(objet[V], taille_objet[V], reference[V], taille_reference[V])

def position_relative_H(objet, largeur_objet, reference, largeur_reference):
    if objet + largeur_objet/2 < reference - largeur_reference/2:
        return GAUCHE
    elif objet - largeur_objet/2 > reference + largeur_reference/2:
        return DROITE
    else:
        return CENTRE

def position_relative_V(objet, hauteur_objet, reference, hauteur_reference):
    if objet + hauteur_objet < reference:            # - HAUTEUR_BLOC/2 des 2 cotés
        return BAS
    elif objet > reference + hauteur_reference:      # - HAUTEUR_BLOC/2 des 2 cotés
        return HAUT
    else:
        return CENTRE

def direction_H(objet, reference, largeur_objet=0, largeur_reference=0):
    rel = position_relative_H(objet, largeur_objet, reference, largeur_reference)
    return VERS_DROITE if rel == DROITE else VERS_GAUCHE

def direction_V(objet, reference, hauteur_objet=0, hauteur_reference=0):
    rel = position_relative_V(objet, hauteur_objet, reference, hauteur_reference)
    return VERS_HAUT if rel == HAUT else VERS_BAS