from setuptools import setup, find_packages

requires = [
    'flask',
    'flask-sqlalchemy',
    'psycopg2',
    'gunicorn'
]

setup(
    name='informal-economy-backend-server',
    version='0.0',
    keywords='web flask',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)   