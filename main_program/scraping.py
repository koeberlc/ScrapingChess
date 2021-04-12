#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import re


class Scrap:
    def __init__(self, url):
        '''
        Constructeur d'une instance de la classe Scrap
        '''
        self.url = url
        self.set_soup()
        self.liste_partie = []

    def get_url(self):
        '''
        Récupération de l'url

        returns :
            self.url(string)
        '''
        return self.url

    def get_soup(self):
        '''
        Récupération de la soup qui contient
        le code html de la page

        returns :
            self.soup(soup)
        '''
        return self.soup

    def get_liste_partie(self):
        '''
        Récupération de la liste des parties

        returns :
            self.liste_partei(list)
        '''
        return self.liste_partie

    def set_soup(self):
        '''
        Initilisation de la soup qui contient
        le code html de la page
        '''
        r = requests.get(self.url)

        html_doc = r.text

        self.soup = BeautifulSoup(html_doc, 'html.parser')

    def scrap_elo(self):
        '''
        Scrappe l'ELO du joueur.

        returns :
            String
        '''
        soup = self.soup
        list_strong = soup.find_all('strong')

        for texte in list_strong:
            if texte.string == "ELO Classic:":
                return int(texte.parent.parent.contents[-2].string)

        return "Pas de parties en classique"

    def scrap_data(self):
        '''
        Scrappe l'ensemble des parties du joueur.

        returns :
            self.get_liste_partie()(List)
        '''
        add_to_url = ""
        page = 1
        for a in self.soup.find_all("a", {"class": "pagination"}):
            if(a.string != "Next"):
                page = a.string

        for i in range(0, int(page)):
            print("new page")
            # on get les données de la page à partir de son url
            r = requests.get(self.url + "/?p=1&start=" + str(int(i) * 50))
            # on extrait le texte brut de la page html
            html_doc = r.text
            # on cherche à parser la page html
            soup = BeautifulSoup(html_doc, 'html.parser')
            self.scrap_partie(soup)
        return self.get_liste_partie()

    def scrap_mouvement(self, url):
        '''
        Scrappe les mouvements du joueur.

        args :
            url(string)

        returns : mouvement(list)
        '''
        mouvements = []

        r = requests.get(url)
        html_doc = r.text
        soup = BeautifulSoup(html_doc, 'html.parser')

        div = soup.find('div', {'id': 'GameTextLayerPopup'})
        list_a = div.find_all('a')

        for a in list_a:
            mouvements.append(a.string)

        return mouvements

    def scrap_partie(self, soup):
        '''
        Scrappe toutes les parties auxquelles le joueur a joué

        args :
            soup(soup)
        '''

        div = soup.find('div', {'id': 'mainfull'})
        table = div.find('table', {'class': 'stable'})
        tbody = table.find('tbody')
        list_tr = tbody.find_all('tr')

        for tr in list_tr:
            print("Récupération d'une nouvelle partie")
            partie = []
            list_td = tr.find_all('td')

            for td in list_td:
                a = td.find('a')

                if a:

                    data = None
                    data = a.attrs['href']

                    joueur = re.search(r'players/.*', data)

                    if joueur:

                        joueur = joueur.group(0)
                        joueur = joueur.replace("players/", "")
                        joueur = joueur.replace("_", " ")
                        partie.append(joueur)

                    elif a.get('title'):

                        partie.append(a.string)

                    elif a.get('onclick'):

                        url_partie = a.attrs['onclick']
                        url_partie = re.search(
                            r'https://www.*popupgame',
                            url_partie).group(0)
                        url_partie = url_partie.replace("'", "")
                        url_partie = url_partie.replace(", ", "")
                        url_partie = url_partie.replace("popupgame", "")

                        id_game = (re.search(r'g=[0-9]*', url_partie)).group(0)
                        id_game = id_game.replace("g=", "")
                        partie.append(id_game)

                        mouvements = self.scrap_mouvement(url_partie)
                        partie.append(mouvements)

                if(td.get("id") == "col-eco"):
                    a = td.find('a')
                    partie.append(a.string)

            
            self.liste_partie.append(partie)
