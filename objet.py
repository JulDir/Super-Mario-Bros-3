import numpy as np
from constantes import *
import mario
from collisions import *
from IA import *

# Variables

premiere_iteration = True

# Sprites

piece_      = pygame.image.load('images/piece.png')
champignon_ = pygame.image.load('images/champignon.png')

piece      = pygame.transform.scale(piece_, (LARGEUR_PIECE * LARGEUR_BLOC_FENETRE, HAUTEUR_PIECE * HAUTEUR_BLOC_FENETRE))
champignon = pygame.transform.scale(champignon_, (LARGEUR_CHAMPIGNON * LARGEUR_BLOC_FENETRE, HAUTEUR_CHAMPIGNON * HAUTEUR_BLOC_FENETRE))

# Fonctions

def initialiser_objets(temps_maintenant):
    global liste_objets, premiere_iteration, temps_derniere_maj

    liste_objets = []
    premiere_iteration = False
    temps_derniere_maj = temps_maintenant


def creer_objet(type, position, vitesse, temps_maintenant, charge=False, actif=False, delai_activation=1, delai_disparition=-1):
    global liste_objets

    objet = [type, position, vitesse, temps_maintenant, charge, actif, delai_activation, delai_disparition]
    liste_objets.append(objet)

def creer_depuis_bloc(type, position_bloc, temps_maintenant):
    creer_objet(
        type=type,
        position=np.array(position_bloc, dtype=float),
        vitesse=np.array([0, VITESSE_SORTIE_BLOC[type]]),
        temps_maintenant=temps_maintenant,
        charge=True,
        delai_activation=TEMPS_SORTIE_BLOC
        )

def supprimer_objet(objet):
    global liste_objets
    liste_objets.remove(objet)


def mettre_a_jour_toutes_positions(temps_maintenant, niveau):
    global liste_objets, premiere_iteration, temps_derniere_maj

    if premiere_iteration:
        initialiser_objets(temps_maintenant)
        return

    blocs = niveau.blocs_solides
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

    # si objet pas chargé (charger/decharger items TBD)
    if not objet[CHARGE]:
        return

    # initialiser acceleration
    acceleration = np.zeros(2)

    # objet actif (sensibles à la physique)
    if objet[ACTIF]:
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

    objet[VITESSE][H] = direction_H(objet[POSITION][H], mario.position[H]) * VITESSE_OBJET[objet[TYPE]]


def gerer_physique(objet, acceleration, blocs):

    # si touche sol
    if test_collision_bas_bloc(objet[POSITION], TAILLE_OBJET[objet[TYPE]], blocs, bordure=False):
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
        and test_collision_gauche_bloc(objet[POSITION], TAILLE_OBJET[objet[TYPE]], blocs, bordure=False)) \
            or (sens_vitesse(objet[VITESSE], H) == VERS_DROITE \
                and test_collision_droite_bloc(objet[POSITION], TAILLE_OBJET[objet[TYPE]], blocs, bordure=False)):
        objet[VITESSE][H] = - objet[VITESSE][H]


def sprite(objet):

    if objet[TYPE] == PIECE:
        return piece
    elif objet[TYPE] == CHAMPIGNON:
        return champignon