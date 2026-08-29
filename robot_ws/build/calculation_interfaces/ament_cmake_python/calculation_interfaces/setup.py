from setuptools import find_packages
from setuptools import setup

setup(
    name='calculation_interfaces',
    version='0.0.0',
    packages=find_packages(
        include=('calculation_interfaces', 'calculation_interfaces.*')),
)
