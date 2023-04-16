# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 18:53:02 2023

@author: thieu
"""

import json
import urllib
import urllib.request

#Récupération de la liste des villes
res = urllib.request.urlopen("https://api.jcdecaux.com/vls/v3/contracts?apiKey=e0a1bf2c844edb9084efc764c089dd748676cc14").read()
#On récupéère les informations au format chaîne de caractères
page = res.decode("utf8")
#On les mets ensuites dans une liste pour y accéder plus facilement
js = json.loads(page)
#On crée un dictionnaire vide que l'on utilisera pour classer les villes
ladder = {}
#On va parcourir la liste des villes
for i in range(len(js)-1):
    #Récupération des stations de chaque ville
    res_stat = urllib.request.urlopen("https://api.jcdecaux.com/vls/v3/stations?contract={}&apiKey=e0a1bf2c844edb9084efc764c089dd748676cc14".format(js[i]["name"])).read()
    page_stat = res_stat.decode("utf8")
    js_stat = json.loads(page_stat)
    total_mec = 0
    total_elec = 0
    name = js[i]["name"]
    #Nous allons maintenant récupérer les informations de toutes le stations
    for j in range(len(js_stat)-1):
        res_fin = urllib.request.urlopen("https://api.jcdecaux.com/vls/v3/stations/{}?contract={}&apiKey=e0a1bf2c844edb9084efc764c089dd748676cc14".format(js_stat[j]["number"],name)).read()
        page_fin = res_fin.decode("utf8")
        js_fin = json.loads(page_fin)
        #On va récupérer le nombre de vélos électriques et mécaniques de chaque ville
        total_mec += js_fin["totalStands"]["availabilities"]["mechanicalBikes"]
        total_elec += js_fin["totalStands"]["availabilities"]["electricalBikes"]
    #On additionne les deux types de vélos puis on ajoute le total dans le dictionnaire avec pour clé le nom de la ville
    ladder[name] = total_elec + total_mec
#On trie le dictionnaire de manière décroissante en fonction du nombre de vélo
sorted_ladder = dict(sorted(ladder.items(),key=lambda item:item[1],reverse=True))
#On imprime ensuite en sorite ce classement
print("Voici le classment des villes possédant le plus de vélo:")
for key, value in sorted_ladder.items():
    print("{} avec {} vélos".format(key,value))