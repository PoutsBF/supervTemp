import random
import logging as lg
from sqlalchemy import func
from datetime import date, datetime, time, timedelta

from .models  import db, data_environnement, capteurs, init_models

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
        init_models()

    retour = []
    if etendue == "all":
        req = db.session.query(data_environnement.idCapteur, \
                               func.max(data_environnement.timeStamp), \
                               capteurs.location, \
                               data_environnement.temperature, \
                               data_environnement.hygrometrie, \
                               data_environnement.batterie)\
                .group_by(data_environnement.idCapteur)\
                .where(data_environnement.idCapteur==capteurs.id)\
                .all()

    elif etendue == "instant":
        req = db.session.query(data_environnement.idCapteur, \
                               data_environnement.timeStamp, \
                               capteurs.location, \
                               data_environnement.temperature, \
                               data_environnement.hygrometrie, \
                               data_environnement.batterie)\
                .where(data_environnement.idCapteur==capteurs.id)\
                .order_by(data_environnement.timeStamp)\
                .all()

    else:
        pass

    # col = req[0].keys
    # print(req[0].keys())

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
