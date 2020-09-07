from flask import Flask

from heroes_app.db import DBClass

app = Flask(__name__)

db_class = DBClass()


@app.route("/")
def index():
    return "Welcome to the hero page"


@app.route("/hero/<name>", methods=['GET'])
def single_hero(name):

    return db_class.get_hero_as_df(name).to_html()


@app.route("/all")
def all_heroes():
    df = db_class.heroes_to_df()

    df.set_index(['name'], inplace=True)
    df.index.name = None

    return df.to_html()
