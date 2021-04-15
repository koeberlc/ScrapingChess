#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import csv
import json
import re
import requests
from main_program.scraping import Scrap
from main_program.database import Database
from main_program.analyse import Analyse


def main():

    url, nom = menu()

    reviews_data = []

    scrap = Scrap(url)

    elo = scrap.scrap_elo()

    list_partie = scrap.scrap_data()

    saisie = askSave()
    if(saisie == "1"):
        db = Database()
        db.saveBDD(list_partie)

    analyse = Analyse(list_partie, nom, elo)
    foldername = nom
    with open('result/' + foldername + '.json', 'w', encoding='utf8') as outfile:
            json.dump(analyse.get_data(), outfile, indent=4, ensure_ascii=False)

    saisie = askAnalyse()
    if saisie == "1":
        while 1:
            saisie = chooseAnalyse()
            if saisie == "1":
                print(analyse.get_nombre_partie())
            elif saisie == "2":
                print(analyse.get_nombre_victoire())
            elif saisie == "3":
                print(analyse.get_nombre_moyen_coups())
            elif saisie == "4":
                print(analyse.get_ouverture_plus_utilise())
            elif saisie == "5":
                print(analyse.get_ouverture_plus_gagnant())
            elif saisie == "6":
                print(str(analyse.get_taux_victoire()) + "%")
            else:
                break


def askSave():
    '''
    Demande à l'utilisateur s'il veut enregistrer
    les données dans la BDD ou non.

    returns :
        saisie(String)

    '''
    choix = ["1", "2"]
    print("---------------------------------------")
    print("Voulez-vous sauvegarder les données dans la BDD")
    print("1/ Oui")
    print("2/ Non")
    print("---------------------------------------")
    saisie = input("Saisie : ")
    if(saisie not in choix):
        print("Erreur saisie")
        return askSave()
    return saisie


def askAnalyse():
    '''
    Demande à l'utilisateur s'il veut analyser
    les données ou non.

    returns :
        saisie(String)

    '''
    choix = ["1", "2"]
    print("---------------------------------------")
    print("Voulez-vous obtenir des statistiques complémentaires ?")
    print("1/ oui")
    print("2/ non")
    print("---------------------------------------")
    saisie = input("Saisie : ")

    if(saisie not in choix):
        print("Erreur saisie")
        return askAnalyse()

    return saisie


def chooseAnalyse():
    '''
    Demande à l'utilisateur s'il l'analyse qu'il
    souhaite effectuer.

    returns :
        saisie(String)

    '''
    choix = ["1", "2", "3", "4", "5", "6", "7"]
    print("---------------------------------------")
    print("1/ Nombre de parties jouées")
    print("2/ Nombre de victoire")
    print("3/ Le nombre de coups moyen")
    print("4/ L'ouverture la plus utilisée")
    print("5/ L'ouverture la plus maitrisée")
    print("6/ Le taux de victoire du joueur")
    print("7/ Quitter")
    print("---------------------------------------")
    saisie = input("Saisie : ")
    if(saisie not in choix):
        print("Erreur saisie")
        return chooseAnalyse()
    return saisie


def menu():
    '''
    Demande à l'utilisateur d'input un nom et un prénom et renvoie
    l'URL associée.

    returns :
        requete(String)
    '''
    nom = input("Saisir le prenom et nom d'un joueur (ex: Magnus Carlsen) : ")
    nom = nom.replace(" ", "_")
    # nom = "Magnus_Carlsen"
    requete = 'https://www.365chess.com/players/' + nom
    return requete, nom


main()
