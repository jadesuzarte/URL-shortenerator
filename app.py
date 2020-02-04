from flask import Flask, request, jsonify, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import secrets
import os  # python module to deal with file paths

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Product Class/Model


class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    longg = db.Column(db.String)
    short = db.Column(db.String)

    def __init__(self, longg, short):
        self.longg = longg
        self.short = short

# Product Schema


class URLSchema(ma.Schema):
    class Meta:
        fields = ('id', 'longg', 'short')


# initialise schema
URL_schema = URLSchema()
URLs_schema = URLSchema(many=True)

def key():
    return secrets.token_urlsafe(10)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def add():
    url_long = request.form['content']
    url_key = key()
    new_url = URL(url_long, url_key)

    try:
        db.session.add(new_url)
        db.session.commit()
        return render_template('added.html', url=url_key)
    except:
        return 'There was an issue adding your task'

@app.route('/<key>', methods=['GET'])
def get_url(key):
    product = URL.query.filter(URL.short == key).first().longg
    return redirect(product)

@app.route('/all', methods=['GET'])
def get_all():
    all_urls = URL.query.all()
    result = URLs_schema.dump(all_urls)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
