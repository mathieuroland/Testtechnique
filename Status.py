# -*- coding: utf-8 -*-
"""
@author: thieu
"""
#Le fichier status liste les stations ouvertes de chaque ville

import json
import urllib
import urllib.request

#Récupération de la liste des villes
res = urllib.request.urlopen("https://api.jcdecaux.com/vls/v3/contracts?apiKey=e0a1bf2c844edb9084efc764c089dd748676cc14").read()
#On récupéère les informations au format chaîne de caractères
page = res.decode("utf8")
#On les mets ensuites dans une liste pour y accéder plus facilement
js = json.loads(page)
#On va parcourir la liste des villes
for i in range(len(js)-1):
    #Récupération des stations de chaque ville
    res_stat = urllib.request.urlopen("https://api.jcdecaux.com/vls/v3/stations?contract={}&apiKey=e0a1bf2c844edb9084efc764c089dd748676cc14".format(js[i]["name"])).read()
    page_stat = res_stat.decode("utf8")
    js_stat = json.loads(page_stat)
    name = js[i]["name"]
    print("Voici les stations ouverte à {} :".format(name))
    #Nous allons maintenant récupérer les informations de toutes le stations
    for j in range(len(js_stat)-1):
        #On récupère les informations d'une station grace à son number
        res_fin = urllib.request.urlopen("https://api.jcdecaux.com/vls/v3/stations/{}?contract={}&apiKey=e0a1bf2c844edb9084efc764c089dd748676cc14".format(js_stat[j]["number"],name)).read()
        page_fin = res_fin.decode("utf8")
        js_fin = json.loads(page_fin)
        #On vérifie si le status de la station est open
        if (js_fin["status"] == "OPEN"):
            print("{}".format(js_fin["name"]))
    print("\n")