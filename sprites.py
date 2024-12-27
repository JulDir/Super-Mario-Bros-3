import pygame
from constantes import *

def load_image(path, taille = TAILLE_BLOC):
    image_ = pygame.image.load(path)
    taille_fenetre = (taille[H] * LARGEUR_BLOC_FENETRE, taille[V] * HAUTEUR_BLOC_FENETRE)
    image = pygame.transform.scale(image_, taille_fenetre)
    return image

def retourner_image(image):
    pygame.transform.flip(image, True, False)

### mario



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