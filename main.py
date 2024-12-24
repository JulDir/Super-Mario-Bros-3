import pygame
import affichage
import mario
import objet
from niveaux import Niveau
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

champ = False
temps_champ = 5

niveau = Niveau()

#--- Boucle principale
while not fini:

    temps_maintenant = pygame.time.get_ticks() / 1000
    traiter_evenements()

    # test champignon
    if not champ and temps_maintenant >= temps_champ:
        objet.creer_depuis_bloc(CHAMPIGNON, [10, 5], temps_maintenant)
        champ = True
        print('CHAMPIGNON')
    
    if champ:
        print(f'champ = {objet.liste_objets[0]}')

    mario.mettre_a_jour_position(touches, niveau, temps_maintenant, derniere_touche_direction)
    objet.mettre_a_jour_toutes_positions(temps_maintenant)

    affichage.dessiner_decors(fenetre, niveau, mario.position_camera)
    affichage.dessiner_objets(fenetre, mario.position_camera)
    affichage.dessiner_mario(fenetre, mario.position_camera)

    pygame.display.flip()
    horloge.tick(FPS)

pygame.display.quit()
pygame.quit()
