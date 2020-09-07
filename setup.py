from setuptools import setup


setup(
    name='heroes_app',
    keywords='',
    version='0.1',
    author='Niels Hoogeveen',
    entry_points={
        'console_scripts': [
            'heroes = heroes_app.app:main',
            'update_db = heroes_app.db:update_db'
        ]
    }
)
