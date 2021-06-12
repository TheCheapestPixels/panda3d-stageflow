"""A setuptools based setup module.
"""

from setuptools import setup, find_packages
from os import path


here = path.abspath(path.dirname(__file__))
with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='panda3d-stageflow',
    version='0.1b4',
    description='A kind of FSM for game states',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/TheCheapestPixels/panda3d-stageflow/',
    author='TheCheapestPixels',
    author_email='TheCheapestPixels@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='stageflow panda3d',
    packages=find_packages(exclude=['tests', 'examples']),
    python_requires='>=3.5, <4',
    install_requires=[],
    extras_require={},
)
