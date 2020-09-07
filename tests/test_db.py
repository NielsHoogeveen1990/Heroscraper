import pytest
import os
from shutil import rmtree


from heroes_app.db import *

# DB settings
TEST_DB_FOLDER = 'test_db'
TEST_DB_NAME = TEST_DB_FOLDER + '/test.db'

# Table settings
TEST_TABLE_NAME = 'test_table'
TEST_TABLE_FORMAT = {'name': 'text', 'skill': 'integer'}

SINGLE_HERO = {'name': 'piet', 'skill': 9000}
SINGLE_HERO_TUPLE = ('piet', 9000)

@pytest.fixture
def db_class():
    os.mkdir(TEST_DB_FOLDER)

    yield DBClass(TEST_DB_NAME, table_name=TEST_TABLE_NAME, table_format=TEST_TABLE_FORMAT)

    rmtree(TEST_DB_FOLDER)


def test_init(db_class):

    # Check that connection is set
    assert isinstance(db_class.conn, sqlite3.Connection)

    # Check that database table has 0 rows and all columns exist
    assert db_class.run_query(f'SELECT Count(*) FROM {TEST_TABLE_NAME}')[0][0] == 0
    assert isinstance(db_class.run_query(f'SELECT {" ".join(TEST_TABLE_FORMAT.keys())} FROM {TEST_TABLE_NAME}'), list)


def test_run_query(db_class):
    # Test that we can add values and retrieve them
    db_class.run_query(f'INSERT INTO {TEST_TABLE_NAME} VALUES {SINGLE_HERO_TUPLE}')
    assert db_class.run_query(f'SELECT * FROM {TEST_TABLE_NAME}')[0] == SINGLE_HERO_TUPLE


def test_create_table(db_class):
    # Test that we can create a table
    table_name = 'table2'
    db_class.create_table(table_name=table_name, table_format=TEST_TABLE_FORMAT)
    assert db_class.run_query(f'SELECT Count(*) FROM {table_name}')[0][0] == 0

    # Test that if we create a table that exists nothing happens
    db_class.run_query(f'INSERT INTO {table_name} VALUES {SINGLE_HERO_TUPLE}')
    db_class.create_table(table_name=table_name, table_format=TEST_TABLE_FORMAT)
    assert db_class.run_query(f'SELECT Count(*) FROM {table_name}')[0][0] == 1


def test_add_hero_to_db(db_class):
    db_class.add_hero_to_db(SINGLE_HERO, TEST_TABLE_NAME)
    assert db_class.run_query(f'SELECT * FROM {TEST_TABLE_NAME}')[0] == SINGLE_HERO_TUPLE


def test_get_hero_from_db(db_class):
    table_name = TEST_TABLE_NAME
    db_class.add_hero_to_db(SINGLE_HERO, table_name)
    assert db_class.get_hero_from_db(SINGLE_HERO_TUPLE[0], table_name)[0] == SINGLE_HERO_TUPLE


def test_get_hero_as_df(db_class):
    table_name = TEST_TABLE_NAME
    db_class.add_hero_to_db(SINGLE_HERO, table_name)
    single_hero = {k: [v] for k, v in SINGLE_HERO.items()}
    pd.testing.assert_frame_equal(
        db_class.get_hero_as_df(SINGLE_HERO_TUPLE[0], table_name), pd.DataFrame.from_dict(single_hero, 'columns')
    )


def test_add_all_heroes():
    pass


def test_add_hero():
    pass


def test_heroes_to_df(db_class):
    table_name = TEST_TABLE_NAME
    db_class.add_hero_to_db(SINGLE_HERO, table_name)
    single_hero = {k: [v] for k, v in SINGLE_HERO.items()}
    pd.testing.assert_frame_equal(
        db_class.heroes_to_df(table_name), pd.DataFrame.from_dict(single_hero, 'columns')
    )
