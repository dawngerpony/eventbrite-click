try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Eventbrite Click',
    'author': 'Dafydd James',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'dafydd@cantab.net',
    'version': '0.1.0',
    'install_requires': ['nose'],
    'packages': ['ebclick'],
    'scripts': [],
    'name': 'ebclick'
}

setup(**config)
