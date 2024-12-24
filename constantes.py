import pygame

# controles / parametres

FPS = 50

H = 0
V = 1

TOUCHE_GAUCHE = pygame.K_q
TOUCHE_DROITE = pygame.K_d
TOUCHE_HAUT   = pygame.K_z
TOUCHE_BAS    = pygame.K_s
TOUCHE_SAUT   = pygame.K_SPACE
TOUCHE_COURSE = pygame.K_LSHIFT

APPUIE_GAUCHE = 0
APPUIE_DROITE = 1
APPUIE_HAUT   = 2
APPUIE_BAS    = 3
APPUIE_SAUT   = 4
APPUIE_COURSE = 5

# mario

NB_FORMES = 8

LARGEUR_MARIO       = 1 # en blocs
HAUTEUR_PETIT_MARIO = 1
HAUTEUR_GRAND_MARIO = 2
HAUTEUR_MARIO = [HAUTEUR_PETIT_MARIO] + [HAUTEUR_GRAND_MARIO for i in range(NB_FORMES-1)]
TAILLE_MARIO  = list(zip([LARGEUR_MARIO for i in range(NB_FORMES)], HAUTEUR_MARIO))

VERS_GAUCHE = -1
VERS_DROITE = 1
VERS_HAUT   = 1
VERS_BAS    = -1

PETIT         = 0
GRAND         = 1
FEU           = 2
TANUKI        = 3
SUPER_TANUKI  = 4
TANUKI_PIERRE = 5
MARTEAU       = 6
GRENOUILLE    = 7

RIEN           = 0
CARAPACE_VERTE = 1
CARAPACE_ROUGE = 2
BLOC           = 3

ETAT_BASE      = PETIT
VIES_BASE      = 5
OBJET_BASE     = RIEN
DIRECTION_BASE = VERS_DROITE

FIXE     = 0
MARCHE   = 1
COURS    = 2
SAUTE    = 3
FREINE   = 4
VOLE     = 5
NAGE     = 6

# mouvements

VITESSE_MARCHE_H     = 4   # bloc / s
VITESSE_COURSE_H     = 10  # bloc / s
ACCELERATION_H       = 10  # bloc / s²
RALENTISSEMENT_H     = 10  # bloc / s²
FREINAGE_H           = 20  # bloc / s²
TEMPS_MAX_FREINAGE_H = 1   # s

VITESSE_BASE_V       = 9.5 # bloc / s
VITESSE_COURSE_V     = 10  # bloc / s
TEMPS_PROLONGER_SAUT = 0.3 # s
VITESSE_MAX_CHUTE    = 100 # bloc / s
GRAVITATION          = -35 # bloc / s²

TEMPS_ANIMATION_MARCHE = 200 # ms

# blocs / collisions

LARGEUR_BLOC = 1 # en blocs
HAUTEUR_BLOC = 1
TAILLE_BLOC = (LARGEUR_BLOC, HAUTEUR_BLOC)

TOLERANCE = 1e-3

CENTRE         = 0
GAUCHE         = 1
DROITE         = 2
HAUT           = 4
HAUT_GAUCHE    = 5
HAUT_DROITE    = 6
BAS            = 8
BAS_GAUCHE     = 9
BAS_DROITE     = 10

# affichage

LARGEUR_FENETRE = 800
HAUTEUR_FENETRE = 600
TAILLE_FENETRE = (LARGEUR_FENETRE, HAUTEUR_FENETRE)

LARGEUR_FENETRE_EN_BLOCS = 20  # blocs à l'écran
LARGEUR_BLOC_FENETRE = LARGEUR_FENETRE // LARGEUR_FENETRE_EN_BLOCS  # en pixels
HAUTEUR_BLOC_FENETRE = LARGEUR_BLOC_FENETRE
TAILLE_BLOC_FENETRE = (LARGEUR_BLOC_FENETRE, HAUTEUR_BLOC_FENETRE)
HAUTEUR_FENETRE_EN_BLOCS = HAUTEUR_FENETRE // HAUTEUR_BLOC_FENETRE

G = 0
D = 1
