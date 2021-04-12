from math import *
from collections import Counter
import statistics
from statistics import mean


class Analyse:

    def __init__(self, list_partie, name, elo):
        '''
        Constructeur d'une instance de la classe Analyse
        '''
        self.data = {}
        self.data["joueur"] = name.replace("_", " ")
        self.data["elo"] = elo
        self.data["partie"] = {}
        self.data["partie"]["nombre"] = 0
        self.data["partie"]["victoire"] = 0
        self.data["partie"]["defaite"] = 0
        self.data["partie"]["nul"] = 0

        self.data["ouverture"] = {}
        self.data["ouverture"]["total"] = []
        self.data["ouverture"]["gagnant"] = []
        self.data["ouverture"]["perdant"] = []

        self.data["coups"] = {}
        self.data["coups"]["nb_coups"] = []
        self.data["coups"]["nb_moyen"] = 0

        self.raw_data = list_partie

        self.setData()

    def setData(self):
        '''
        Création mise en forme des données en fonction
        des parties récupérées
        '''
        for partie in self.raw_data:
            self.increment_nb_partie()
            self.add_ouverture(partie[3])
            self.add_coups(ceil(len(partie[5])/2))

            score = ""
            if partie[0] == self.data["joueur"]:
                score = partie[2][0]
            else:
                score = partie[2][-1]

            if score == "1":
                self.increment_victoire()
                self.add_ouverture_gagnant(partie[3])
            elif score == "0":
                self.add_ouverture_perdant(partie[3])
                self.increment_defaite()
            else:
                self.increment_nul()

        self.set_coups_moyen()

    def increment_nb_partie(self):
        '''
        Incrementation du nombre de partie
        '''
        self.data["partie"]["nombre"] += 1

    def increment_victoire(self):
        '''
        Incrementation du nombre de victoires
        '''
        self.data["partie"]["victoire"] += 1

    def increment_defaite(self):
        '''
        Incrementation du nombre de défaites
        '''
        self.data["partie"]["defaite"] += 1

    def increment_nul(self):
        '''
        Incrementation du nombre de matches nuls
        '''
        self.data["partie"]["nul"] += 1

    def add_ouverture(self, ouverture):
        '''
        Ajout d'une ouverture utilisée
        '''
        self.data["ouverture"]["total"].append(ouverture)

    def add_ouverture_gagnant(self, ouverture):
        '''
        Ajout d'une ouverture utilisée lors d'une partie gagnante
        '''
        self.data["ouverture"]["gagnant"].append(ouverture)

    def add_ouverture_perdant(self, ouverture):
        '''
        Ajout d'une ouverture utilisée lors d'une partie perdante
        '''
        self.data["ouverture"]["perdant"].append(ouverture)

    def add_coups(self, nombre):
        '''
        Ajout d'un nombre de coups effectué lors d'une partie
        '''
        self.data["coups"]["nb_coups"].append(nombre)

    def set_coups_moyen(self):
        '''
        Calcul de la moyenne de coups joués
        '''
        somme = 0
        list_nb_coups = self.data["coups"]["nb_coups"]
        for nb in list_nb_coups:
            somme += nb

        self.data["coups"]["nb_moyen"] = somme/len(list_nb_coups)
    def get_data(self):
        '''
        Récupération de l'ensemble des données

        returns :
            self.data(dict)
        '''
        return self.data
    def get_nombre_partie(self):
        '''
        Récupération du nombre de parties jouées

        returns :
            self.data["partie"]["nombre"](int)
        '''
        return self.data["partie"]["nombre"]

    def get_nombre_victoire(self):
        '''
        Récupération du nombre de victoires

        returns :
            self.data["partie"]["victoire"](int)
        '''
        return self.data["partie"]["victoire"]

    def get_nombre_defaite(self):
        '''
        Récupération du nombre de défaites

        returns :
            self.data["partie"]["defaite"](int)
        '''
        return self.data["partie"]["defaite"]

    def get_nombre_nul(self):
        '''
        Récupération du nombre de parties nulles

        returns :
            self.data["partie"]["nul"](int)
        '''
        return self.data["partie"]["nul"]

    def get_ouverture_total(self):
        '''
        Récupération de toutes les ouvertures jouées

        returns :
            self.data["ouverture"]["total"](list)
        '''
        return self.data["ouverture"]["total"]

    def get_ouverture_gagnant(self):
        '''
        Récupération de toutes les ouvertures gagnantes

        returns :
            self.data["ouverture"]["gagnant"](list)
        '''
        return self.data["ouverture"]["gagnant"]

    def get_ouverture_perdant(self):
        '''
        Récupération de toutes les ouvertures perdantes

        returns :
            self.data["ouverture"]["perdant"](list)
        '''
        return self.data["ouverture"]["perdant"]

    def get_nombre_coups(self):
        '''
        Récupération du nombre de coups de toutes les parties

        returns :
            self.data["coups"]["nb_coups"](list)
        '''
        return self.data["coups"]["nb_coups"]

    def get_nombre_moyen_coups(self):
        '''
        Récupération de la moyenne du nombre de coups joués

        returns :
            self.data["coups"]["nb_moyen"](float)
        '''
        return self.data["coups"]["nb_moyen"]

    def get_ouverture_plus_utilise(self):
        '''
        Analyse de l'ouverture la plus utilisée

        returns :
            (tupple)
        '''
        return Counter(self.get_ouverture_total()).most_common(1)[0]

    def get_ouverture_plus_gagnant(self):
        '''
        Analyse de l'ouverture la plus utilisée sur une partie gagnante

        returns :
            (tupple)
        '''
        return Counter(self.get_ouverture_gagnant()).most_common(1)[0]

    def get_ouverture_plus_perdant(self):
        '''
        Analyse de l'ouverture la plus utilisée sur une partie perdante

        returns :
            (tupple)
        '''
        return Counter(self.get_ouverture_perdant()).most_common(1)[0]

    def get_taux_victoire(self):
        '''
        Analyse du taux de victoire du joueur

        returns :
            (tupple)
        '''
        result = (self.get_nombre_victoire() + self.get_nombre_nul() / 2)
        result /= self.get_nombre_partie()
        result *= 100
        return round(result, 2)
