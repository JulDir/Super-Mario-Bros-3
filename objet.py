import numpy as np
from constantes import *
import mario
import niveaux
from collisions import *
from IA import *

# Variables

premiere_iteration = True

# Fonctions

def initialiser_objets(temps_maintenant):
    global liste_objets, premiere_iteration, temps_derniere_maj

    liste_objets = []
    premiere_iteration = False
    temps_derniere_maj = temps_maintenant


def creer_objet(type, position, vitesse, temps_maintenant, actif=False, delai_activation=1, delai_disparition=-1):
    global liste_objets

    objet = [type, position, vitesse, temps_maintenant, actif, delai_activation, delai_disparition]
    liste_objets.append(objet)

def creer_depuis_bloc(type, position_bloc, temps_maintenant):
    creer_objet(
        type=type,
        position=np.array(position_bloc, dtype=float),
        vitesse=np.array([0, vitesse_sortie_bloc(type)]),
        temps_maintenant=temps_maintenant,
        delai_activation=TEMPS_SORTIE_BLOC
        )

def vitesse_sortie_bloc(type):
    return VITESSE_SORTIE_BLOC[type-1]

def supprimer_objet(objet):
    global liste_objets
    liste_objets.remove(objet)


def mettre_a_jour_toutes_positions(temps_maintenant, niveau):
    global liste_objets, premiere_iteration, temps_derniere_maj

    if premiere_iteration:
        initialiser_objets(temps_maintenant)
        return

    blocs = niveaux.blocs(niveau)
    for objet in liste_objets:
        mettre_a_jour_position(objet, temps_maintenant, temps_derniere_maj, blocs)

    temps_derniere_maj = temps_maintenant


def mettre_a_jour_position(objet, temps_maintenant, temps_derniere_maj, blocs):
    global liste_objets

    # gestion limite de temps objets
    if objet[DELAI_DISPARITION] > 0 \
        and temps_maintenant - objet[MOMENT_APPARITION] >= objet[DELAI_DISPARITION]:
        supprimer_objet(objet)
        return

    # si objet sort écran
    if not est_charge(objet[POSITION], taille_objet(objet), mario.position_camera):
        supprimer_objet(objet)
        return

    # initialiser acceleration
    acceleration = np.zeros(2)

    # objet actif (utilisables & sensibles à la physique)
    if objet[ACTIF]:
        if mario.test_collision(objet[POSITION], taille_objet(objet)):
            mario.ramasse_objet(objet[TYPE])
            supprimer_objet(objet)
            return
        gerer_physique(objet, acceleration, blocs)
    # objets inactifs (sortie des blocs, etc.)
    elif objet[DELAI_ACTIVATION] > 0 \
        and temps_maintenant - objet[MOMENT_APPARITION] >= objet[DELAI_ACTIVATION]:
        activer(objet)

    # deplacements
    dt = temps_maintenant - temps_derniere_maj
    objet[POSITION] += objet[VITESSE] * dt + 0.5 * acceleration * dt**2
    objet[VITESSE]  += acceleration * dt


def activer(objet):
    objet[ACTIF] = True
    objet[VITESSE][H] = direction_H(objet[POSITION][H], mario.position[H]) * vitesse_objet(objet[TYPE])


def vitesse_objet(type):
    return VITESSE_OBJET[type-1]

def taille_objet(objet):
    return TAILLE_OBJET[objet[TYPE]-1]

def gerer_physique(objet, acceleration, blocs):

    # si touche sol
    if test_collision_bas_bloc(objet[POSITION], taille_objet(objet), blocs, bordure=False):
        au_sol = True
    else:
        au_sol = False

    # action de la gravité / normale du sol
    if au_sol and objet[TYPE] != FEUILLE:
        objet[VITESSE][V] = 0
        acceleration[V] = 0
    else:
        acceleration[V] = GRAVITATION

    # collision gauche/droite
    if (sens_vitesse(objet[VITESSE], H) == VERS_GAUCHE \
        and test_collision_gauche_bloc(objet[POSITION], taille_objet(objet), blocs, bordure=False)) \
            or (sens_vitesse(objet[VITESSE], H) == VERS_DROITE \
                and test_collision_droite_bloc(objet[POSITION], taille_objet(objet), blocs, bordure=False)):
        objet[VITESSE][H] = - objet[VITESSE][H]
