import os

from setuptools import find_packages, setup

from wikijs import __VERSION__

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='allianceauth-wiki-js',
    version=__VERSION__,
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='Alliance Auth Service module for Wiki JS',
    long_description=long_description,
    url="https://github.com/pvyParts/allianceauth-wiki-js",
    long_description_content_type='text/markdown',
    author='AaronKable',
    author_email='aaronkable@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    python_requires='>=3.8',
    install_requires=[
        "allianceauth>=2.15.1,<4.0.0",
        "graphqlclient"
    ],
    extras_require={
        'discordbot': ["allianceauth-discordbot>=3.0.0"]
    },
)
