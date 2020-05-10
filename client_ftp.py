#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 11:54:30 2020

CLIENT FTP
https://docs.python.org/3/library/ftplib.html

ATELIER PYTHON FORMATION AJC
scrpit jouant le rôle d'un client FTP pouvant
réaliser les commandes CWD, DELE, LIST, MKD, RMD, RNFR, STOR

"""
#import os
from subprocess import run
from ftplib import FTP
from getpass import getpass

#*****************************************************************************************
#
# LES MACHINES VIRTUELLES SONT
# - debian (192.168.56.2) qui joue le rôle du client
# - debian2 (192.168.56.3) qui joue le rôle du serveur
#
# - ON INSTALLE VSFTP SUR LES MACHINES DEBIAN : "apt install vsftp"
# - ON CONFIGURE LE FICHIER CONF /etc/vsftp.conf sur debian2 
#   AFIN D'AVOIR LES PERMISSIONS NECESSAIRES EN DECOMMANTANT LA LIGNE
#   write_enable=YES
# 
#*****************************************************************************************

# -----------
# CONNEXION |
# -----------
# Users des machines virtuelles : root et clement
# Entrer le nom d’hôte, le nom d’utilisateur et le mot de passe

hostname =input("Quel est le nom de domaine du serveur FTP ? :")
#hostname = "192.168.56.3"

# on démarre une connexion ftp à la machine "debian02" en créant une instance ftp
ftp=FTP(hostname)
user = input("Username:")
#user = "clement"
mdp = getpass()

# authentification au serveur ftp
ftp.login(user=user, passwd=mdp)

# renvoie le message de bienvenue du serveur ftp
ftp.getwelcome()

# -------------------------
# COMMANDES A IMPLEMENTER |
# -------------------------
# CWD (change current directory) pour changer de répertoire de travail
def CWD(dest_dir):
    ftp.cwd(dest_dir)

# DELE (delete) pour supprimer un fichier
def DELE(name):
        ftp.delete(name) 

# LIST pour lister les fichiers et dossiers d’un répertoire (répertoire courant par défaut)
def LIST(dir_=""):
    if dir_=="":
        ftp.nlst(pwd())
    else:
        ftp.nlst(dir_)
        
# MKD (make directory) pour créer un répertoire
def MKD(new_dir):
    ftp.mkd(new_dir)

# RMD (remove directory) pour supprimer un répertoire
def RMD(name):
    ftp.rmd(name)

# RNFR (rename a file from (name …)) pour renommer un répertoire X en Y
def RNFR(old_name, new_name):
    ftp.rename(old_name, new_name)

# STOR (store a file) pour envoyer un fichier sur le serveur.
def STOR(filename):
    ftp.storbinary('STOR ' + filename, open(filename, 'rb'))

# ----------------------------------------------------------------------------------------------------------------------------
connexion = True
## Une fois connécté on demande si l'utilisateur veut envoyer une commande
## ou bien en taper une avec un argument
while connexion == True:
    print("Connaissez vous la commande à envoyer (Y/N ; Q)")
    choice = input(" : ")
    choice = str.lower(choice)

    # ----------------------
    # ENVOYER UNE COMMANDE |
    # ----------------------
    if choice == 'n':
        while 1:
            print("Voici les différentes options : \n 0 : Changer de répertoire \n 1 : Afficher le répertoire courant \n 2 : Lister les fichiers du répertoire \n 3 : Créer un répertoire \n 4 : Supprimer un fichier \n 5 : Supprimer un répertoire \n 6 : Renommer un fichier \n 7 : Transférer un fichier \n 8 : Déplacer un fichier \n 9 : Quitter")
            try:
                opt = int(input("Quel option choisissez vous ?\n "))
            except ValueError:
                print("Entrer un nombre : ");continue

            if opt == 0:
                # change de repertoire (CWD)
                repertoire = input("Dans quel répertoire voulez vous aller ?: ")
                ftp.cwd(repertoire)
                print(" \n ---- \n")
            elif opt == 1:
                # afficher le répertoire courrant (PWD)
                print(ftp.pwd())
                print(" \n ---- \n")
            elif opt == 2: 
                # lister les fichiers (LIST)
                ftp.retrlines('LIST', callback=None) 
                print(" \n ---- \n")
            elif opt == 3:
                # créer le répertoire (MKD)
                nom_rep = input("Nommer le répertoire à créer (rép courant): ")
                try:
                    ftp.mkd(nom_rep)
                    print("Le répertoire " + nom_rep + " a été créé.")
                except:
                    print("\n /!\ /!\ /!\ \n Problème lors de la création du répertoire. Assurez vous que le nom soit correct.")
                print(" \n ---- \n")
            elif opt == 4:
                # supprimer un fichier (DELE)
                nom_fic = input("Indiquer le nom du fichier à supprimer: ")
                try:
                    ftp.delete(nom_fic)
                    print("Le fichier " + nom_fic + " a été supprimé.")
                except FileNotFoundError:
                    print("Fichier non trouvé.")
                print(" \n ---- \n")
            elif opt == 5:
                # supprime le répertoire (RMD)
                nom_dos = input("Indiquer le répertoire à supprimer : ")
                try:
                    ftp.rmd(nom_dos)
                    print("Le répertoire " + nom_dos + " a été supprimé.")
                except:
                    print("\n /!\ /!\ /!\ \n Problème lors de la suppresion du répertoire. Assurez vous qu'il soit vide.")
                print(" \n ---- \n")
            elif opt == 6:
                # renomme le fichier (RNFR)
                name = input("Indiquer le nom du fichier à renommer : ")
                new_name = input(print("Indiquer le nouveau nom : "))
                try:
                    ftp.rename(name, new_name)
                except FileNotFoundError:
                    print("Fichier non trouvé.")
                print(" \n ---- \n")
            elif opt == 7:
                # Envoie le fichier (STOR)
                nom_fic = input("Entrer le nom du fichier à transférer : ")
                try:
                    ftp.storlines('STOR ' + nom_fic, open(nom_fic,'rb'))
                except FileNotFoundError:
                    print("\n /!\ /!\ /!\ \n Problème lors du transfert. Fichier non trouvé.")
                print(" \n ---- \n")
            elif opt == 8:
                # déplace le fichier
                nom_fic = input("Indiquer le fichier à déplacer : ")
                dest_fic = input("Indiquer l'emplacement : ")
                try:
                    ftp.rename(nom_fic, dest_fic)
                except:
                    print("\n /!\ /!\ /!\ \n Problème lors du déplacement. Vérifier les chemins.")
                print(" \n ---- \n")
            elif opt == 9:
                break



    # -------------------------------------
    # TAPER UNE COMMANDE AVEC UN ARGUMENT |  A FINIR, ne marche pas
    # -------------------------------------
    elif choice == 'y':
        while 1:
            print("Voici les différentes commandes : CWD, DELE, LIST, MKD, RMD, RNFR, STOR.\n (Q pour quitter) ")
            comm = input("Entrer votre commande : ")
            
            #try:
            run(comm, shell = True, capture_output = True)
            #except:
            #print("Erreur de saisie")
            
            print(" \n ---- \n")
            
            if str.lower(comm) == 'q':
                break

        
    elif choice == 'q':
        print(" FTP session is closed. \n")
        print(" \n ---- \n")
        connexion = False

ftp.quit()