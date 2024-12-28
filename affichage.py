import pygame
import mario
import objet
import sprites
import niveaux
from collisions import *
from constantes import *
from couleurs import *


def niveau_vers_fenetre(coordonnee, position_camera):
    x_n, y_n = coordonnee
    x_offset = position_camera[H] - LARGEUR_BLOC / 2
    y_offset = position_camera[V] - HAUTEUR_BLOC / 2

    x_f = (x_n - x_offset) * LARGEUR_BLOC_FENETRE
    y_f = - (y_n - y_offset) * HAUTEUR_BLOC_FENETRE + HAUTEUR_FENETRE

    return x_f, y_f

def taille_dans_fenetre(taille):
    l, h = taille
    return l * LARGEUR_BLOC_FENETRE, h * HAUTEUR_BLOC_FENETRE

def rect_bloc_fenetre(coordonnee, position_camera):
    return rect_fenetre(coordonnee, TAILLE_BLOC, position_camera)


def rect_fenetre(coordonnee, taille, position_camera):
    x, y = coordonnee
    largeur, hauteur = taille
    taille_f = taille_dans_fenetre(taille)
    coin_f = niveau_vers_fenetre((x - LARGEUR_BLOC / 2, y + hauteur - HAUTEUR_BLOC / 2), position_camera)
    return pygame.rect.Rect(coin_f, taille_f)


def zone_affichable(position_camera):
    x, y = position_camera
    min_x = min(round(x), int(x))
    min_y = min(round(y), int(y))
    x, y = position_camera + [LARGEUR_FENETRE_EN_BLOCS, HAUTEUR_FENETRE_EN_BLOCS] + np.array(TAILLE_BLOC)/2
    max_x = max(round(x), int(x))
    max_y = max(round(y), int(y))
    return (min_x, min_y), (max_x, max_y)


def dessiner_decors(fenetre, niveau):
    fenetre.fill(BLEU_CLAIR)
    sol = niveaux.blocs_sol(niveau)
    (min_x, min_y), (max_x, max_y) = zone_affichable(mario.position_camera)

    for x in range(min_x, max_x):
        for y in range(min_y, max_y):
            if sol[x, y]:
                rect = rect_bloc_fenetre((x,y), mario.position_camera)
                pygame.draw.rect(fenetre, VERT_CLAIR, rect)


def dessiner_blocs(fenetre, niveau):
    blocs = niveaux.blocs_non_sol(niveau)
    (min_x, min_y), (max_x, max_y) = zone_affichable(mario.position_camera)

    for x in range(min_x, max_x):
        for y in range(min_y, max_y):
            if blocs[x, y]:
                rect = rect_bloc_fenetre((x,y), mario.position_camera)
                fenetre.blit(sprites.bloc(niveau[BLOCS][x, y]), rect)


def dessiner_mario(fenetre):
    rect = rect_fenetre(mario.position, TAILLE_MARIO[mario.etat], mario.position_camera)
    fenetre.blit(sprites.mario(), rect)


def dessiner_objets(fenetre):
    for obj in objet.liste_objets:
        if obj[ACTIF]:
            rect = rect_fenetre(obj[POSITION], TAILLE_OBJET[obj[TYPE]], mario.position_camera)
            fenetre.blit(sprites.objet(obj[TYPE]), rect)

def dessiner_objets_fond(fenetre):
    for obj in objet.liste_objets:
        if not obj[ACTIF]:
            rect = rect_fenetre(obj[POSITION], TAILLE_OBJET[obj[TYPE]], mario.position_camera)
            fenetre.blit(sprites.objet(obj[TYPE]), rect)