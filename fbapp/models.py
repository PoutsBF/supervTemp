from os import device_encoding
from flask import sessions
from flask_sqlalchemy import SQLAlchemy
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/

import datetime, asyncio
import logging as lg
import sqlalchemy

from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.operators import nullsfirst_op
from .controlBLE import scanner_loop
from .views import app

govee_devices = {'A4:C1:38:7B:49:14': {'name': 'GVH5075_4914', 'identifiant': 'chambre Maxine'},
                 'A4:C1:38:0F:48:6E': {'name': 'GVH5075_486E', 'identifiant': 'véranda'},
                 'A4:C1:38:1A:00:22': {'name': 'GVH5075_0022', 'identifiant': 'garage'},
                 'A4:C1:38:4B:28:8E': {'name': 'GVH5075_288E', 'identifiant': 'chambre Martin'},
                 'A4:C1:38:F3:DC:A8': {'name': 'GVH5075_DCA8', 'identifiant': 'salle de bain'},
                 'A4:C1:38:3D:F7:8A': {'name': 'GVH5075_F78A', 'identifiant': 'chambre parents'},
                 'A4:C1:38:86:C6:6F': {'name': 'GVH5075_C66F', 'identifiant': 'Salle à manger'},
                 'A4:C1:38:2A:88:5D': {'name': 'GVH5075_885D', 'identifiant': 'mobile'}}

db = SQLAlchemy(app)

# CREATE TABLE `Capteurs` (
#   `idCapteur` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
#   `mac_addr` MEDIUMTEXT(17) NULL DEFAULT NULL,
#   `location` MEDIUMTEXT(20) NULL DEFAULT NULL,
#   `name` MEDIUMTEXT(15) NULL DEFAULT NULL,
#   PRIMARY KEY (`idCapteur`)
# );
class capteurs(db.Model):
    __tablename__ = "capteurs"
    id = db.Column(db.Integer, primary_key=True)
    mac_addr = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(15), nullable=False)

    Rcapteur = db.relationship('data_environnement', backref='capteurs', uselist=False, lazy=True)

    def __init__(self, **kwargs):
        self.mac_addr = kwargs.get("mac_addr", "")
        self.location = kwargs.get("location", "")
        self.name = kwargs.get("name", "")

    def __repr__(self):
            return f'[id{self.id}]- {self.mac_addr} - {self.location} - {self.name}'


# CREATE TABLE `Datas` (
#   `id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
#   `idCapteur` INTEGER NULL DEFAULT NULL,
#   `timeStamp` DATETIME NULL DEFAULT NULL,
#   `temperature` FLOAT NULL DEFAULT NULL,
#   `hygrometrie` FLOAT NULL DEFAULT NULL,
#   `batterie` TINYINT NULL DEFAULT NULL,
#   PRIMARY KEY (`id`)
# );
class data_environnement(db.Model):
    __tablename__ = "data_environnement"
    id = db.Column(db.Integer, primary_key=True)
    idCapteur = db.Column(db.Integer, db.ForeignKey('capteurs.id'), nullable=False)

    timeStamp = db.Column(db.DateTime, nullable=False)
    temperature = db.Column(db.Float, nullable=True)
    hygrometrie = db.Column(db.Float, nullable=True)
    batterie = db.Column(db.Integer, nullable=True)

    def __init__(self, **kwargs):
        self.idCapteur = kwargs.get("idCapteur", 0)
        self.timeStamp = kwargs.get("timeStamp", datetime.datetime.now())
        self.temperature = kwargs.get("temperature", Null)
        self.hygrometrie = kwargs.get("hygrometrie", Null)
        self.batterie = kwargs.get("batterie", Null)

    def __repr__(self):
            return f'[id{self.id}]- {self.idCapteur} - {self.timeStamp} - {self.temperature} - {self.hygrometrie} - {self.batterie}'

def init_models():
    # ## Only first time : todo, test à la première création...
    # db.drop_all()
    # db.create_all()
    # for c_govee in govee_devices:
    #     nvCapteur = capteurs(mac_addr = c_govee, location = govee_devices[c_govee]["identifiant"], name = govee_devices[c_govee]["name"])
    #     lg.warning(nvCapteur)
    #     db.session.add(nvCapteur)
    # db.session.commit()
    # lg.warning('Database initialized !')
    data_recepts = asyncio.run(scanner_loop())
    print(data_recepts)
    for mac in data_recepts:
        ajout_data( mac=mac, 
                    timeStamp=data_recepts[mac]["timeStamp"], 
                    temperature=data_recepts[mac]["temperature"],
                    hygrometrie=data_recepts[mac]["hygrometrie"],
                    batterie=data_recepts[mac]["batterie"],
                    name=data_recepts[mac]["name"])
    lg.warning('BLE ok')

def ajout_data(**kwargs):
    mac = kwargs.get("mac")
    if mac != None:
        timeStamp = kwargs.get("timeStamp", "") 
        temperature = kwargs.get("temperature", Null)
        hygrometrie = kwargs.get("hygrometrie", Null)
        batterie = kwargs.get("batterie", Null)
        name = kwargs.get("name", "")

    cCapteur = capteurs.query.filter(capteurs.name == name).all()
    idCapteur = cCapteur[0].id
    nvData = data_environnement(idCapteur=idCapteur, timeStamp=timeStamp, temperature=temperature, hygrometrie=hygrometrie, batterie=batterie)
    lg.warning(nvData)
    db.session.add(nvData)
    db.session.commit()
    lg.warning('Data ajouté !')

init_models()

# https://docs.sqlalchemy.org/en/14/orm/query.html
# https://www.it-swarm-fr.com/fr/python/flask-sqlalchemy-ou-sqlalchemy/1071549488/
# https://www.it-swarm-fr.com/fr/python/flask-sqlalchemy-verifie-si-une-ligne-existe-dans-la-table/1055082755/

sqlalchemy.select(data_environnement.idCapteur, sqlalchemy.func.max())
result = sessions.execute(query).fetchall()

print(result)
