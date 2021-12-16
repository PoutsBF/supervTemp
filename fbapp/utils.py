import random
import logging as lg
from sqlalchemy import func


from .models  import db, data_environnement, capteurs


def find_content():
    retour = []
    retour.insert(0, ("#", "heure", "lieu", "température", "hygrométrie", "batterie"))
    retour = db.session.query(data_environnement.idCapteur, \
                            func.max(data_environnement.timeStamp), \
                            capteurs.location, \
                            data_environnement.temperature, \
                            data_environnement.hygrometrie, \
                            data_environnement.batterie)\
        .group_by(data_environnement.idCapteur)\
        .where(data_environnement.idCapteur==capteurs.id)\
        .all()


    return retour
