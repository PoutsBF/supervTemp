# -*- coding: utf-8 -*-
#! python3

from sqlalchemy import func
from datetime import date, datetime, time, timedelta
import threading
import asyncio

from .models  import db, data_environnement, capteurs, init_models
from .controlBLE import scanner_loop
import json

"""
------------ Décoration pour les variables statiques -------------
"""
def static(dict_var_val):
    def staticf(f):    
        def decorated(*args, **kwargs):
            for var, val in dict_var_val.items():
                if not (hasattr(decorated, var)):
                    setattr(decorated, var, val)
            return f(*args, **kwargs)
        return decorated
    return staticf

@static({'last_stamp': datetime.today()})
def find_content(etendue):
    if find_content.last_stamp < datetime.today() :
        find_content.last_stamp += timedelta(minutes=30)
        # init_models()

    retour = []
    if etendue == "instant":
        req = db.session.query(data_environnement.idCapteur, \
                               func.max(data_environnement.timeStamp), \
                               capteurs.location, \
                               data_environnement.temperature, \
                               data_environnement.hygrometrie, \
                               data_environnement.batterie)\
                .group_by(data_environnement.idCapteur)\
                .where(data_environnement.idCapteur==capteurs.id)\
                .all()

    elif etendue == "all":
        req = db.session.query(data_environnement.idCapteur, \
                               data_environnement.timeStamp, \
                               capteurs.location, \
                               data_environnement.temperature, \
                               data_environnement.hygrometrie, \
                               data_environnement.batterie)\
                .where(data_environnement.idCapteur==capteurs.id)\
                .order_by(data_environnement.timeStamp.desc())\
                .all()

    else:
        pass

    retour = []
    for line in req:
        retour_ligne = []
        for item in line:
            if(type(item) is float):
                retour_ligne.append("{:.1f}".format(item))
            elif(type(item) is datetime):
                retour_ligne.append(item.strftime("%d/%m/%y %H:%M"))
            else:
                retour_ligne.append(item)
        retour.append(retour_ligne)

    return retour

class BaseThread(threading.Thread):
    def __init__(self, callback=None, *args, **kwargs):
        target = kwargs.get('target')
        if target==None:
            target = async_majBLE
        super(BaseThread, self).__init__(target=self.target_with_callback, *args, **kwargs)
        self.callback = callback
        self.method = target

    def target_with_callback(self):
        result = self.method()
        if self.callback is not None:
            self.callback(result)

""" ---------------------------------------------------------------------------
    Timer pour faire un refresh des températures toutes les 15mn
"""
def scan():
#    threading.Timer((2*60.0), scan, args=[callback]).start() # bloque l'émission des messages web server
    # Lance un scan, tableau de données en retour
    data_recepts = asyncio.run(scanner_loop())

    # Boucle pour itérer les données reçues
    for mac in data_recepts:
        # Recherche l'ID dans la base en fonction du nom du capteur
        cCapteur = capteurs.query.filter(capteurs.name == data_recepts[mac]["name"]).all()
        idCapteur = cCapteur[0].id # sélectionne spécifiquement l'id
        # Prépare les données au format de la table de la base de données
        nvData = data_environnement(idCapteur=idCapteur, 
                                    timeStamp=data_recepts[mac]["timeStamp"], 
                                    temperature=data_recepts[mac]["temperature"], 
                                    hygrometrie=data_recepts[mac]["hygrometrie"], 
                                    batterie=data_recepts[mac]["batterie"])
        # Ajoute les données dans la base
        db.session.add(nvData)

    # A l'issue, enregistre les requêtes dans la base
    db.session.commit()

def async_majBLE():
    req = db.session.query(data_environnement.idCapteur, \
                            func.max(data_environnement.timeStamp), \
                            capteurs.location, \
                            data_environnement.temperature, \
                            data_environnement.hygrometrie, \
                            data_environnement.batterie)\
            .group_by(data_environnement.idCapteur)\
            .where(data_environnement.idCapteur==capteurs.id)\
            .all()
    # Met en forme les données pour l'affichage
    retour = {}
    pos = 1
    for line in req:
        retour[str(pos)] = {}
        col = 0
        for item in line:
            # nom_col = req[0].keys()._keys[col] // nom de colonne, mais il en manque une !!
            if(type(item) is float):    # Affichage des valeurs flottantes à 1 décimales
                retour[str(pos)][str(col)] = "{:.1f}".format(item)
            elif(type(item) is datetime): # Affichage jour/mois/année heure:minute
                retour[str(pos)][str(col)] = item.strftime("%d/%m/%y %H:%M")
            else:        # pas de changement
                retour[str(pos)][str(col)] = item
            col += 1
        pos += 1

    retour_complet = {}
    retour_complet["data"] = retour
    retour_complet["message"] = "majDataInst" 

    # col = req[0].keys
    # print(req[0].keys())
    
    retour_json = json.dumps(retour_complet)

    return retour_json