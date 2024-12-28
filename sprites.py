import pygame
import mario as m
from constantes import *

def load_image(path, taille = TAILLE_BLOC):
    image_ = pygame.image.load(path)
    taille_fenetre = (taille[H] * LARGEUR_BLOC_FENETRE, taille[V] * HAUTEUR_BLOC_FENETRE)
    image = pygame.transform.scale(image_, taille_fenetre)
    return image

def retourner_image(image):
    return pygame.transform.flip(image, True, False)

### mario

mario_g       = load_image(MARIO_PATH + 'mario.png', TAILLE_MARIO[PETIT])
marche1_g     = load_image(MARIO_PATH + 'marche1.png', TAILLE_MARIO[PETIT])
saute_g       = load_image(MARIO_PATH + 'saute.png', TAILLE_MARIO[PETIT])
grand_g       = load_image(MARIO_PATH + 'grand.png', TAILLE_MARIO[GRAND])
grand_saute_g = load_image(MARIO_PATH + 'grand_saute.png', TAILLE_MARIO[GRAND])
feu_g         = load_image(MARIO_PATH + 'feu.png', TAILLE_MARIO[FEU])
feu_saute_g   = load_image(MARIO_PATH + 'feu_saute.png', TAILLE_MARIO[FEU])

mario_d       = retourner_image(mario_g)
marche1_d     = retourner_image(marche1_g)
saute_d       = retourner_image(saute_g)
grand_d       = retourner_image(grand_g)
grand_saute_d = retourner_image(grand_saute_g)
feu_d         = retourner_image(feu_g)
feu_saute_d   = retourner_image(feu_saute_g)

SPRITES_MARCHE_GAUCHE_PETIT = [mario_g, marche1_g]
SPRITES_MARCHE_DROITE_PETIT = [mario_d, marche1_d]
SPRITES_MARCHE_PETIT = [SPRITES_MARCHE_GAUCHE_PETIT, SPRITES_MARCHE_DROITE_PETIT]

SPRITES_MARCHE_GAUCHE_GRAND = [grand_g]
SPRITES_MARCHE_DROITE_GRAND = [grand_d]
SPRITES_MARCHE_GRAND = [SPRITES_MARCHE_GAUCHE_GRAND, SPRITES_MARCHE_DROITE_GRAND]

SPRITES_MARCHE_GAUCHE_FEU = [feu_g]
SPRITES_MARCHE_DROITE_FEU = [feu_d]
SPRITES_MARCHE_FEU = [SPRITES_MARCHE_GAUCHE_FEU, SPRITES_MARCHE_DROITE_FEU]

SPRITES_MARCHE = [SPRITES_MARCHE_PETIT, SPRITES_MARCHE_GRAND, SPRITES_MARCHE_FEU]

SPRITES_SAUT_PETIT = [[saute_g], [saute_d]]
SPRITES_SAUT_GRAND = [[grand_saute_g], [grand_saute_d]]
SPRITES_SAUT_FEU   = [[feu_saute_g], [feu_saute_d]]

SPRITES_SAUT = [SPRITES_SAUT_PETIT, SPRITES_SAUT_GRAND, SPRITES_SAUT_FEU]

def sprite_serie_mario():

    if m.direction == VERS_GAUCHE:
        dir = G
    else:
        dir = D

    if not m.au_sol:
        return SPRITES_SAUT[m.etat][dir]
    else:
        return SPRITES_MARCHE[m.etat][dir]

def mario():
    # animations TBD
    return sprite_serie_mario()[0]


### blocs

brique       = load_image(BLOC_PATH + 'brique.png')
bloc_vide    = load_image(BLOC_PATH + 'bloc.png')
bloc_mystere = load_image(BLOC_PATH + 'bloc_mystere.png')
bloc_bois    = load_image(BLOC_PATH + 'bloc_bois.png')
bloc_note    = load_image(BLOC_PATH + 'bloc_note.png')

BLOCS = [brique, bloc_vide, bloc_mystere, bloc_bois, bloc_note]

def bloc(type):
    return BLOCS[type-2]

### objets

piece      = load_image(OBJET_PATH + 'piece.png')
champignon = load_image(OBJET_PATH + 'champignon.png')
fleur      = load_image(OBJET_PATH + 'fleur.png')
feuille    = load_image(OBJET_PATH + 'feuille.png')

OBJETS = [piece, champignon, fleur, feuille]

def objet(type):
    return OBJETS[type-1]

### ennemis