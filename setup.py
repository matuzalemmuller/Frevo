from setuptools import setup

setup(
   name='frevo',
   version='1.0.0',
   description='Run terminal commands directly from your Mac top bar',
   url='https://gitlab.com/matuzalemmuller/frevo',
   license='GNU GPLv3',
   author='Mat Muller',
   author_email='matmuller.development@gmail.com',
   packages=['frevo'],  
   install_requires=['PyQt5', 'appscript', 'PyObjC'], 
)