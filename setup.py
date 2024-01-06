from setuptools import setup, find_packages

VERSION = '0.1'
DESCRIPTION = 'A utility to provide easy interaction with HubSpot and common tools'

setup(
    name='hubspot_tools',
    version=VERSION,
    author='Reed Iandolo',
    author_email='riandolo103@gmail.com',
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests', 'python-dotenv']
)