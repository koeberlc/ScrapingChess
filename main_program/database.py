#!/usr/bin/python
# -*- coding: utf-8 -*-

import mysql.connector as MySQLdb

class Database:
    def __init__(self):
        '''
        Constructeur d'une instance de la classe Database
        '''
        self.connexion = self.seConnecter()

    def get_connexion(self):
        '''
        Récupération de la connexion

        returns :
            self.connexion(objet mysql.connector)
        '''
        return self.connexion

    def seConnecter(self):
        '''
        Etablissement de la connexion à la BDD.

        returns :
            connexion(objet mysql.connector)
        '''
        # Pour modifier la connexion à la base de données, il
        # faut modifier les lignes suivantes
        connexion = MySQLdb.connect(
            user="root",  # Database User
            host="localhost",  # Database IP (server IP)
            database="proj632_chess")  # Database name

        print("Connecté")

        return connexion

    def saveBDD(self, list_partie):
        '''
        Sauvegarde des parties dans la base de données

        args = list_partie(List)
        '''

        self.connexion

        curseur = self.connexion.cursor(buffered=True)

        # On sauvegarde chaque element de data
        for partie in list_partie:
            game_exist = False

            requete = "select id_game from game"
            curseur.execute(requete)

            # On verifie que l'utilisateur n'existe pas deja
            # Afin d'éviter les doublons
            for c in curseur.fetchall():
                if str(partie[4]) == str(c[0]):
                    game_exist = True

            # S'il n'existe pas on l'insert
            if(not game_exist):
                requete = "insert into game values (" + partie[4] + ", '"
                requete += partie[0] + "', '" + partie[1] + "', '" + partie[2]
                requete += "', '" + ','.join(partie[5]) + "')"
                curseur.execute(requete)
                print("Données sauvegardées")
            else:
                print("Données déjà sauvegardées")
        self.connexion.commit()
