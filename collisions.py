from constantes import *


def test_collision_droite_bloc(objet, taille, grille, separe = True, bordure = True):
    yb, yh = generate_rays_references_y(objet, taille[V])

    for y in [yb, objet[V], yh]:
        if test_touche_droite_bloc((objet[H], y), taille[H]/2 + TOLERANCE, grille, False, bordure):
            if separe and test_touche_droite_bloc((objet[H], y), taille[H]/2, grille, False, bordure):
                x_grille_collision = round(objet[H] + taille[H]/2)
                objet[H] = x_grille_collision - (LARGEUR_BLOC/2 + taille[H]/2)
            return True
    return False

def test_collision_gauche_bloc(objet, taille, grille, separe = True, bordure = True):
    yb, yh = generate_rays_references_y(objet, taille[V])

    for y in [yb, objet[V], yh]:
        if test_touche_gauche_bloc((objet[H], y), taille[H]/2 + TOLERANCE, grille, False, bordure):
            if separe and test_touche_gauche_bloc((objet[H], y), taille[H]/2, grille, False, bordure):
                x_grille_collision = round(objet[H] - taille[H]/2)
                objet[H] = x_grille_collision + (LARGEUR_BLOC/2 + taille[H]/2)
            return True
    return False

def test_collision_haut_bloc(objet, taille, grille, separe = True, bordure = True):
    xg, xd = generate_rays_references_x(objet, taille[H])

    for x in [xg, objet[H], xd]:
        if test_touche_haut_bloc((x, objet[V]), taille[V] - HAUTEUR_BLOC/2 + TOLERANCE, grille, False, bordure):
            if separe and test_touche_haut_bloc((x, objet[V]), taille[V] - HAUTEUR_BLOC/2, grille, False, bordure):
                y_grille_collision = round(objet[V] + taille[V] - HAUTEUR_BLOC/2)
                objet[V] = y_grille_collision - taille[V]
            return True
    return False

def test_collision_bas_bloc(objet, taille, grille, separe = True, bordure = True):
    xg, xd = generate_rays_references_x(objet, taille[H])

    for x in [xg, objet[H], xd]:
        if test_touche_bas_bloc((x, objet[V]), HAUTEUR_BLOC/2 + TOLERANCE, grille, False, bordure):
            if separe and test_touche_bas_bloc((x, objet[V]), HAUTEUR_BLOC/2, grille, False, bordure):
                y_grille_collision = round(objet[V] - HAUTEUR_BLOC/2)
                objet[V] = y_grille_collision + HAUTEUR_BLOC
            return True
    return False

def generate_rays_references_x(objet, largeur):
    return objet[H] - 0.75*(largeur/2), objet[H] + 0.75*(largeur/2)

def generate_rays_references_y(objet, hauteur):
    return objet[V] - (HAUTEUR_BLOC/2) + TOLERANCE, objet[V] + (hauteur - HAUTEUR_BLOC/2) - TOLERANCE

def test_touche_dh_bloc(objet, distance, grille, direction, separe = True, bordure = True):

    coordonnees_grille = [round(objet[H]), round(objet[V])]
    coordonnees_grille[direction] = round(objet[direction] + distance)
    x_g, y_g = coordonnees_grille

    if coordonnees_grille[direction] >= grille.shape[direction]:
        if bordure:
            if separe:
                objet[direction] = coordonnees_grille[direction] - (TAILLE_BLOC[direction]/2 + distance)
            return True
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
