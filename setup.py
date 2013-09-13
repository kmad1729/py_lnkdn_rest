import os
from setuptools import setup

#Utility function to read the README file
#Used for the long_description.

def read(fname):
    return open(os.path.join(os.path.dirname(__file__),fname)).read()

setup(
    name = "py_lnkdn_rest",
    version = "0.1",
    author = "Kashyap Maduri",
    author_email = "kashyap.mad@gmail.com",
    description = ("A utility API to connect and extract data to linkedin REST API"),
    packages = ['py_lnkdn_rest'],
    long_description = read('README'),
    classifiers= [
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Utilities"
    ],
)
