import numpy as np
from constantes import *

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
    creer_objet(type, np.array(position_bloc, dtype=float), np.array([0, VITESSE_SORTIE_BLOC]),
                temps_maintenant, delai_activation=TEMPS_SORTIE_BLOC, charge=True)

def supprimer_objet(objet):
    global liste_objets
    liste_objets.remove(objet)


def mettre_a_jour_toutes_positions(temps_maintenant):
    global liste_objets, premiere_iteration, temps_derniere_maj

    if premiere_iteration:
        initialiser_objets(temps_maintenant)
        return

    for objet in liste_objets:
        mettre_a_jour_position(objet, temps_maintenant, temps_derniere_maj)
    
    temps_derniere_maj = temps_maintenant


def mettre_a_jour_position(objet, temps_maintenant, temps_derniere_maj):
    global liste_objets

    if objet[DELAI_DISPARITION] > 0 \
        and temps_maintenant - objet[MOMENT_APPARITION] >= objet[DELAI_DISPARITION]:
        supprimer_objet(objet)
        return

    if not objet[CHARGE]:
        return

    acceleration = np.zeros(2)
    if objet[ACTIF]:
        gerer_vitesses(objet, acceleration)
    elif objet[DELAI_ACTIVATION] > 0 \
        and temps_maintenant - objet[MOMENT_APPARITION] >= objet[DELAI_ACTIVATION]:
        objet[ACTIF] = True

    dt = temps_maintenant - temps_derniere_maj
    print(dt)
    objet[POSITION] += objet[VITESSE] * dt + 0.5 * acceleration * dt**2


def gerer_vitesses(objet, acceleration):
    objet[VITESSE] = np.zeros(2)


def sprite(objet):

    if objet[TYPE] == PIECE:
        return champignon
    elif objet[TYPE] == CHAMPIGNON:
        return champignon