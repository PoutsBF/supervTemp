from flask import Flask, render_template, url_for, request
import logging as lg

app = Flask(__name__)
app.config.from_object('config')

#from .utils import find_content

@app.route('/')
@app.route('/index/')
def index():
    if 'img' in request.args:
        img = request.args['img']
        og_url = url_for('index', img=img, _external=True)
        og_image = url_for('static', filename=img, _external=True)
    else:
        og_url = url_for('index', _external=True)
        og_image = url_for('static', filename='tmp/sample.jpg', _external=True)

    description = "Toi, tu sais comment utiliser la console ! "
    page_title = "Le test ultime"

    og_description = "Découvre qui tu es vraiment en faisant le test ultime !"
    return render_template('index.html',
                          user_name='Julio',
                          user_image=url_for('static', filename='img/profile.png'),
                          description=description,
                          blur=True,
                          page_title=page_title,
                          og_url=og_url,
                          og_image=og_image,
                          og_description=og_description)

if __name__ == "__main__":
    app.run()