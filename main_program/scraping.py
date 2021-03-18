#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup  
import requests
import re

class Scrap:
	def __init__(self, url):
		self.url = url
		self.set_soup()
		self.data = []




	def get_url(self):
		return self.url

	def get_data(self):
		return self.data

	def get_soup(self):
		return self.soup

	def set_soup(self):
		#on get les données de la page à partir de son url
		r = requests.get(self.url)
		#on extrait le texte brut de la page html 
		html_doc = r.text
		#on cherche à parser la page html 
		self.soup = BeautifulSoup(html_doc, 'html.parser')
		
	
	def scrap_elo(self):

		soup = self.soup
		list_strong = soup.find_all('strong')

		for texte in list_strong:
			if texte.string == "ELO Classic:":
				return texte.parent.parent.contents[-2].string

		return "pas de parties en classique"

	def scrap_partie(self):

		liste_partie = []
		soup = self.soup  
		div = soup.find('div', {'id' : 'mainfull'})
		table = div.find('table', {'class': 'stable'})
		tbody = table.find('tbody')
		list_tr = tbody.find_all('tr')

		for tr in list_tr:

			partie = []
			list_td = tr.find_all('td')

			for td in list_td:
				a = td.find('a')

				if a:

					data = None
					data = a.attrs['href']
					print(data)
					joueur = re.search(r'players/.*',data)
					
					if joueur:

						joueur = joueur.group(0)
						joueur = joueur.replace("players/", "")
						joueur = joueur.replace("_", " ")
						partie.append(joueur)
				
					elif a.get('title'):

						partie.append(a.string)
						
					elif a.get('onclick'):


						url_partie = a.attrs['onclick']
						url_partie = re.search(r'https://www.*popupgame',url_partie).group(0)
						url_partie = url_partie.replace("'","")
						url_partie = url_partie.replace(",","")	
						url_partie = url_partie.replace("popupgame","")	
						partie.append(url_partie)


			liste_partie.append(partie)

		return liste_partie
