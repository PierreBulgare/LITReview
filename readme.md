# LITReview - Critiques de Livres et d'Articles

## Informations sur la version
**Version** : 1.0\
**Date** : 27 Janvier 2025\
**Auteur** : Pierre BULGARE

## Description
Cette application web a pour objectif de permettre aux utilisateurs de créer, gérer et partager des critiques sur des livres et articles. Elle offre la possibilité de soumettre des demandes de critiques, de rédiger des avis détaillés et d'attribuer des notes aux ouvrages évalués.

## Prérequis
* **Python 3.10 ou une version supérieur** : [Téléchargements](https://www.python.org/downloads/)

*Si Python est déjà installé sur votre système, vous pouvez vérifier la version en tapant dans votre terminal : `python --version` pour Windows et `python3 --version` pour Mac OS/Linux.*

* Packages requis :
  * `Django` 5.1.4 - Framework utilisé pour la conception de l'application
  * `pillow` 11.1.0 - Pour la gestion des images

## Mode d'emploi
### Installation de l'environnement Python virtuel
Pour utiliser le programme, vous devez d'abord installer un environnement Python et installer les prérequis :

**🖥️ Windows**
- Lancez le fichier `launch.bat`

**🖥️ Mac OS/Linux**
- Lancez le fichier `launch.sh`

***Ce fichier vérifiera si Python et Pip sont installés sur votre système, puis créera un environnement virtuel s'il n'existe pas déjà. Ensuite, il s'assurera que les packages requis sont installés dans cet environnement et les installera automatiquement si nécessaire. Il lancera ensuite le serveur et la page d'accueil de l'application.***

### Utilisation de l'application
Vous avez la possibilité de tester l'inscription, la connexion, la création d'un ticket, la création d'une critique et les fonctionnalités de gestions d'utilisateurs comme les abonnements.

**Flux**\
Cette page permet de visualiser les posts de l'utilisateur connecté et des utilisateurs suivis dans un ordre antichronologique. Il est aussi possible de répondre à des demandes de critiques.\
Pour tester la page flux, la base de donnée possède quelques critiques et billets.\
- Créez un compte sur l'application
- Abonnez-vous à pierre.bulgare, camille.martin ou leopold.durand (ou les trois) pour avoir le flux

**Posts**\
Cette page permet à la visualisation et la gestion des posts de l'utilisateur connecté uniquement. L'utilisateur peut modifier ou supprimer ses billets et ses critiques.

**Abonnements**\
Cette page permet de gérer les fonctionnalités utilisateurs comme l'abonnement, le désabonnement et le blocage. Elle permet aussi de visualiser les utilisateurs abonnés.
Trois utilisateurs sont disponibles dans la base de donnée pour essayer l'abonnement:
- pierre.bulgare
- camille.martin
- leopold.durant

**Création de Ticket**\
La page de création de ticket propose un formule simple avec trois champs (Titre, Description et Image), seul le titre est requis, les deux autres champs sont facultatifs.

**Création d'une critique**\
La page de création de critique a deux fonctionnalités:
- La réponse à une critique depuis un billet utilisateur
- La création d'une critique sans relation avec un billet utilisateur (cela permet à la fois de créer un billet et une critique dans le même formulaire)

**Suppression des posts**\
La suppression des posts est possible depuis la page posts.\
⚠️ **Important** : Supprimé un billet supprimera aussi la critique liée s'il y en a une. En revanchhe, supprimer une critique ne supprime bien évidemment pas un billet même s'il a été créé de manière simultanée dans le formulaire de création de critique.

## Contacts
Si vous avez le moindre doute ou si vous rencontrez une erreur lors de l'exécution du programme, n'hésitez pas à me contacter.

---

*** Si vous ne pouvez pas utiliser les fichiers de lancement `launch.bat` ou `launch.sh`, vous pouvez installer manuellement l'environnement Python et les prérequis en exécutant les commandes suivantes dans votre terminal :

_Vérifiez que vous êtes bien dans le répertoire où se trouvent `requirements.txt` et `main.py` avant de lancer les commandes ci-dessous._

**Windows**
1. Créez l'environnement virtuel : `python -m venv venv`
2. Activez l'environnement : `venv\Scripts\activate`
3. Installez les prérequis : `pip install -r requirements.txt`
4. Lancez le serveur : `python manage.py runserver`
5. Accédez au serveur : [127.0.0.1:8000](http://127.0.0.1:8000)

**Mac OS/Linux**
1. Créez l'environnement virtuel : `python3 -m venv venv`
2. Activez l'environnement : `source venv/bin/activate`
3. Installez les prérequis : `pip3 install -r requirements.txt`
4. Lancez le serveur : `python3 manage.py runserver`
5. Accédez au serveur : [127.0.0.1:8000](http://127.0.0.1:8000)