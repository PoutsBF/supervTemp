# supervTemp

## Commentaires à venir...
J'ai acheté des thermo/hygromètres Govee, qui ont la particularité d'être Bluetooth pour l'observation instantanée et pour l'acquisition longue durée.
Pour l'acquisition instantanée, un scan permet d'avoir en réponse un bloc contenant la température, l'hygrométrie et le niveau de batterie.
Des exemples de découvertes sont (crédits) :
- [GoveeBTTempLogger](https://github.com/wcbonner/GoveeBTTempLogger)
- [home is where you hang your hack](https://github.com/home-is-where-you-hang-your-hack/sensor.goveetemp_bt_hci) (protocole)
- [GoveeWatcher](https://github.com/Thrilleratplay/GoveeWatcher) (protocole)
- [Govee BT client](https://github.com/asednev/govee-bt-client)
- [GoveeTemperatureAndHumidity](https://github.com/neilsheps/GoveeTemperatureAndHumidity)
- [bluetooth-temperature-sensors](https://github.com/deepcoder/bluetooth-temperature-sensors)
- [homebridge-plugin-govee](https://github.com/asednev/homebridge-plugin-govee)
- [analyse](https://wimsworld.wordpress.com/2020/07/01/govee-gvh5075-thermometer-hygrometer/)
- [site Govee](https://eu.govee.com/collections/home-improvement)

Je suis intéressé par l'acquisition longue durée mais les informations sont difficiles à extraire (l'assistance Govee ne fournit pas les informations, une observation par WireShark sera nécessaire).

L'objectif de ce projet est donc :
- scan et acquisition des valeurs instantanées de 8 thermomètres
- Enregistrement dans 2 tables jointes (capteurs / datas) d'une base SQLite, à l'aide de l'ORM Flask-SQLAlchemy
- Web serveur Flask pour l'affichage des thermomètres, de l'implantation dans un plan, et la liste des dernières acquisitions

## Todo :
- mettre les infos temps réel en standby et passer le callback en websocket
- Intégrer les températures dans un plan
- mettre en place un graphe paramétré 
> 1 an / 1 mois / 1 semaine / 24h
- modifier les icones de batterie en réception des mises à jour


## Sources / bibliothèques
### Flask
Web serveur 
- [documentation Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [tutorial Flask](https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3-fr)

### Flask-SQLalchemy
ORM (Object-Relational Mapping) pour l'accès à la BDD
- [documentation Flask SQL Alchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)

### WebSocket
Gestion des webservices (pour la mise à jour des champs en asynchrone et dans le cas de mise à jour)
#### Flask-SocketIO
- ~~[documentation Flask Socket IO](https://flask-socketio.readthedocs.io/)~~
gestion d'une communication en mode polling, ne répond pas à mes attentes (surcharge du médium de communication, fait tourner du code inutilement sur le client !)

#### Flask-Sockets
- ~~[Flask Sockets](https://github.com/heroku-python/flask-sockets)~~
- ~~[documentation flask-sockets](https://devcenter.heroku.com/articles/python-websockets)~~
Premier essai non concluant. Après changement, c'était l'adresse en javascript qui était mauvaise.

#### Flask-SocketIO
- ~~[Flask Sockets](https://github.com/heroku-python/flask-sockets)~~
gestion d'une communication en mode polling, ne répond pas à mes attentes (surcharge du médium de communication, fait tourner du code inutilement sur le client !)

### Bleak (Bluetooth)
Interface windows et raspbian pour l'utilisation du Bluetooth
- [documentation Bleak](https://bleak.readthedocs.io/)
- [projet Bleak](https://pypi.org/project/bleak/)
- [Github Bleak](https://github.com/hbldh/bleak/tree/master)

### Bootstrap
Template pour la page HTML
- [https://getbootstrap.com/](https://getbootstrap.com/ "site Bootstrap")

### Bootstrap table
Gestion des tableaux HTML : filtre / tri / pagination notamment
- [https://bootstrap-table.com/](https://bootstrap-table.com/ "Site Bootstrap-table")

## Outils
### LayouIT
Pour la création assistée du template Bootstrap
- [https://www.layoutit.com/](https://www.layoutit.com/ "Site layout it")


----

*Texte en italique*
_Texte en italique_
**Texte en gras**
__Texte en gras__
***Texte en italique et en gras***
___Texte en italique et en gras___
~~Ce texte est barré.~~ mais pas celui-là.
#  Titre 1
## Titre 2
###  Titre 3
#### Titre 4
#####  Titre 5
###### Titre 6

Titre 1
=
Titre 2
-

>Ceci est une **zone en retrait**.
>La zone continue ici

>Ceci est une autre **zone de retrait**.
Cette zone continue également dans la ligne suivante.
Cependant, cette ligne n’est plus en retrait

- Liste1
- Liste 2
- Liste 3

1. Liste 1
2. Liste 2
3. Liste 3

[ ] A
[x] B
[ ] C

C’est le `code`.
``C’est tout le `code`.``

```html
<html>
  <head>
  </head>
</html>
```

Ici ce qui suit [Lien](https://example.com/ "titre de lien optionnel").

![Ceci est un exemple d’image](https://example.com/bild.jpg)

|cellule 1|cellule 2|
|--------|--------|
|    A    |    B    |
|    C    |    D    |

Dans le texte ordinaire [^1] vous pouvez facilement placer des notes de bas de page [^2]
[^1]: Vous trouverez ici le texte de la note de bas de page.
 [^2]: **Note de page de page** peut aussi être *formatée*.
Et celles-ci comprennent même plusieurs lignes

A & B
&alpha;
1 < 2
<p>

Ceci est un \*exemple avec des astérisques\*.
Ceci est un *exemple des astérisques sans antislash*.