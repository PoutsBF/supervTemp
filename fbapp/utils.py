import random
import logging as lg
from sqlalchemy import func
from sqlalchemy.orm.attributes import QueryableAttribute
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

# example using BaseThread with callback

def async_majBLE():
# Met à jour les données en faisant un scan Bluetooth
# Enregistre les données dans la base de données
# Met en forme les données pour les renvoyer pour affichage

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

    # Requête les dernières données sur chaques capteurs
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


""" ----------------------------------------------------------------------------------------
"""
def to_dict(self, show=None, _hide=None, _path=None):
    """Return a dictionary representation of this model."""

    show = show or []
    _hide = _hide or []

    hidden = self._hidden_fields if hasattr(self, "_hidden_fields") else []
    default = self._default_fields if hasattr(self, "_default_fields") else []
    default.extend(['id', 'modified_at', 'created_at'])

    if not _path:
        _path = self.__tablename__.lower()

        def prepend_path(item):
            item = item.lower()
            if item.split(".", 1)[0] == _path:
                return item
            if len(item) == 0:
                return item
            if item[0] != ".":
                item = ".%s" % item
            item = "%s%s" % (_path, item)
            return item

        _hide[:] = [prepend_path(x) for x in _hide]
        show[:] = [prepend_path(x) for x in show]

    columns = self.__table__.columns.keys()
    relationships = self.__mapper__.relationships.keys()
    properties = dir(self)

    ret_data = {}

    for key in columns:
        if key.startswith("_"):
            continue
        check = "%s.%s" % (_path, key)
        if check in _hide or key in hidden:
            continue
        if check in show or key in default:
            ret_data[key] = getattr(self, key)

    for key in relationships:
        if key.startswith("_"):
            continue
        check = "%s.%s" % (_path, key)
        if check in _hide or key in hidden:
            continue
        if check in show or key in default:
            _hide.append(check)
            is_list = self.__mapper__.relationships[key].uselist
            if is_list:
                items = getattr(self, key)
                if self.__mapper__.relationships[key].query_class is not None:
                    if hasattr(items, "all"):
                        items = items.all()
                ret_data[key] = []
                for item in items:
                    ret_data[key].append(
                        item.to_dict(
                            show=list(show),
                            _hide=list(_hide),
                            _path=("%s.%s" % (_path, key.lower())),
                        )
                    )
            else:
                if (
                    self.__mapper__.relationships[key].query_class is not None
                    or self.__mapper__.relationships[key].instrument_class
                    is not None
                ):
                    item = getattr(self, key)
                    if item is not None:
                        ret_data[key] = item.to_dict(
                            show=list(show),
                            _hide=list(_hide),
                            _path=("%s.%s" % (_path, key.lower())),
                        )
                    else:
                        ret_data[key] = None
                else:
                    ret_data[key] = getattr(self, key)

    for key in list(set(properties) - set(columns) - set(relationships)):
        if key.startswith("_"):
            continue
        if not hasattr(self.__class__, key):
            continue
        attr = getattr(self.__class__, key)
        if not (isinstance(attr, property) or isinstance(attr, QueryableAttribute)):
            continue
        check = "%s.%s" % (_path, key)
        if check in _hide or key in hidden:
            continue
        if check in show or key in default:
            val = getattr(self, key)
            if hasattr(val, "to_dict"):
                ret_data[key] = val.to_dict(
                    show=list(show),
                    _hide=list(_hide),
                    _path=('%s.%s' % (_path, key.lower())),
                )
            else:
                try:
                    ret_data[key] = json.loads(json.dumps(val))
                except:
                    pass

    return ret_data