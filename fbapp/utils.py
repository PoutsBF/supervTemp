import random
import logging as lg
from sqlalchemy import func
from datetime import date, datetime, time, timedelta
import threading
import asyncio

from .models  import db, data_environnement, capteurs, init_models
from .controlBLE import scanner_loop

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
                .limit(100)\
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

async def async_majBLE():
    data_recepts = asyncio.run(scanner_loop())
    for mac in data_recepts:
        cCapteur = capteurs.query.filter(capteurs.name == data_recepts[mac]["name"]).all()
        idCapteur = cCapteur[0].id
        nvData = data_environnement(idCapteur=idCapteur, 
                                    timeStamp=data_recepts[mac]["timeStamp"], 
                                    temperature=data_recepts[mac]["temperature"], 
                                    hygrometrie=data_recepts[mac]["hygrometrie"], 
                                    batterie=data_recepts[mac]["batterie"])

    db.session.add(nvData)
    db.session.commit()

    req = db.session.query(data_environnement.idCapteur, \
                            data_environnement.timeStamp, \
                            capteurs.location, \
                            data_environnement.temperature, \
                            data_environnement.hygrometrie, \
                            data_environnement.batterie)\
                    .where(data_environnement.idCapteur==capteurs.id)\
                    .order_by(data_environnement.timeStamp)\
                    .all()
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

    cb_retour(retour)

