import pygame
import numpy as np
import time
import affichage
import mario
import objet
from niveaux import creer_niveau
from constantes import *

### Variables

touches = [False for i in range(6)]
derniere_touche_direction = TOUCHE_HAUT

### Fonctions

def traiter_evenements():
    global fini
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            fini = True
        if evenement.type == pygame.KEYDOWN or evenement.type == pygame.KEYUP:
            traiter_touche(evenement.key, evenement.type)


def traiter_touche(touche, type):
    appuie = type == pygame.KEYDOWN

    if touche == TOUCHE_GAUCHE:
        touche_appuiee = APPUIE_GAUCHE
        derniere_touche_direction = APPUIE_GAUCHE
    elif touche == TOUCHE_DROITE:
        touche_appuiee = APPUIE_DROITE
        derniere_touche_direction = APPUIE_DROITE
    elif touche == TOUCHE_BAS:
        touche_appuiee = APPUIE_BAS
        derniere_touche_direction = APPUIE_BAS
    elif touche == TOUCHE_HAUT:
        touche_appuiee = APPUIE_HAUT
        derniere_touche_direction = APPUIE_HAUT
    elif touche == TOUCHE_SAUT:
        touche_appuiee = APPUIE_SAUT
    elif touche == TOUCHE_COURSE:
        touche_appuiee = APPUIE_COURSE
    else:
        return
    appuyer_lacher_touche(touche_appuiee, appuie)


def appuyer_lacher_touche(touche, appuie):
    touches[touche] = appuie


pygame.init()
pygame.key.set_repeat(25, 25)

fenetre = pygame.display.set_mode(affichage.TAILLE_FENETRE)

fini = False
horloge = pygame.time.Clock()

champi = False
temps_champi = 0.5

blocs = np.zeros((40, 20), dtype = int)
blocs[:, :2] = BLOC_SOL
blocs[8:12, 5] = BLOC_BRIQUE
objets = np.zeros_like(blocs)
objets[10,5] = CHAMPIGNON
niveau = creer_niveau(blocs, entites=objets)

#--- Boucle principale
while not fini:

    temps_maintenant = pygame.time.get_ticks() / 1000
    traiter_evenements()

    mario.mettre_a_jour_position(touches, niveau, temps_maintenant, derniere_touche_direction)
    objet.mettre_a_jour_toutes_positions(temps_maintenant, niveau)

    affichage.dessiner_decors(fenetre, niveau)
    affichage.dessiner_objets_fond(fenetre)
    affichage.dessiner_blocs(fenetre, niveau)
    affichage.dessiner_objets(fenetre)
    affichage.dessiner_mario(fenetre)

    pygame.display.flip()
    horloge.tick(FPS)

pygame.display.quit()
pygame.quit()
