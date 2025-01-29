#!/bin/bash

# Vérifie si Python est installé
if ! command -v python3 &> /dev/null
then
    echo "[ERREUR] Python n'est pas installé sur votre ordinateur. Veuillez installer Python."
    exit 1
fi

# Crée un environnement virtuel s'il n'existe pas
if [ ! -d "venv" ]; then
    echo "[INFO] Création de l'environnement virtuel..."
    python3 -m venv venv
fi

# Active l'environnement virtuel
echo "[INFO] Activation de l'environnement virtuel..."
# shellcheck disable=SC1091
source venv/bin/activate

# Vérifie si pip est installé dans l'environnement virtuel
if ! command -v pip &> /dev/null
then
    echo "[ERREUR] Pip n'est pas installé dans l'environnement virtuel."
    deactivate
    exit 1
fi

# Mise à jour de pip
echo "[INFO] Mise à jour de pip..."
python3 pip install --upgrade pip
if [ $? -ne 0 ]; then
    echo "[ERREUR] Echec de la mise à jour de pip."
    deactivate
    exit 1
fi

# Installation des packages à partir de requirements.txt
echo "[INFO] Installation des packages depuis requirements.txt..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[ERREUR] Echec de l'installation des packages depuis requirements.txt."
    deactivate
    exit 1
fi

# Vérifie si manage.py existe avant de l'exécuter
if [ ! -f "manage.py" ]; then
    echo "[ERREUR] Le fichier manage.py est introuvable."
    deactivate
    exit 1
fi

# Lance le fichier main.py
echo "[INFO] Lancement du programme..."
python3 manage.py runserver

# Désactive l'environnement virtuel
deactivate

# Pause
echo "[INFO] Script terminé. Appuyez sur une touche pour fermer."
# shellcheck disable=SC2162
read -n 1 -s