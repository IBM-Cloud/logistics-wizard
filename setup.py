"""
A proxy app for the Logistics Wizard demo system

See:
https://github.com/IBM-Bluemix/cf-deployment-tracker-service
https://github.com/IBM-Bluemix/cf-deployment-tracker-client-python
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='logistics-wizard',
    version='0.1.0',
    description='Proxy app for the Logistics Wizard demo system',
    long_description=long_description,
    url='https://github.com/IBM-Bluemix/logistics-wizard',
    author='Jake Peyser',
    author_email='jepeyser@us.ibm.com',
    license='Apache-2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7'
    ],
    keywords='demos samples logistics hybrid-cloud microservices',
    packages=find_packages(),
    install_requires=['Flask,Flask-Cors>=2,gunicorn>=19,requests>=2,PyJWT>=1,decorator>=4,cf-deployment-tracker'],
)
