import sqlite3
from contextlib import closing
from heroes_app.scrape import scrape_all, scrape_hero
import pandas as pd


DB_LOCATION = "db/heroes.db"
TABLE_NAME = 'heroes'

TABLE_FORMAT = {
    'url_name': 'text',
    'name': 'text',
    'health_points': 'integer',
    'damage_per_attack': 'integer',
    'attack_speed': 'integer',
    'mana': 'integer',
    'damage_per_second': 'float',
    'gold_price': 'integer',
    'attack_range': 'float',
    'hero_type': 'text',
    'release_date': 'text',
}


class DBClass:
    def __init__(self, loc=DB_LOCATION, table_name=TABLE_NAME, table_format=TABLE_FORMAT):
        self.conn = sqlite3.connect(loc)
        self.create_table(table_name, table_format)

    def create_table(self, table_name, table_format: dict):
        format_str = ', '.join([f'{key} {value}' for key, value in table_format.items()])
        self.run_query(sql_str=f"CREATE TABLE IF NOT EXISTS {table_name} ({format_str});")

    def run_query(self, sql_str, *args):
        conn = self.conn
        with closing(conn.cursor()) as cursor:
            result = cursor.execute(sql_str, tuple(args)).fetchall()

            conn.commit()
        return result

    def add_hero_to_db(self, hero_dict: dict, table_name):

        name = hero_dict['name']

        if len(self.get_hero_from_db(name, table_name)) > 0:
            self.run_query(f'DELETE FROM {table_name} WHERE name=?', name)

        keys = tuple([x.replace(' ', '_') for x in hero_dict.keys()])
        vals = tuple(list(hero_dict.values()))

        self.run_query(f'INSERT INTO {table_name} {keys} VALUES {vals};')

    def get_hero_from_db(self, hero_name, table_name):
        hero = self.run_query(f"SELECT * FROM {table_name} WHERE name=?", hero_name)
        return hero

    def get_hero_as_df(self, hero_name, table_name):
        hero = pd.read_sql_query(f"SELECT * FROM {table_name} WHERE name='{hero_name}'", self.conn)
        return hero

    def add_all_heroes(self, n=None, table_name='heroes'):
        all_heroes = scrape_all(n=n)

        for hero_url, hero_info in all_heroes.items():
            hero_info.update({'url_name': hero_url})
            self.add_hero_to_db(hero_info, table_name)

    def add_hero(self, url_name, table_name='heroes'):
        hero_url, hero_info = scrape_hero(url_name)
        hero_info.update({'url_name': url_name})

        self.add_hero_to_db(hero_info, table_name)

    def heroes_to_df(self, table_name='heroes'):
        heroes = pd.read_sql_query(f"SELECT * FROM {table_name}", self.conn)
        return heroes


def update_db():
    dbc = DBClass()
    dbc.add_all_heroes()


def main():
    pass


if __name__ == '__main__':
    main()
