# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 02:02:01 2023

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
    #Selon le nombre de vélos de chaque types, la sortie du programme sera diéfférente
    #Cas où il y a deux type de vélos
    if (total_elec > 0 and total_mec > 0):
        print("{} possède un total de {} vélos mécaniques".format(name,total_mec))
        print("{} possède un total de {} vélos électriques".format(name,total_elec))
        ratio = (total_mec / (total_elec + total_mec))*100
        ratio_elec = 100 - ratio
        print("{} possède {}% vélo mécanique et {}% de vélo mécanique".format(name,ratio,ratio_elec))
    #Cas seulement des vélos électriques
    elif (total_elec > 0 and total_mec == 0):
        print("{} possède un total de {} vélos électriques".format(name,total_elec))
        print("{} n'a que des vélos électriques".format(name))
    #Cas seulement des vélos mécaniques 
    elif (total_elec == 0 and total_mec > 0):
        print("{} possède un total de {} vélos mécaniques".format(name,total_mec))
        print("{} n'a que des vélos mécaniques".format(name))
    #Aucun vélos
    else :
        print("{} n'a pas de vélo".format(name))
