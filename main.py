#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

import csv
import json 
import re
import urllib.request

from main_program.scraping import Scrap





def main():
    url = menu()

    reviews_data = []
    
    scrap = Scrap(url)

    scrap.scrap_elo()
    print(scrap.scrap_partie())

        
    

def menu():
    nom = input("Saisir le prenom et nom d'un joueur (ex: Magnus Carlsen) : ")
    nom = nom.replace(" ", "_")

    return 'https://www.365chess.com/players/' + nom


main()
