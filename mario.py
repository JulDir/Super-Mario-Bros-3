import math
import numpy as np
import niveaux
from constantes import *
from collisions import *

### Variables

premiere_maj = True
en_vie = True

### Fonctions

# Deplacements

def norme_vitesse():
    return math.sqrt(vitesse[H]**2 + vitesse[V]**2)

def norme_vitesse(direction):
    return abs(vitesse[direction])


def mettre_a_jour_position(touches, niveau, temps_maintenant, derniere_direction):
    global position, vitesse, temps_derniere_maj, direction, premiere_maj, position_camera, mouvement, au_sol

    # initialisation
    if premiere_maj:
        initialiser_variables(temps_maintenant)
        return

    dt = temps_maintenant - temps_derniere_maj

    # gestion touches directionnelles
    bouge = False
    if touches[APPUIE_DROITE] and touches[APPUIE_GAUCHE]:
        if derniere_direction == APPUIE_GAUCHE:
            direction = VERS_GAUCHE
        elif derniere_direction == APPUIE_DROITE:
            direction = VERS_DROITE
    elif touches[APPUIE_DROITE]:
        direction = VERS_DROITE
        bouge = True
    elif touches[APPUIE_GAUCHE]:
        direction = VERS_GAUCHE
        bouge = True
    else:
        bouge = False

    cours = touches[APPUIE_COURSE]
    saute = touches[APPUIE_SAUT]

    # initialiser acceleration
    acceleration = np.zeros(2)
    # print(f'avant calculs {acceleration, vitesse, position}')

    # gestion collisions (avant gérer sauts pour éviter wall jumps)
    gerer_chute(acceleration, niveau)
    gerer_collisions_H(acceleration, niveau)

    # gestion sauts & deplacements verticaux
    gerer_sauts(temps_maintenant, saute, cours, niveau)
    
    # gestion deplacements horizontaux
    gerer_vitesses_H(acceleration, temps_maintenant, bouge, cours)

    # calculs deplacements
    deplacement = vitesse * dt + 0.5 * acceleration * dt**2
    position   += deplacement
    vitesse    += acceleration * dt
    # print(f'après calculs {acceleration, vitesse, position}')

    # gestion camera
    gerer_scrolling(deplacement, niveau)

    temps_derniere_maj = temps_maintenant


def initialiser_variables(temps_maintenant):
    global premiere_maj, position, vitesse, direction, etat, vies, objet_tenu, \
        mouvement, position_camera, au_sol, temps_derniere_maj, temps_debut_saut, \
            peut_prolonger_saut, temps_debut_freinage, en_vie

    position             = np.array([8.0, 10.0])
    vitesse              = np.array([0.0, 0.0])
    etat                 = ETAT_BASE
    vies                 = VIES_BASE
    objet_tenu           = OBJET_BASE
    direction            = DIRECTION_BASE
    mouvement            = FIXE
    premiere_maj         = False
    direction            = VERS_DROITE
    au_sol               = True
    mouvement            = FIXE
    position_camera      = np.array([0.0, 0.0])
    temps_derniere_maj   = temps_maintenant
    temps_debut_saut     = -1
    peut_prolonger_saut  = True
    temps_debut_freinage = -1
    en_vie               = True


def position_relative_camera_H():
    offset = round(position[H] - position_camera[H])
    if offset < LARGEUR_FENETRE_EN_BLOCS / 2:
        return GAUCHE
    else:
        return DROITE


def gerer_vitesses_H(acceleration, temps_maintenant, bouge, cours):
    global vitesse, au_sol, direction, temps_debut_freinage

    if bouge:
        if cours:
            vitesse_max = VITESSE_COURSE_H
        else:
            vitesse_max = VITESSE_MARCHE_H
    else:
        vitesse_max = 0

    if sens_vitesse(vitesse, H) != 0 and sens_vitesse(vitesse, H) != direction:
        acc = FREINAGE_H
    elif norme_vitesse(H) < vitesse_max:
        acc = ACCELERATION_H
    elif norme_vitesse(H) > vitesse_max:
        if au_sol:
            acc = - RALENTISSEMENT_H
        else:
            acc = 0
    else:
        acc = 0
        vitesse[H] = 0

    acceleration[H] = acc * direction

    if vitesse_max == 0 and acc != 0:
        if temps_debut_freinage < 0:
            temps_debut_freinage = temps_maintenant
        elif temps_maintenant - temps_debut_freinage > TEMPS_MAX_FREINAGE_H \
            or norme_vitesse(H) < TOLERANCE:
            acceleration[H] = 0
            vitesse[H] = 0
            temps_debut_freinage = -1
    else: temps_debut_freinage = -1


