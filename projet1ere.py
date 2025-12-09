import random
import time

# On charge un dictionnaire de mots (un fichier dictionnaire.txt doit être présent)
def charger_dictionnaire(fichier="dictionnaire.txt"):
    try:
        with open(fichier, "r", encoding="utf-8") as f:
            return [mot.strip().lower() for mot in f if mot.strip()]
    except FileNotFoundError:
        print("Le fichier dictionnaire.txt est introuvable.")
        return []

# Vérifie si le mot joueur est dans l'ordre des lettres du mot de référence
def est_plonge(mot, mot_ref):
    i = 0
    for lettre in mot_ref:
        if i < len(mot) and mot[i] == lettre:
            i += 1
    return i == len(mot)

# --- paramètres ---
HP_DEPART = 30
TEMPS_MAX = 10
dictionnaire = charger_dictionnaire()
dictionnaire_ref = [mot for mot in dictionnaire if len(mot) >= 6]

# On définit deux joueurs
joueurs = [
    {"nom": "Joueur 1", "hp": HP_DEPART},
    {"nom": "Joueur 2", "hp": HP_DEPART}
]

tour = 1
print("=== Jeu du mot plongé ===")

# Boucle principale
while joueurs[0]["hp"] > 0 and joueurs[1]["hp"] > 0:
    print(f"\n--- Tour {tour} ---")
    mot_ref = random.choice(dictionnaire_ref)
    print(f"Mot de référence : {mot_ref}")

    for joueur in joueurs:
        print(f"{joueur['nom']} : entrez un mot en {TEMPS_MAX} secondes :")
        debut = time.time()
        mot_joueur = input("> ").lower().strip()
        temps = time.time() - debut

        if temps > TEMPS_MAX:
            print("Temps dépassé ! -5 HP")
            joueur["hp"] -= 5
        elif mot_joueur not in dictionnaire:
            print("Mot invalide ! -5 HP")
            joueur["hp"] -= 5
        elif not est_plonge(mot_joueur, mot_ref):
            print("Le mot n'est pas plongé ! -5 HP")
            joueur["hp"] -= 5
        else:
            print(f"Mot accepté ! L'adversaire perd {len(mot_joueur)} HP")
            # L'autre joueur perd des HP
            adversaire = joueurs[1] if joueur is joueurs[0] else joueurs[0]
            adversaire["hp"] -= len(mot_joueur)

    print("\nÉtat des joueurs :")
    for joueur in joueurs:
        print(f"{joueur['nom']} : {joueur['hp']} HP")

    tour += 1

# Résultat final
vainqueur = max(joueurs, key=lambda j: j["hp"])
print(f"\n=== Victoire de {vainqueur['nom']} ! ===")