import random
import time

def charger_dictionnaire(fichier="dictionnaire.txt"):
    """
    Charge un dictionnaire de mots depuis un fichier texte.

    Args:
        fichier (str): Chemin vers le fichier contenant les mots (un mot par ligne).
                      Par défaut : "dictionnaire.txt".

    Returns:
        list: Liste des mots en minuscules, sans espaces ni sauts de ligne.
              Retourne une liste vide si le fichier est introuvable.
    """
    try:
        with open(fichier, "r", encoding="utf-8") as f:
            return [mot.strip().lower() for mot in f if mot.strip()]
    except FileNotFoundError:
        print("Le fichier dictionnaire.txt est introuvable.")
        return []

def est_plonge(mot, mot_ref):
    """
    Vérifie si un mot est "plongé" dans un mot de référence.
    Un mot est plongé si ses lettres apparaissent dans l'ordre (mais pas forcément consécutives) dans le mot de référence.

    Args:
        mot (str): Mot à tester.
        mot_ref (str): Mot de référence.

    Returns:
        bool: True si le mot est plongé, False sinon.
    """
    i = 0
    for lettre in mot_ref:
        if i < len(mot) and mot[i] == lettre:
            i += 1
    return i == len(mot)

# --- paramètres ---
HP_DEPART = 50  # Points de vie initiaux pour chaque joueur
TEMPS_MAX = 15  # Temps maximum pour entrer un mot (en secondes)

dictionnaire = charger_dictionnaire()
dictionnaire_ref = [mot for mot in dictionnaire if len(mot) >= 6]  # On ne garde que les mots de 6 lettres ou plus

# On stocke les PVs des joueurs

joueurs = [50, 50]

tour = 1
print("=== Jeu du mot plongé ===")

# Boucle principale
while joueurs[0] > 0 and joueurs[1] > 0:
    print("\n--- Tour ", tour, " ---")
    mot_ref = random.choice(dictionnaire_ref)
    print("Mot de référence : ", mot_ref)

    for i in range(len(joueurs)):
        print("joueur ", i+1, " : entrez un mot en ", TEMPS_MAX, " secondes :")
        debut = time.time()
        mot_joueur = input("> ").lower().strip()
        temps = time.time() - debut

        if temps > TEMPS_MAX:
            print("Temps dépassé ! -5 HP")
            joueurs[i] -= 5
        elif mot_joueur not in dictionnaire:
            print("Mot invalide ! -5 HP")
            joueurs[i] -= 5
        elif not est_plonge(mot_joueur, mot_ref):
            print("Le mot n'est pas plongé ! -5 HP")
            joueurs[i] -= 5
        else:
            print("Mot accepté ! L'adversaire perd ", len(mot_joueur), " HP")
            # L'autre joueur perd des HP
            if i == 0:
                joueurs[1] -= len(mot_joueur) 
            else:
                 joueurs[0] -= len(mot_joueur)

    print("\nÉtat des joueurs :")
    for i in range(len(joueurs)):
        print("joueur ", i, " : ", joueurs[i], " HP")

    tour += 1

# Résultat final
if joueurs[0] > joueurs[1]:
    print("\n=== Victoire du joueur 1 ! ===")
elif joueurs[0] < joueurs[1]:
    print("\n=== Victoire du joueur 2 ! ===")
else:
    print("\n=== Égalité ! ===")
