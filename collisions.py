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

def rect(position, taille):
    coin = position[H] - taille[H]/2, position[V] + taille[V] - HAUTEUR_BLOC/2
    return pygame.rect.Rect(coin, taille)

def test_collision_entites(objet1, taille1, objet2, taille2):
    return rect(objet1, taille1).colliderect(rect(objet2, taille2))

def test_collision_droite_bloc(objet, taille, grille, separe = True, bordure = True, test_etendu = True):
    y_rays = generate_rays_references_y(objet, taille[V])
    h = TOLERANCE if test_etendu else -TOLERANCE

    for y in y_rays:
        if test_touche_droite_bloc((objet[H], y), taille[H]/2 + h, grille, False, bordure):
            if separe and (h == 0 or test_touche_droite_bloc((objet[H], y), taille[H]/2, grille, False, bordure)):
                x_grille_collision = round(objet[H] + taille[H]/2)
                objet[H] = x_grille_collision - (LARGEUR_BLOC/2 + taille[H]/2)
            return True
    return False

def test_collision_gauche_bloc(objet, taille, grille, separe = True, bordure = True, test_etendu = True):
    y_rays = generate_rays_references_y(objet, taille[V])
    h = TOLERANCE if test_etendu else 0

    for y in y_rays:
        if test_touche_gauche_bloc((objet[H], y), taille[H]/2 + h, grille, False, bordure):
            if separe and (h == 0 or test_touche_gauche_bloc((objet[H], y), taille[H]/2, grille, False, bordure)):
                x_grille_collision = round(objet[H] - taille[H]/2)
                objet[H] = x_grille_collision + (LARGEUR_BLOC/2 + taille[H]/2)
            return True
    return False

def test_collision_haut_bloc(objet, taille, grille, separe = True, bordure = True, test_etendu = True):
    x_rays = generate_rays_references_x(objet, taille[H])
    h = TOLERANCE if test_etendu else 0

    for x in x_rays:
        if test_touche_haut_bloc((x, objet[V]), taille[V] - HAUTEUR_BLOC/2 + h, grille, False, bordure):
            if separe and (h == 0 or test_touche_haut_bloc((x, objet[V]), taille[V] - HAUTEUR_BLOC/2, grille, False, bordure)):
                y_grille_collision = round(objet[V] + taille[V] - HAUTEUR_BLOC/2)
                objet[V] = y_grille_collision - taille[V]
            return True
    return False

def test_collision_bas_bloc(objet, taille, grille, separe = True, bordure = True, test_etendu = True):
    x_rays = generate_rays_references_x(objet, taille[H])
    h = TOLERANCE if test_etendu else 0

    for x in x_rays:
        if test_touche_bas_bloc((x, objet[V]), HAUTEUR_BLOC/2 + h, grille, False, bordure):
            if separe and (h == 0 or test_touche_bas_bloc((x, objet[V]), HAUTEUR_BLOC/2, grille, False, bordure)):
                y_grille_collision = round(objet[V] - HAUTEUR_BLOC/2)
                objet[V] = y_grille_collision + HAUTEUR_BLOC
            return True
    return False

def generate_rays_references_x(objet, largeur):
    return objet[H] - 0.75*(largeur/2), objet[H], objet[H] + 0.75*(largeur/2)

def generate_rays_references_y(objet, hauteur):
    yb = objet[V] - 0.75*(HAUTEUR_BLOC/2)
    yh = objet[V] + (hauteur - 1.25*HAUTEUR_BLOC/2)
    ym = (yh + yb) / 2
    return yb, ym, yh


def test_touche_dh_bloc(objet, distance, grille, direction, separe = True, bordure = True):

    coordonnees_grille = [round(objet[H]), round(objet[V])]
    coordonnees_grille[direction] = round(objet[direction] + distance)
    x_g, y_g = coordonnees_grille

    if coordonnees_grille[direction] >= grille.shape[direction]:
        if bordure:
            if separe:
                objet[direction] = coordonnees_grille[direction] - (TAILLE_BLOC[direction]/2 + distance)
            return True
        else:
            return False
    elif grille[x_g, y_g]:
        if separe:
            objet[direction] = coordonnees_grille[direction] - (TAILLE_BLOC[direction]/2 + distance)
        return True
    else:
        return False

def test_touche_gb_bloc(objet, distance, grille, direction, separe = True, bordure = True):

    coordonnees_grille = [round(objet[H]), round(objet[V])]
    coordonnees_grille[direction] = round(objet[direction] - distance)
    x_g, y_g = coordonnees_grille

    if coordonnees_grille[direction] < 0:
        if bordure:
            if separe:
                objet[direction] = coordonnees_grille[direction] + (TAILLE_BLOC[direction]/2 + distance)
            return True
        else:
            return False
    elif grille[x_g, y_g]:
        if separe:
            objet[direction] = coordonnees_grille[direction] + (TAILLE_BLOC[direction]/2 + distance)
        return True
    else:
        return False

def test_touche_gauche_bloc(objet, largeur_gauche, grille, separe = True, bordure = True):
    return test_touche_gb_bloc(objet, largeur_gauche, grille, H, separe, bordure)

def test_touche_droite_bloc(objet, largeur_droite, grille, separe = True, bordure = True):
    return test_touche_dh_bloc(objet, largeur_droite, grille, H, separe, bordure)

def test_touche_haut_bloc(objet, hauteur_haut, grille, separe = True, bordure = True):
    return test_touche_dh_bloc(objet, hauteur_haut, grille, V, separe, bordure)

def test_touche_bas_bloc(objet, hauteur_bas, grille, separe = True, bordure = True):
    return test_touche_gb_bloc(objet, hauteur_bas, grille, V, separe, bordure)


def test_touche_dh(objet, distance, point, direction, separe):
    if objet[direction] + distance >= point:
        if separe:
            objet[direction] = point - distance
        return True
    else:
        return False

def test_touche_gb(objet, distance, point, direction, separe):
    if objet[direction] - distance <= point:
        if separe:
            objet[direction] = point + distance
        return True
    else:
        return False

def test_touche_droite(objet, largeur_droite, point_droit, separe=True):
    return test_touche_dh(objet, largeur_droite, point_droit, H, separe)

def test_touche_gauche(objet, largeur_gauche, point_gauche, separe=True):
    return test_touche_gb(objet, largeur_gauche, point_gauche, H, separe)

def test_touche_haut(objet, hauteur_haut, point_haut, separe=True):
    return test_touche_dh(objet, hauteur_haut, point_haut, V, separe)

def test_touche_bas(objet, hauteur_bas, point_bas, separe=True):
    return test_touche_gb(objet, hauteur_bas, point_bas, V, separe)
