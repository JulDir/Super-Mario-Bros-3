import pygame
import mario
import objet
from constantes import *
from couleurs import *

### images

brick_ = pygame.image.load(BLOC_PATH + 'brick.png')
brick = pygame.transform.scale(brick_, TAILLE_BLOC_FENETRE)

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


def dessiner_decors(fenetre, niveau):
    fenetre.fill(niveau.fond)


def dessiner_blocs(fenetre, niveau):
    for x in range(niveau.LARGEUR):
        for y in range(niveau.HAUTEUR):
            if niveau.blocs_solides[x][y]:
                rect = rect_bloc_fenetre((x,y), mario.position_camera)
                fenetre.blit(brick, rect)


def dessiner_mario(fenetre):
    rect = rect_fenetre(mario.position, TAILLE_MARIO[mario.etat], mario.position_camera)
    fenetre.blit(mario.sprite(), rect)


def dessiner_objets(fenetre):
    for obj in objet.liste_objets:
        if obj[CHARGE] and obj[ACTIF]:
            rect = rect_fenetre(obj[POSITION], TAILLE_OBJET[obj[TYPE]], mario.position_camera)
            fenetre.blit(objet.sprite(obj), rect)

def dessiner_objets_fond(fenetre):
    for obj in objet.liste_objets:
        if obj[CHARGE] and not obj[ACTIF]:
            rect = rect_fenetre(obj[POSITION], TAILLE_OBJET[obj[TYPE]], mario.position_camera)
            fenetre.blit(objet.sprite(obj), rect)