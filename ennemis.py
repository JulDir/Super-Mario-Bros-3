import numpy as np
from collisions import *
from constantes import *


# Variables

premiere_iteration = True

# Fonctions

def initialiser_ennemis(temps_maintenant):
    global liste_ennemis, liste_points_apparition, premiere_iteration, temps_derniere_maj

    liste_ennemis = []
    liste_points_apparition = {}
    premiere_iteration = False
    temps_derniere_maj = temps_maintenant


def creer_ennemi(type, position, vitesse, temps_maintenant, delai_disparition=-1, etat=[]):
    global liste_ennemis

    position_ = np.array(position, dtype=float)
    vitesse_  = np.array(vitesse, dtype=float)
    etat_     = list(etat)
    ennemi = [
        type,
        position_,
        vitesse_,
        temps_maintenant,
        delai_disparition,
        etat_,
        np.copy(position_)
        ]
    liste_ennemis.append(ennemi)


def creer_point_apparition(type, position, vitesse):
    global liste_points_apparition

    position_ = np.array(position, dtype=float)
    vitesse_  = np.array(vitesse, dtype=float)

    liste_points_apparition[position_] = (type, vitesse_, False)


def supprimer_ennemi(ennemi):
    global liste_ennemis, liste_points_apparition
    liste_points_apparition[ennemi[POINT_APPARITION]][ENNEMI_EN_VIE] = False
    liste_ennemis.remove(ennemi)


def taille_ennemi(type):
    return TAILLE_ENNEMI(-type-1)

def gerer_chargement_ennemis(position_camera, temps_maintenant):
    global liste_ennemis, liste_points_apparition

    for ennemi in liste_ennemis:
        if not est_charge(ennemi[POSITION], taille_ennemi(ennemi[TYPE]), position_camera) \
            or (ennemi[DELAI_DISPARITION] > 0 \
                and temps_maintenant - ennemi[MOMENT_APPARITION] >= ennemi[DELAI_DISPARITION]):
            supprimer_ennemi(ennemi)

    for position in liste_points_apparition:
        point_apparition = liste_points_apparition[position]
        if not point_apparition[ENNEMI_EN_VIE]:
            type = point_apparition[TYPE_APPARITION]
            taille = taille_ennemi(type)
            if est_charge(position, taille, position_camera) \
                and not est_dans_ecran(position, taille, position_camera):
                creer_ennemi(type, position, point_apparition[VITESSE_APPARITION], temps_maintenant)