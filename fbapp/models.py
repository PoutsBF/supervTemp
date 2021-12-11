#from flask_sqlalchemy import SQLAlchemy

import datetime

from .views import app

govee_devices = {'A4:C1:38:7B:49:14': {'name': 'GVH5075_4914', 'identifiant': 'chambre Maxine'},
                 'A4:C1:38:0F:48:6E': {'name': 'GVH5075_486E', 'identifiant': 'véranda'},
                 'A4:C1:38:1A:00:22': {'name': 'GVH5075_0022', 'identifiant': 'garage'},
                 'A4:C1:38:4B:28:8E': {'name': 'GVH5075_288E', 'identifiant': 'chambre Martin'},
                 'A4:C1:38:F3:DC:A8': {'name': 'GVH5075_DCA8', 'identifiant': 'salle de bain'},
                 'A4:C1:38:3D:F7:8A': {'name': 'GVH5075_F78A', 'identifiant': 'chambre parents'},
                 'A4:C1:38:86:C6:6F': {'name': 'GVH5075_C66F', 'identifiant': 'Salle à manger'},
                 'A4:C1:38:2A:88:5D': {'name': 'GVH5075_885D', 'identifiant': 'mobile'}}

class Capteur:

    def __init__(self, **kwargs):
        kwargs.get("name")
        self.mac = ""
        self.name = ""
        self.identifiant = ""

class DataEnvironnement:
    def __init__(self, description, gender):
        self.capteur = Capteur()
        self.temperature = 0.0
        self.hygrometrie = 0.0
        self.timeStamp = datetime.datetime.now()

def init_models():

    pass

init_models()
