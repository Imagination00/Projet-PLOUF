import unicodedata
import time
import os
import random

# --- utilitaires ---
def enlever_accents(mot: str) -> str:
    """
    Enlève les accents d'un mot et le convertit en minuscules.

    Args:
        mot (str): Mot à normaliser.

    Returns:
        str: Mot sans accents, en minuscules.
    """
    return ''.join(
        c for c in unicodedata.normalize('NFD', mot)
        if unicodedata.category(c) != 'Mn'
    ).lower()

def charger_dictionnaire(fichier: str = "dictionnaire.txt") -> frozenset:
    """
    Charge un dictionnaire de mots depuis un fichier texte, en normalisant les mots (sans accents).

    Args:
        fichier (str): Chemin vers le fichier contenant les mots (un mot par ligne).
                      Par défaut : "dictionnaire.txt".

    Returns:
        frozenset: Ensemble figé de mots normalisés (sans accents, en minuscules).
                  Retourne un ensemble vide si le fichier est introuvable.
    """
    if not os.path.exists(fichier):
        print(f"Fichier {fichier} introuvable")
        return frozenset()
    with open(fichier, encoding="utf-8") as f:
        return frozenset(
            enlever_accents(m.strip()) for m in f if m.strip()
        )

def est_plonge(m: str, M: str) -> bool:
    """
    Vérifie si un mot est "plongé" dans un mot de référence (version optimisée avec deux pointeurs).

    Args:
        m (str): Mot à tester.
        M (str): Mot de référence.

    Returns:
        bool: True si le mot est plongé, False sinon.
    """
    i = j = 0
    while i < len(m) and j < len(M):
        if m[i] == M[j]:
            i += 1
        j += 1
    return i == len(m)

def mot_plus_long_possible(mot_ref: str, dictionnaire: frozenset, interdits: set) -> str:
    """
    Trouve le mot le plus long plongé dans un mot de référence, parmi ceux non interdits.

    Args:
        mot_ref (str): Mot de référence.
        dictionnaire (frozenset): Ensemble des mots valides.
        interdits (set): Ensemble des mots interdits pour ce tour.

    Returns:
        str: Le mot le plus long possible, ou None si aucun mot valide.
    """
    candidats = [m for m in dictionnaire if est_plonge(m, mot_ref) and m not in interdits]
    if not candidats:
        return None
    return max(candidats, key=len)

# --- paramètres du jeu ---
HP_DEPART = 50  # Points de vie initiaux pour chaque joueur
TEMPS_MAX = 15  # Temps maximum pour entrer un mot (en secondes)

dictionnaire = charger_dictionnaire()
dictionnaire_ref = [mot for mot in dictionnaire if len(mot) >= 6]  # On ne garde que les mots de 6 lettres ou plus

# Structure des joueurs : chaque joueur a un historique de ses mots pour éviter les répétitions
joueurs = [
    {"nom": "Joueur 1", "hp": HP_DEPART, "mots": set()},
    {"nom": "Joueur 2", "hp": HP_DEPART, "mots": set()},
]

def demander_mot(joueur: dict, mot_ref: str, interdits: set) -> str:
    """
    Demande à un joueur d'entrer un mot plongé dans le mot de référence, dans un temps limité.

    Args:
        joueur (dict): Dictionnaire représentant le joueur.
        mot_ref (str): Mot de référence.
        interdits (set): Ensemble des mots interdits pour ce tour.

    Returns:
        str: Le mot entré par le joueur (normalisé), ou None en cas d'erreur.
    """
    print(f"{joueur['nom']} → mot plongé dans '{mot_ref}' ({TEMPS_MAX}s) :")
    start = time.time()
    mot = input("> ").strip()
    duree = time.time() - start

    if duree > TEMPS_MAX:
        print("Temps dépassé")
        return None

    mot = enlever_accents(mot)
    if mot in interdits:
        print("Mot interdit ce tour")
        return None

    return mot

# --- boucle du jeu ---
tour = 1
while all(j["hp"] > 0 for j in joueurs):
    print("\n" + "="*30)
    print(f"Tour {tour}")
    print("="*30)

    # Chaque joueur a un mot de référence différent (même longueur)
    mot_ref_j1 = random.choice(dictionnaire_ref)
    longueur = len(mot_ref_j1)
    mots_possibles_j2 = [mot for mot in dictionnaire_ref if len(mot) == longueur and mot != mot_ref_j1]
    mot_ref_j2 = random.choice(mots_possibles_j2)
    mots_refs = [mot_ref_j1, mot_ref_j2]

    for i, joueur in enumerate(joueurs):
        mot_ref = mots_refs[i]
        interdits = {mot_ref}  # mots interdits pour ce tour
        mot = demander_mot(joueur, mot_ref, interdits)

        if not mot or mot not in dictionnaire or mot in joueur["mots"] or not est_plonge(mot, mot_ref):
            print(f"{joueur['nom']} rate ( -{len(mot_ref)} HP )")
            joueur["hp"] -= len(mot_ref)
        else:
            joueur["mots"].add(mot)
            adversaire = joueurs[(i + 1) % 2]
            adversaire["hp"] -= len(mot)
            print(f"{joueur['nom']} joue '{mot}'")

        # Afficher la solution du mot le plus long possible non interdit
        solution = mot_plus_long_possible(mot_ref, dictionnaire, interdits.union(joueur["mots"]))
        if solution:
            print(f"Mot le plus long possible : {solution}")

    print("\nÉtat des joueurs :")
    for joueur in joueurs:
        print(f"{joueur['nom']:10} {joueur['hp']:>3} HP")

    tour += 1

# --- fin du jeu ---
vainqueur = max(joueurs, key=lambda j: j["hp"])
print("\n" + "="*30)
print(f"Victoire : {vainqueur['nom']}")
print("="*30)
