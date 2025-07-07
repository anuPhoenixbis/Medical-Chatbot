# we have to define setup.py to make the package installable
#from src folder so that we can use these imports locally
from setuptools import setup, find_packages

#created the setup function with package details
setup(
    name='medical_chatbot',
    version='0.1',
    description='A medical chatbot for answering health-related questions',
    author='Anubhav',
    packages=find_packages(),
    install_requires=[]
)

#initializing the package
#this will create a dist folder with the package files
#to look for which folders are included in the package, we can use the find_packages function
#this will find all the packages in the folder that have an __init__.py file
#the install_requires parameter is used to specify the dependencies of the package