def gerer_collisions_H(acceleration, niveau):
    global position, vitesse
    blocs = niveaux.blocs(niveau)

    if test_collision_droite_bloc(position, TAILLE_MARIO[etat], blocs):
        # print('collision droite')
        if vitesse[H] > 0:
            vitesse[H] = 0
        if acceleration[H] > 0:
            acceleration[H] = 0
    if test_collision_gauche_bloc(position, TAILLE_MARIO[etat], blocs):
        # print('collision gauche')
        if vitesse[H] < 0:
            vitesse[H] = 0
        if acceleration[H] < 0:
            acceleration[H] = 0
    test_touche_gauche(position, 0, 0)
    test_touche_droite(position, 0, blocs.shape[H])

    # tomber dans trou
    if test_touche_bas(position, - HAUTEUR_MARIO[etat], 0, False):
        prend_degats(True)


def gerer_sauts(temps_maintenant, saute, cours, niveau):
    global position, vitesse, etat, au_sol, temps_debut_saut, peut_prolonger_saut
    blocs = niveaux.blocs(niveau)

    if saute:
        if au_sol:
            peut_prolonger_saut = True
            temps_debut_saut = temps_maintenant
        if peut_prolonger_saut:
            if cours:
                vitesse[V] = VITESSE_COURSE_V
            else:
                vitesse[V] = VITESSE_BASE_V
    else:
        peut_prolonger_saut = False

    # frapper bloc
    if vitesse[V] > 0 and test_collision_haut_bloc(position, TAILLE_MARIO[etat], blocs, bordure=False):
        vitesse[V] = 0
        peut_prolonger_saut = False
        niveaux.frapper_bloc(niveau, position, etat, temps_maintenant)

    if temps_maintenant - temps_debut_saut > TEMPS_PROLONGER_SAUT:
        peut_prolonger_saut = False


def gerer_chute(acceleration, niveau):
    global position, vitesse, mouvement, au_sol
    blocs = niveaux.blocs(niveau)

    if not test_collision_bas_bloc(position, TAILLE_MARIO[etat], blocs, bordure=False):
        mouvement = SAUTE
        au_sol = False
        if not (vitesse[V] < 0 and abs(vitesse[V]) >= VITESSE_MAX_CHUTE):
            acceleration[V] = GRAVITATION
    else:
        # print(f'atterissage: {position}')
        au_sol = True
        if vitesse[V] < 0:
            vitesse[V] = 0


def gerer_scrolling(deplacement_mario, niveau):
    global direction, position_camera

    pos_relative = position_relative_camera_H()
    if (direction == VERS_GAUCHE and pos_relative != DROITE) \
        or (direction == VERS_DROITE and pos_relative != GAUCHE):
        position_camera[H] += deplacement_mario[H]

    test_touche_gauche(position_camera, 0, 0)
    test_touche_droite(position_camera, LARGEUR_FENETRE_EN_BLOCS, niveaux.taille(niveau)[H])
    test_touche_bas(position_camera, 0, 0)


# Interactions

def prend_degats(mortel=False):
    global etat, en_vie
    if mortel or etat == PETIT:
        en_vie = False
    elif etat == GRAND:
        etat = PETIT
    else:
        etat = GRAND

def test_collision(objet, taille):
    global position, etat
    return test_collision_rect_entites(position, TAILLE_MARIO[etat], objet, taille)

def ramasse_objet(objet):
    global etat

    if objet == CHAMPIGNON and etat == PETIT:
        etat = GRAND
    elif objet == FLEUR:
        etat = FEU
    elif objet == FEUILLE:
        etat = TANUKI
